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


def is_bool_like(spec):
    """
    :param spec: swagger object specification in dict form
    :rtype: boolean
    """
    # Calling isinstance(spec, Mapping) is relatively slow. As this function
    # gets usually called with a dict type argument we optimize for that case
    # by executing a much cheaper isinstance(spec, dict) check before the more
    # expensive isinstance(spec, Mapping) check.
    return isinstance(spec, (dict, Mapping))


# def is_list_like(spec):
#     """
#     :param spec: swagger object specification in dict form
#     :rtype: boolean
#     """
#     return isinstance(spec, (list, tuple))


