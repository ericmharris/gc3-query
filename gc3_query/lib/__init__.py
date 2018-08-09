# -*- coding: utf-8 -*-

"""Top-level package for GC3 Query."""

# __all__ = ['Path', 'List', 'Optional', 'Any', 'Callable', 'Dict', 'Tuple', 'Union', 'Set', 'Generator']
from pathlib import Path
from typing import List, Optional, Any, Callable, Dict, Tuple, Union, Set, Generator, Iterable
DictStrAny = Dict[str, Any]

from gc3_query.lib.gc3_config import GC3Config
from gc3_query.lib.gc3logging import get_logging


gc3_cfg = GC3Config()

BASE_DIR: Path = Path(__file__).parent.parent
CONFIG_DIR: Path = BASE_DIR.joinpath(gc3_cfg.atoml.config_dir)
OPEN_API_CATALOG_DIR: Path = BASE_DIR.joinpath(gc3_cfg.open_api.api_catalog_dir)
