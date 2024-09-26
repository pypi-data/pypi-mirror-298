from abc import ABC, abstractmethod

from eth_typing import ChecksumAddress
from mach_client import Quote, Token

from .. import config
from ..log import LogContextAdapter, Logger, make_logger


class RiskManager(ABC):
    def __init__(self, wallet: ChecksumAddress, log: Logger):
        self.log = log
        self.wallet = wallet
        pass

    @abstractmethod
    def check_order(
        self, src_token: Token, dest_token: Token, quote: Quote
    ) -> bool: ...


# Reject high-slippage orders between "similar" tokens (ie. between USD stablecoins, wrapped ETH tokens, etc.)
class SimilarTokenRiskManager(RiskManager):
    logger = make_logger("risk_manager", True, config.log_files["high_slippage"])

    special_usd_stablecoins = frozenset(
        (
            "DAI",
            "FRAX",
            "MIM",
        )
    )

    def __init__(self, wallet: ChecksumAddress, max_slippage: float):
        assert 0.0 <= max_slippage <= 1.0, "Slippage must be a percentage between 0 and 1"
        super().__init__(wallet, LogContextAdapter(self.logger, "Slippage manager"))
        self.max_slippage = max_slippage

    def check_order(self, src_token: Token, dest_token: Token, quote: Quote) -> bool:
        if (
            src_token.symbol == dest_token.symbol
            or ("USD" in src_token.symbol and "USD" in dest_token.symbol)
            or ("BTC" in src_token.symbol and "BTC" in dest_token.symbol)
            or ("ETH" in src_token.symbol and "ETH" in dest_token.symbol)
            or ("EUR" in src_token.symbol and "EUR" in dest_token.symbol)
            or (
                src_token.symbol in self.special_usd_stablecoins
                and dest_token.symbol in self.special_usd_stablecoins
            )
        ):
            # Convert from ticks to coin-denominated amounts
            src_amount = quote["src_amount"] / 10 ** src_token.decimals
            dest_amount = quote["dst_amount"] / 10 ** dest_token.decimals
            slippage = src_amount / dest_amount - 1.0
            self.log.debug(f"{src_token} => {dest_token} Slippage: {100 * slippage}%")
            return slippage >= -self.max_slippage

        self.log.debug(f"{src_token} and {dest_token} are not similar, ignoring")
        return True
