import asyncio
import logging
from pprint import pformat
import time
from typing import Optional

from eth_account.signers.local import LocalAccount
from hexbytes import HexBytes
from mach_client import ChainId, client, Token
from web3 import AsyncWeb3
from web3.contract import AsyncContract

from ..balances import get_balance, get_gas_balance
from .. import config
from ..destination_policy import DestinationPolicy
from ..log import LogContextAdapter, make_logger
from ..safe_transactions import safe_build_and_send_tx
from ..utility import (
    choose_source_token,
    make_order_book_contract,
    make_w3,
)
from .risk_manager import SimilarTokenRiskManager


logger = logging.getLogger("cctt")


async def ensure_approval(
    w3: AsyncWeb3,
    account: LocalAccount,
    spender_address,
    src_address,
    amount: int,
) -> Optional[HexBytes]:
    contract: AsyncContract = w3.eth.contract(address=src_address, abi=config.erc20_abi)

    try:
        allowance_func = contract.functions.allowance(
            account.address,
            spender_address,
        )
    except Exception as e:
        raise ValueError(f"failed to build allowance function: {e}") from e

    try:
        allowance: int = await allowance_func.call()
    except Exception as e:
        raise ConnectionError(f"failed to get allowance: {e}") from e

    logger.debug(f"Allowance of {allowance=}/{amount=} ({100 * allowance / amount}%)")

    if allowance >= amount:
        return None

    try:
        approve_func = contract.functions.approve(
            spender_address,
            amount,
        )
    except Exception as e:
        raise ValueError(f"failed to build approve function: {e}") from e

    logger.debug("Approving larger allowance")
    try:
        tx_hash = await safe_build_and_send_tx(
            w3,
            account,
            approve_func,
        )
    except Exception as e:
        raise ValueError(f"failed to send approve tx: {e}") from e

    logger.debug(f"Approval transaction hash: {tx_hash.hex()}")
    return tx_hash


