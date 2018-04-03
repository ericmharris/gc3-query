# -*- coding: utf-8 -*-

"""Library module for gc3query.



"""
# __all__ = ['UnexpectedThingHappenedException', 'InvalidThingHappenedException']


import click

from gc3_query import __version__
from gc3_query.lib import *
from gc3_query.lib.logging import Logging, get_logging

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help', '-?'], # help_option_names sets tokens that come after a command that'll trigger help.
                        ignore_unknown_options=True)

class BaseException(Exception):
    """
    Base custom exception
    """

    def __init__(self, msg=None, thing=None, other_thing=None):
        self.msg = msg
        self.thing = thing
        self.other_thing = other_thing

    def __str__(self):
        exception_msg = f"Message: {self.msg}\n"
        if self.thing is not None:
            exception_msg = f"{exception_msg}, other relevant thing\n"
        if self.other_thing is not None:
            other_thing = "\n".join(self.other_thing)
            exception_msg = f"{exception_msg}, other_thing:\n{other_thing}"
        return exception_msg


class UnexpectedThingHappenedException(BaseException):
    """Thrown when an unexpected thing happend . """
    def __init__(self, msg=None, thing=None, other_thing=None, alert_text=None):
        super().__init__(msg, thing, other_thing)
        self.alert_text = alert_text

    def __str__(self):
        return "Alert Text: {}\n{}".format(self.alert_text, super(UnexpectedThingHappenedException, self).__str__())


class InvalidThingHappenedException(BaseException):
    """
    Thrown when an invalid thing happened
    """
    pass