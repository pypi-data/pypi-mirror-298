from mach_client import ChainId, client, Token
from web3 import AsyncWeb3
from web3.types import Wei

from .utility import make_token_contract


def decimal_balance(chain: ChainId, symbol: str, balance: int) -> float:
    decimals = client.deployments[chain]["assets"][symbol]["decimals"]
    return balance / (10**decimals)


def _helper(chain: ChainId, raw_balances: dict[str, int]) -> dict[str, float]:
    return {
        symbol: decimal_balance(chain, symbol, balance)
        for symbol, balance in raw_balances.items()
    }


async def get_balance(w3: AsyncWeb3, token: Token) -> int:
    src_token_contract = make_token_contract(w3, token)
    return await src_token_contract.functions.balanceOf(w3.eth.default_account).call()


# Balances of a wallet denominated in coins instead of ticks
def get_balances(wallet: str) -> dict[ChainId, dict[str, float]]:
    raw_balances = client.get_token_balances(wallet)
    return {
        chain: _helper(chain, raw_chain_balances)
        for chain, raw_chain_balances in raw_balances.items()
    }


async def get_gas_balance(w3: AsyncWeb3) -> Wei:
    return await w3.eth.get_balance(w3.eth.default_account)  # type: ignore
