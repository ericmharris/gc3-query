# -*- coding: utf-8 -*-

import logging
from logging import RootLogger
from typing import Callable, Tuple


class Logging:
    # default_logging_level = 'warning'
    default_logging_level = 'debug'
    logging_levels = {'debug': logging.DEBUG,
                      'info': logging.INFO,
                      'warning': logging.WARN,
                      'error': logging.ERROR,
                      'critical': logging.CRITICAL}

    def __init__(self, level=None):
        """Configure logging and store runtime default_logging_level in class variable

        :param level: One of debug, info, warning, error, critical.
        :type level: str
        """
        self.logger: RootLogger = None
        self.logging_level = level if level else self.default_logging_level
        logging.basicConfig(level=Logging.logging_levels[self.logging_level])


    def get_logging(self, name: str, level=None) -> Tuple[Callable]:
        """Returns logging functions properly configured.
        _debug, _info, _warning, _error, _critical = get_logging(name=__name__)

        :param name:  Usually __main__
        :type name: str
        :param level: Desired logging level (will update all logging to that level)
        :type level: str
        :return: Callable
        :rtype:
        """
        self.logger = logging.getLogger(name=name)
        if level:
            self.logger.setLevel(Logging.logging_levels[level])
        else:
            self.logger.setLevel(Logging.logging_levels[self.default_logging_level])
        debug, info, warning, error, critical = self.logger.debug, self.logger.info, self.logger.warning, self.logger.error, self.logger.critical
        return debug, info, warning, error, critical

    @classmethod
    def set_default_logging_level(cls, level: str) -> str:
        """Sets the logging level used by all logging"""
        cls.default_logging_level = level
        return level



def get_logging(name: str, level=None) -> Tuple[Callable]:
    """Returns logging functions properly configured.
    _debug, _info, _warning, _error, _critical = get_logging(name=__name__)

    :param name:  Usually __main__
    :type name: str
    :param level: Desired logging level (will update all logging to that level)
    :type level: str
    :return: Callable
    :rtype:
    """
    _logging = Logging(level=level)
    debug, info, warning, error, critical = _logging.get_logging(name=name, level=level)
    return debug, info, warning, error, critical
