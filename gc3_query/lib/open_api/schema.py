# -*- coding: utf-8 -*-

"""
gc3-query.schema    [9/2/2018 1:50 PM]
~~~~~~~~~~~~~~~~

<DESCR SHORT>

<DESCR>
"""

################################################################################
## Standard Library Imports
import sys, os

################################################################################
## Third-Party Imports
from dataclasses import dataclass

################################################################################
## Project Imports
from gc3_query.lib import *
from gc3_query.lib.util import str_to_bool, bool_to_str
from gc3_query.lib.gc3logging import  get_logging

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

# -*- coding: utf-8 -*-
import copy
from collections import Mapping

from six import iteritems

from bravado_core.exception import SwaggerMappingError


# 'object' and 'array' are omitted since this should really be read as
# "Swagger types that map to python primitives"
SWAGGER_PRIMITIVES = (
    'integer',
    'number',
    'string',
    'boolean',
    'null',
)


def is_str_bool_like(s: str) -> bool:
    try:
        _s = str_to_bool(s)
    except RuntimeError:
        return False
    return True


# def is_list_like(spec):
#     """
#     :param spec: swagger object specification in dict form
#     :rtype: boolean
#     """
#     return isinstance(spec, (list, tuple))


