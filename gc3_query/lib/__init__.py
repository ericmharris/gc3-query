# -*- coding: utf-8 -*-

"""Top-level package for GC3 Query."""

# __all__ = ['Path', 'List', 'Optional', 'Any', 'Callable', 'Dict', 'Tuple', 'Union', 'Set', 'Generator']
from pathlib import Path
from typing import List, Optional, Any, Callable, Dict, Tuple, Union, Set, Generator, Iterable

from gc3_query.lib.gc3_config import GC3Config
from gc3_query.lib.gc3logging import get_logging



BASE_DIR: Path = Path(__file__).parent.parent
gc3_cfg = GC3Config()
