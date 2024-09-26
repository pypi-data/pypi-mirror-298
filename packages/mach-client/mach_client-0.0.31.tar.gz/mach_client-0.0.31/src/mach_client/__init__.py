from datetime import datetime as _datetime
import logging as _logging
from pathlib import Path as _Path
import sys as _sys
from typing import Optional as _Optional

from . import config as _config
from .client import client, MachClient, Quote
from .constants import ChainId
from .data_types import Chain, Token

__all__ = [
    "Chain",
    "ChainId",
    "client",
    "data_types",
    "MachClient",
    "Quote",
    "Token",
]


# Exclusive: log to stdout if logging to file?
def _make_logger(
    name: str, path: _Optional[_Path] = None, exclusive=False
) -> _logging.Logger:
    logger = _logging.getLogger(name)
    logger.setLevel(_logging.DEBUG)

    handler: _logging.Handler = _logging.FileHandler(path) if path else _logging.StreamHandler(_sys.stdout)  # type: ignore
    handler.setLevel(_logging.DEBUG)
    logger.addHandler(handler)

    if path and not exclusive:
        handler = _logging.StreamHandler(_sys.stdout)
        handler.setLevel(_logging.DEBUG)
        logger.addHandler(handler)

    logger.info(f"START {name} {_datetime.today()}\n")

    return logger


_path = _config.log_files.get("app")

_make_logger("mach-client", _Path(_path) if _path else None, True)
