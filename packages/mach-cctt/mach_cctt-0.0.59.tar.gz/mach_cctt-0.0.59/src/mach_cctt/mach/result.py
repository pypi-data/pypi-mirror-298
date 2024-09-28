from dataclasses import dataclass
from typing import Tuple

from eth_typing import ChecksumAddress
from hexbytes import HexBytes
from mach_client import ChainId, Token
from mach_client.client import GasEstimate, Quote
from web3.contract.async_contract import AsyncContractFunction


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


@dataclass
class SubmitOrderFailed:
    src_chain: ChainId
    place_order_tx: HexBytes


@dataclass
class SourceNotWithdrawn:
    order_response: dict
    wait_time: int


@dataclass
class DestinationNotReceived:
    order_response: dict
    wait_time: int


TradeError = (
    InsufficientDestinationGas
    | QuoteFailed
    | QuoteInvalidAmount
    | RiskManagerRejection
    | CannotFill
    | ApprovalFailed
    | PlaceOrderFailed
    | SubmitOrderFailed
    | SourceNotWithdrawn
    | DestinationNotReceived
)


@dataclass
class Order:
    pair: Tuple[Token, Token]
    quote: Quote
    response: dict


TradeResult = Order | TradeError
