# Note: this module should really be merged with the data_types module, but is kept separate to avoid circular imports in the client module

from enum import IntEnum

from eth_typing import ChecksumAddress


class ChainId(IntEnum):
    ETHEREUM = 1
    OP = 10
    POLYGON = 137
    OPBNB = 204
    MANTLE = 5000
    BASE = 8453
    MODE = 34443
    ARBITRUM = 42161
    CELO = 42220
    AVALANCHE_C_CHAIN = 43114
    BLAST = 81457
    SCROLL = 54352

    @staticmethod
    def from_name(name: str) -> "ChainId":
        return CHAIN_IDS[name]

    def __str__(self):
        return CHAIN_NAMES[self]


CHAIN_NAMES = {
    ChainId.ETHEREUM: "ethereum",
    ChainId.OP: "optimism",
    ChainId.POLYGON: "polygon",
    ChainId.OPBNB: "opbnb",
    ChainId.MANTLE: "mantle",
    ChainId.BASE: "base",
    ChainId.MODE: "mode",
    ChainId.ARBITRUM: "arbitrum",
    ChainId.CELO: "celo",
    ChainId.AVALANCHE_C_CHAIN: "avalanche",
    ChainId.BLAST: "blast",
    ChainId.SCROLL: "scroll",
}

CHAIN_IDS = {name: id for id, name in CHAIN_NAMES.items()}

SCANNERS = {
    ChainId.ETHEREUM: "https://etherscan.io",
    ChainId.OP: "https://optimistic.etherscan.io",
    ChainId.POLYGON: "https://polygonscan.com",
    ChainId.OPBNB: "https://bscscan.com",
    ChainId.MANTLE: "https://explorer.mantle.xyz",
    ChainId.BASE: "https://basescan.org",
    ChainId.MODE: "https://modescan.io",
    ChainId.ARBITRUM: "https://arbiscan.io",
    ChainId.CELO: "https://explorer.celo.org/mainnet",
    ChainId.AVALANCHE_C_CHAIN: "https://snowscan.xyz",
    ChainId.BLAST: "https://blastscan.io",
    ChainId.SCROLL: "https://scrollscan.com",
}


def get_scanner_address(chain_id: ChainId, wallet: ChecksumAddress) -> str:
    return f"{SCANNERS[chain_id]}/address/{wallet}"


def get_scanner_tx(chain_id: ChainId, tx_hash: ChecksumAddress) -> str:
    return f"{SCANNERS[chain_id]}/tx/{tx_hash}"


def get_scanner_token(chain_id: ChainId, token_address: ChecksumAddress) -> str:
    return f"{SCANNERS[chain_id]}/token/{token_address}"
