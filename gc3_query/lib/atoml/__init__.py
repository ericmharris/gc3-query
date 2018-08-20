# -*- coding: utf-8 -*-

from gc3_query.lib import gc3_cfg
from gc3_query import BASE_DIR
from gc3_query.lib.gc3logging import get_logging

from .atoml_config import ATomlConfig
from .config_factory import ConfigFactory

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

cfg = ConfigFactory()


