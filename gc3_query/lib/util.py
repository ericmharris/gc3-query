# -*- coding: utf-8 -*-

"""
gc3-query.util    [9/2/2018 2:13 PM]
~~~~~~~~~~~~~~~~

<DESCR SHORT>

<DESCR>
"""

################################################################################
## Standard Library Imports
import sys, os
import re

################################################################################
## Third-Party Imports
from dataclasses import dataclass

################################################################################
## Project Imports
from gc3_query.lib import *
from gc3_query.lib.gc3logging import  get_logging

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

_cts_underscore_ascii = re.compile(r'(.)([A-Z][a-z]+)')
_cts_underscore_alpha = re.compile('([a-z0-9])([A-Z])')

STR_TO_BOOL: Dict[str, bool] = {"true":True, "false":False}
BOOL_TO_STR: Dict[str, bool] = {True: "true", False: "false"}

def camelcase_to_snake(s: str) -> str:
    """ Convert CamelCase to snake_case

`    CamelCaseString -> camel_case_string`

    :param s:
    :return:
    """
    subbed = _cts_underscore_ascii.sub(r'\1_\2', s)
    return _cts_underscore_alpha.sub(r'\1_\2', subbed).lower()


def bool_to_str(b: bool) -> str:
    _s = BOOL_TO_STR.get(b, None)
    if _s is None:
        raise RuntimeError(f"Failed to convert bool to str")
    return _s

def str_to_bool(s: str) -> bool:
    _b = STR_TO_BOOL.get(s, None)
    if _b is None:
        raise RuntimeError(f"Failed to convert str to bool")
    return _b