async def run(
    src_token: Token, destination_policy: DestinationPolicy, account: LocalAccount
) -> None:
    src_w3 = await make_w3(src_token.chain, account.address)
    src_order_book_contract = make_order_book_contract(src_w3, src_token)

    delayed_transaction_logger = make_logger(
        "delayed_transactions", False, config.log_files["delayed_transactions"]
    )
    stuck_transaction_logger = make_logger(
        "stuck_transactions", False, config.log_files["stuck_transactions"]
    )
    improper_fill_logger = make_logger(
        "improper_fills", False, config.log_files["improper_fills"]
    )

    excluded_chains: set[ChainId] = set()
    destination_policy.add_tried_chain(src_token.chain.id)

    risk_manager = SimilarTokenRiskManager(account.address, config.max_slippage)

    while True:
        log = LogContextAdapter(logger, f"{src_token} => (UNSELECTED)")

        initial_src_balance = await get_balance(src_w3, src_token)
        log.debug(f"{initial_src_balance=}")

        # TODO: some pairs have trouble filling 1 tick, so treat it as 0
        if initial_src_balance <= 1:
            log.critical(f"Source balance empty. Cannot continue trading.")
            break

        if not (dest_token := destination_policy()):
            return

        log = LogContextAdapter(logger, f"{src_token} => {dest_token}")

        destination_policy.add_tried_token(dest_token)
        dest_w3 = await make_w3(dest_token.chain, account.address)

        gas_estimate = client.estimate_gas(dest_token.chain.id)
        estimated_gas = gas_estimate["gas"] * gas_estimate["gas_price"]
        log.debug(f"Estimated gas cost: {estimated_gas}")

        available_gas = await get_gas_balance(dest_w3)
        log.debug(f"Available gas: {available_gas}")

        if available_gas < estimated_gas:
            log.info(
                f"Insufficient gas on chain {dest_token.chain.name}, will be excluded from future selection"
            )
            destination_policy.exclude_chain(dest_token.chain.id)
            excluded_chains.add(dest_token.chain.id)
            continue

        try:
            quote = client.request_quote(
                src_token,
                dest_token,
                initial_src_balance,
                src_w3.eth.default_account,  # type: ignore
            )
        except Exception as e:
            log.warning(f"Quote request failed: {e}")
            continue

        log.debug(f"Quote:")
        log.debug(pformat(quote))

        if quote["invalid_amount"]:
            log.warning(f"Quote had invalid amount")
            continue

        if not risk_manager.check_order(src_token, dest_token, quote):
            log.warning(f"Order rejected by risk manager")
            continue

        src_amount, dest_amount = quote["src_amount"], quote["dst_amount"]

        log.debug(
            f"Can fill {src_amount=}/{initial_src_balance=} ({100 * src_amount / initial_src_balance}%)"
        )

        assert src_amount <= initial_src_balance

        if src_amount < initial_src_balance:
            log.warning("Not enough liquidity to trade entire source balance")

            if src_amount <= 0:
                log.warning(f"Trying another destination")
                break

        # TODO: change
        try:
            await ensure_approval(
                src_w3,
                account,
                src_order_book_contract.address,
                src_token.contract_address,
                max(src_amount, config.solidity_uint_max),
            )
        except Exception as e:
            log.critical(f"Failed to ensure approval")
            raise e

        order_direction = (
            src_token.contract_address,  # srcAsset: address
            dest_token.contract_address,  # dstAsset: address
            dest_token.chain.lz_cid,  # dstLzc: uint32
        )

        order_funding = (
            src_amount,  # srcQuantity: uint96
            dest_amount,  # dstQuantity: uint96
            quote["bond_fee"],  # bondFee: uint16
            quote["bond_asset_address"],  # bondAsset: address
            quote["bond_amount"],  # bondAmount: uint96
        )

        order_expiration = (
            int(time.time()) + 3600,  # timestamp: uint32
            quote["challenge_offset"],  # challengeOffset: uint16
            quote["challenge_window"],  # challengeWindow: uint16
        )

        is_maker = False

        place_order = src_order_book_contract.functions.placeOrder(
            order_direction,
            order_funding,
            order_expiration,
            is_maker,
        )

        assert initial_src_balance == await get_balance(src_w3, src_token)

        try:
            tx_hash = await safe_build_and_send_tx(
                src_w3,
                account,
                place_order,
            )
            log.info(f"Placed order with hash: {tx_hash.hex()}")

            tx_receipt = await src_w3.eth.wait_for_transaction_receipt(tx_hash)
            log.debug("Receipt:")
            log.debug(pformat(dict(tx_receipt)))

        except Exception as e:
            log.warning(f"Failed to send the transaction: {e}")
            continue

        # These need to be computed before the order has been submitted
        start_dest_balance = await get_balance(dest_w3, dest_token)
        expected_src_balance = initial_src_balance - src_amount
        expected_dest_balance = start_dest_balance + dest_amount

        try:
            order_response = client.submit_order(src_token.chain.id, tx_hash)

        except Exception as e:
            log.warning(f"There was an error submitting this order: {e}")
            continue

        log.info("Submitted order")
        log.debug("Response:")
        log.debug(pformat(order_response))

        src_balance = await get_balance(src_w3, src_token)
        log.info(
            f"Waiting for source balance to be withdrawn ({src_balance=}, {expected_src_balance=})..."
        )
        prev_src_balance = src_balance

        count = 0

        while (
            src_balance := await get_balance(src_w3, src_token)
        ) > expected_src_balance and count < config.max_polls:
            count += 1

            if (filled_amount := prev_src_balance - src_balance) > 0:
                log.warning(
                    f"Expected to fill {src_amount} ticks, actually filled {filled_amount} ticks"
                )
                improper_fill_logger.warning(f"Underfill {src_amount - filled_amount}:")
                improper_fill_logger.warning(pformat(order_response) + "\n")
                break

            prev_src_balance = src_balance

            await asyncio.sleep(config.poll_timeout)

        if count >= config.max_polls:
            log.warning("Source balance not withdrawn after max waiting time")
            delayed_transaction_logger.warning(pformat(order_response) + "\n")
            continue

        dest_balance = await get_balance(dest_w3, dest_token)
        log.info(
            f"Source balance withdrawn, waiting to receive destination token ({dest_balance=}, {expected_dest_balance=})..."
        )
        prev_dest_balance = dest_balance

        count = 0

        while (
            dest_balance := await get_balance(dest_w3, dest_token)
        ) < expected_dest_balance and count < config.max_polls:

            count += 1

            if (received_amount := dest_balance - prev_dest_balance) > 0:
                log.warning(
                    f"Expected to receive {dest_amount} ticks, actually received {received_amount} ticks"
                )
                improper_fill_logger.warning(
                    f"Underreceive {dest_amount - received_amount}:"
                )
                improper_fill_logger.warning(pformat(order_response) + "\n")
                break

            prev_dest_balance = dest_balance

            await asyncio.sleep(config.poll_timeout)

        if count >= config.max_polls:
            log.warning("Exceeded max number of polls. Transaction possibly stuck.")
            stuck_transaction_logger.warning(pformat(order_response) + "\n")

            src_token = choose_source_token(excluded_chains, account.address)
            src_w3 = await make_w3(src_token.chain, account.address)
            src_order_book_contract = make_order_book_contract(src_w3, src_token)

        else:
            log.info("Destination balance received - order complete")

            src_token, src_w3, src_order_book_contract = (
                dest_token,
                dest_w3,
                make_order_book_contract(dest_w3, dest_token),
            )

        destination_policy.reset()
        destination_policy.add_tried_token(src_token)
        destination_policy.add_tried_chain(src_token.chain.id)
