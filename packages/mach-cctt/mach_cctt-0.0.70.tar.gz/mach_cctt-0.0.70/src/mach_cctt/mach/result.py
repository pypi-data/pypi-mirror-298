from dataclasses import dataclass
from typing import Tuple

from eth_typing import ChecksumAddress
from hexbytes import HexBytes
from mach_client import Token
from mach_client.client import GasEstimate, Order, Quote
from web3.contract.async_contract import AsyncContractFunction

from ..destination_policy import DestinationPolicy


@dataclass
class EmptySourceBalance:
    token: Token
    wallet: ChecksumAddress


@dataclass
class NoViableDestination:
    destination_policy: DestinationPolicy


@dataclass
class InsufficientDestinationGas:
    destination: Token
    gas_estimate: GasEstimate
    gas_available: int


@dataclass
class QuoteFailed:
    pair: Tuple[Token, Token]
    amount: int
    wallet: ChecksumAddress


@dataclass
class QuoteInvalidAmount:
    pair: Tuple[Token, Token]
    amount: int
    wallet: ChecksumAddress
    quote: Quote

@dataclass
class QuoteLiquidityUnavailable:
    pair: Tuple[Token, Token]
    amount: int
    wallet: ChecksumAddress
    quote: Quote


@dataclass
class RiskManagerRejection:
    pair: Tuple[Token, Token]
    amount: int
    quote: Quote


@dataclass
class CannotFill:
    pair: Tuple[Token, Token]
    amount: int
    quote: Quote


@dataclass
class ApprovalFailed:
    token: Token
    amount: int
    wallet: ChecksumAddress
    spender: ChecksumAddress


@dataclass
class PlaceOrderFailed:
    pair: Tuple[Token, Token]
    wallet: ChecksumAddress
    place_order_function: AsyncContractFunction
    order_direction: tuple[ChecksumAddress, ChecksumAddress, int]
    order_funding: tuple[int, int, int, ChecksumAddress, int]
    order_expiration: tuple[int, int, int]
    is_make: bool


@dataclass
class SubmitOrderFailed:
    pair: Tuple[Token, Token]
    place_order_tx: HexBytes


@dataclass
class SourceNotWithdrawn:
    pair: Tuple[Token, Token]
    order: Order
    wait_time: int


@dataclass
class DestinationNotReceived:
    pair: Tuple[Token, Token]
    order: Order
    wait_time: int


TradeError = (
    EmptySourceBalance
    | NoViableDestination
    | InsufficientDestinationGas
    | QuoteFailed
    | QuoteInvalidAmount
    | QuoteLiquidityUnavailable
    | RiskManagerRejection
    | CannotFill
    | ApprovalFailed
    | PlaceOrderFailed
    | SubmitOrderFailed
    | SourceNotWithdrawn
    | DestinationNotReceived
)


@dataclass
class Trade:
    pair: Tuple[Token, Token]
    quote: Quote
    order: Order


TradeResult = Trade | TradeError
