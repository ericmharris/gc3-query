# -*- coding: utf-8 -*-

from gc3_query.lib.gc3logging import get_logging


from .atoml_config import ATomlConfig
from .config_factory import ConfigFactory

from gc3_query.lib import get_logging
_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

cfg = ConfigFactory()


