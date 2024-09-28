import functools
from typing import AbstractSet

from eth_account.signers.local import LocalAccount
from mach_client import ChainId, Token
import pandas as pd
from web3 import AsyncWeb3
from web3.contract import AsyncContract

from .. import config


atoken_addresses: pd.DataFrame = None  # type: ignore


# Initializes atoken_addresses and returns the list of tokens it contains
def initialize(chains: AbstractSet[ChainId], symbols: AbstractSet[str]) -> list[Token]:
    global atoken_addresses

    df = pd.read_csv(
        "https://raw.githubusercontent.com/bgd-labs/aave-address-book/main/safe.csv"
    )
    df.columns = pd.Index(("address", "name", "chain_id"))

    # Space-separated keywords
    df["keywords"] = df["name"].str.split()

    # Filter for only assets and their Aave aToken equivalents
    df = df[
        (df["keywords"].str[1] == "ASSETS")
        & df["keywords"].str[3].isin(("A_TOKEN", "UNDERLYING"))
    ]

    # Filter rows where the first token starts with "AaveV3"
    df = df[df["keywords"].str[0].str.startswith("AaveV3")]

    # Remove the "AaveV3" prefix and lowercase the rest of the string
    df["keywords"] = df["keywords"].apply(
        lambda tokens: [tokens[0][6:].lower()] + [tokens[1], tokens[2], tokens[3]]
    )

    # Create the new columns from the tokens
    df["chain_name"] = pd.Categorical(df["keywords"].str[0])
    df["symbol"] = pd.Categorical(df["keywords"].str[2])
    df["token_type"] = pd.Categorical(
        df["keywords"].str[3], categories=["A_TOKEN", "UNDERLYING"]
    )

    df = df[df["chain_id"].isin(chains) & df["symbol"].isin(symbols)]

    # Split the DataFrame into A_TOKEN and UNDERLYING subsets
    df_atoken = df[df["token_type"] == "A_TOKEN"].copy()
    df_underlying = df[df["token_type"] == "UNDERLYING"].copy()

    # Merge the two DataFrames on all columns except for 'address' and 'token_type'
    df = pd.merge(
        df_underlying[["chain_name", "symbol", "chain_id", "address"]],
        df_atoken[["chain_name", "symbol", "chain_id", "address"]],
        on=["chain_name", "symbol", "chain_id"],
        suffixes=("_underlying", "_atoken"),
    )

    df.rename(columns={"address_underlying": "address"}, inplace=True)

    result = [
        Token.from_components(ChainId(row[0]), row[1])
        for row in df[["chain_id", "symbol"]].itertuples(index=False)
    ]

    df.set_index(["chain_id", "symbol"], inplace=True)
    df.sort_index(inplace=True)

    atoken_addresses = df

    return result


async def get_atoken_balance(w3: AsyncWeb3, token: Token, account: LocalAccount) -> int:
    symbol = token.symbol if token.symbol != "USDC" else "USDCn"
    atoken_address: str = atoken_addresses.loc[
        (token.chain.id, symbol), "address_atoken"
    ]  # type: ignore
    atoken_contract = w3.eth.contract(address=atoken_address, abi=config.erc20_abi)  # type: ignore

    return await atoken_contract.functions.balanceOf(account.address).call()


@functools.cache
async def get_all_atokens(w3: AsyncWeb3, chain: ChainId):
    contract_address = config.aave_pool_data_provider_addresses[chain]
    pool_data_provider = w3.eth.contract(address=contract_address, abi=config.aave_pool_data_provider_abi)  # type: ignore
    return await pool_data_provider.functions.getAllATokens().call()


# async def get_atoken_balance_v2(
#     w3: AsyncWeb3, token: Token, account: LocalAccount
# ) -> int:
#     chain = token.chain.id
#     atokens = await get_all_atokens(w3, chain)
    