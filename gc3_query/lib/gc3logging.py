# -*- coding: utf-8 -*-

import sys

from pathlib import Path
from typing import List, Optional, Any, Callable, Dict, Tuple, Union, Set, Generator, Iterable

from logbook import Logger, StreamHandler


LOG_LEVEL='WARNING'
# LOG_LEVEL = "DEBUG"


def get_logging(name: str, level: Union[int, str] = LOG_LEVEL) -> Tuple[Callable]:
    """Returns logging functions properly configured.


    from gc3_query.lib import get_logging
_debug, _info, _warning, _error, _critical = get_logging(name=__name__)
    :param name:  Usually __main__
    :type_name name: str
    :param level: {'CRITICAL': 15, 'ERROR': 14, 'WARNING': 13, 'NOTICE': 12, 'INFO': 11, 'DEBUG': 10, 'TRACE': 9, 'NOTSET': 0}
    :type_name level: str
    :return: Callable
    :rtype:
    """

    StreamHandler(sys.stdout, level=level).push_application()
    logger = Logger(name)
    debug, info, warning, error, critical = logger.debug, logger.info, logger.warning, logger.error, logger.critical
    return debug, info, warning, error, critical
