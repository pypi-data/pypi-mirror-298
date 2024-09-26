from __future__ import annotations
from collections.abc import Callable
import logging
from pprint import pformat
from typing import Any, Iterator, TypedDict

import eth_typing
from hexbytes import HexBytes
import requests

from . import config
from .constants import ChainId


# Note: we should really just be deserializing the backend Quote type with BaseModel.validate_from_json
# - https://github.com/tristeroresearch/cache-half-full/blob/62b31212f0456e4fad564021289816d39345b49b/backend/api/v1/endpoints/quotes.py#L51
# - https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel.model_validate_json


class Quote(TypedDict):
    wallet_address: str
    src_chain: str
    dst_chain: str
    src_amount: int
    dst_amount: int
    bond_amount: int
    bond_fee: int
    src_asset_address: str
    bond_asset_address: str
    challenge_offset: int
    challenge_window: int
    invalid_amount: bool
    liquidity_source: str
    created_at: str
    expires_at: str


class GasEstimate(TypedDict):
    gas_estimate: int
    gas_price: int


class MachClient:
    # Routes
    orders = config.backend_url + config.endpoints["orders"]
    gas = config.backend_url + config.endpoints["gas"]
    quotes = config.backend_url + config.endpoints["quotes"]
    token_balances = config.backend_url + config.endpoints["token_balances"]
    get_config = config.backend_url + config.endpoints["get_config"]

    # Make some configuration accessible to the user
    excluded_chains = config.excluded_chains
    rpc_urls = config.rpc_urls

    def __init__(self, root_url: str = config.backend_url):
        self.root = root_url
        self.session = requests.Session()
        self.session.headers.update(
            {
                "accept": "application/json",
                "Content-Type": "application/json",
            }
        )
        self.logger = logging.getLogger("cctt")

        # Fetch config from API
        data: dict = {}
        response = self.session.get(
            MachClient.get_config,
            json=data,
        )
        raw_deployments = self._handle_response(response)["deployments"]

        # Initialize attributes
        self.deployments: dict[ChainId, dict[str, Any]] = {}
        self.gas_tokens: dict[ChainId, str] = {}
        self.chains: set[ChainId] = set()

        for chain_name, chain_data in raw_deployments.items():
            chain_id = ChainId.from_name(chain_name)

            if chain_id in MachClient.excluded_chains:
                continue

            if chain_id not in MachClient.rpc_urls.keys():
                self.logger.warning(f"{chain_id} RPC URL missing from config")
                continue

            # Convert from chain names to chain IDs
            del chain_data["chain_id"]
            self.deployments[chain_id] = chain_data

            self.chains.add(chain_id)

            # The gas token has "wrapped": True
            gas_tokens: Iterator = filter(
                lambda item: item[1].get("wrapped"), chain_data["assets"].items()
            )

            # Maps (symbol name, symbol data) -> symbol name
            gas_tokens = map(lambda item: item[0], gas_tokens)

            assert (
                gas_token := next(gas_tokens)
            ), f"No gas token in config of {chain_id}"

            self.gas_tokens[chain_id] = gas_token

            assert not (
                gas_token_2 := next(gas_tokens, None)
            ), f"Multiple gas tokens on {chain_id}: {gas_token}, {gas_token_2}"

    # TODO: Annotate return type with generics in Python 3.12+
    def _handle_response(
        self,
        response: requests.Response,
        on_success: Callable[[requests.Response], Any] = lambda r: r.json(),
    ) -> Any:
        match response.status_code:
            case 200:
                return on_success(response)

            case 422:
                self.logger.debug("Response:")
                self.logger.debug(pformat(response.json()))
                raise ValueError("Validation error: invalid request")

            case _:
                self.logger.debug("Response:")
                self.logger.debug(pformat(response.json()))
                raise RuntimeError(f"Unknown status code {response.status_code}")

    def request_quote(
        self,
        src_token: Token,  # type: ignore
        dest_token: Token,  # type: ignore
        src_amount: int,
        wallet: eth_typing.ChecksumAddress,
    ) -> Quote:
        data = {
            "dst_asset_address": dest_token.contract_address,
            "dst_chain": dest_token.chain.name,
            "src_amount": src_amount,
            "src_asset_address": src_token.contract_address,
            "src_chain": src_token.chain.name,
            "wallet_address": wallet,
        }

        response = self.session.post(
            MachClient.quotes,
            json=data,
        )

        return self._handle_response(response, lambda r: Quote(dict(r.json())))  # type: ignore

    def estimate_gas(self, chain: ChainId) -> GasEstimate:
        params = {"chain": str(chain)}

        response = self.session.get(MachClient.gas, params=params)

        return self._handle_response(response, lambda r: GasEstimate(dict(r.json())))  # type: ignore

    def submit_order(self, chain: ChainId, place_taker_tx: HexBytes) -> dict:
        data = {
            "chain": str(chain),
            "place_taker_tx": place_taker_tx.hex(),
        }

        response = self.session.post(
            MachClient.orders,
            json=data,
        )

        return self._handle_response(response)

    def get_token_balances(self, wallet_address: str) -> dict[ChainId, dict[str, int]]:
        params = {"wallet_address": wallet_address}

        response = self.session.get(MachClient.token_balances, params=params)

        raw_balances = self._handle_response(response)["balances"]

        return dict(
            # Filter out chains we don't support
            filter(
                lambda item: item[0] in self.chains,
                # Map chain names to IDs
                map(
                    lambda item: (ChainId.from_name(item[0]), item[1]),
                    raw_balances.items(),
                ),
            )
        )


# Singleton
client = MachClient()
