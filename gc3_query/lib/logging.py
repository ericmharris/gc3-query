# -*- coding: utf-8 -*-

import sys
from logbook import Logger, StreamHandler

from gc3_query.lib import *
from gc3_query.lib import Tuple, Callable, Union

# LOG_LEVEL='WARNING'
LOG_LEVEL = "DEBUG"


def get_logging(name: str, level: Union[int, str] = LOG_LEVEL) -> Tuple[Callable]:
    """Returns logging functions properly configured.


    _debug, _info, _warning, _error, _critical = get_logging(name=__name__)
    :param name:  Usually __main__
    :type name: str
    :param level: {'CRITICAL': 15, 'ERROR': 14, 'WARNING': 13, 'NOTICE': 12, 'INFO': 11, 'DEBUG': 10, 'TRACE': 9, 'NOTSET': 0}
    :type level: str
    :return: Callable
    :rtype:
    """

    StreamHandler(sys.stdout, level=level).push_application()
    logger = Logger(name)
    debug, info, warning, error, critical = logger.debug, logger.info, logger.warning, logger.error, logger.critical
    return debug, info, warning, error, critical
