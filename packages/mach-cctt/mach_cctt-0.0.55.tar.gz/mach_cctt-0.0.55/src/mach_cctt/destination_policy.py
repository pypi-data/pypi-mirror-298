from abc import ABC, abstractmethod
from collections import defaultdict
import random
from typing import AbstractSet, Optional

from mach_client import ChainId, client, Token

from .log import Logger, logger


class DestinationPolicy(ABC):
    def __init__(
        self,
        initial_excluded_chains: AbstractSet[ChainId] = client.excluded_chains,
        log: Logger = logger,
    ):
        self.log = log

        self.token_choices = defaultdict(
            set,
            {
                chain: set(chain_info["assets"].keys())
                - frozenset((client.gas_tokens[chain],))
                for chain, chain_info in client.deployments.items()
                if chain not in initial_excluded_chains
            },
        )

        self.tried_tokens: list[Token] = []
        self.tried_chains: list[tuple[ChainId, set[Token]]] = []

    # Produce the destination token for the next trade
    @abstractmethod
    def __call__(self) -> Optional[Token]: ...

    def permanently_exclude_chain(self, chain: ChainId) -> None:
        self.token_choices.pop(chain, None)

    def exclude_chain(self, chain: ChainId) -> None:
        if choices := self.token_choices.pop(chain, None):
            self.tried_chains.append((chain, choices))

    def exclude_token(self, token: Token) -> None:
        chain_id = token.chain.id

        self.token_choices[chain_id].remove(token.symbol)

        # Remove this chain if there are no tokens we can choose from it
        if not self.token_choices[chain_id]:
            self.token_choices.pop(chain_id)

        self.tried_tokens.append(token)

    # Reset for the next trade
    def reset(self) -> None:
        for chain, tokens in self.tried_chains:
            self.token_choices[chain] = tokens

        self.tried_chains.clear()

        for token in self.tried_tokens:
            self.token_choices[token.chain.id].add(token.symbol)

        self.tried_tokens.clear()


class RandomChainFixedSymbolPolicy(DestinationPolicy):
    def __init__(
        self,
        symbol: str,
        initial_excluded_chains: AbstractSet[ChainId] = client.excluded_chains,
    ):
        super().__init__(initial_excluded_chains)
        self.symbol = symbol

    def __call__(self) -> Optional[Token]:
        try:
            chain = random.choice(tuple(self.token_choices.keys()))
        except IndexError:
            self.log.critical(
                "Unable to choose destination token - all choices have been excluded"
            )
            return None

        return Token.from_components(chain, self.symbol)


class CheapChainFixedSymbolPolicy(RandomChainFixedSymbolPolicy):
    cheap_chains = frozenset((ChainId.ARBITRUM, ChainId.BASE, ChainId.OP))

    def __init__(self, symbol: str):
        super().__init__(
            symbol,
            client.excluded_chains.intersection(client.chains - self.cheap_chains),
        )


class RandomChainRandomSymbolPolicy(DestinationPolicy):
    def __init__(self):
        super().__init__()

    def __call__(self) -> Optional[Token]:
        try:
            chain = random.choice(tuple(self.token_choices.keys()))
            symbol = random.choice(tuple(self.token_choices[chain]))
        except IndexError:
            self.log.critical(
                "Unable to choose destination token - all choices have been excluded"
            )
            return None

        return Token.from_components(chain, symbol)


class FixedTokenSingleTradePolicy(DestinationPolicy):
    def __init__(self, token: Token):
        super().__init__()
        self.token = token
        self.called = False

    def __call__(self) -> Optional[Token]:
        if self.called:
            return None

        self.called = True
        return self.token

    def permanently_exclude_chain(self, chain: ChainId) -> None:
        pass

    def exclude_chain(self, chain: ChainId) -> None:
        pass

    def exclude_token(self, token: Token) -> None:
        pass

    def reset(self) -> None:
        pass
