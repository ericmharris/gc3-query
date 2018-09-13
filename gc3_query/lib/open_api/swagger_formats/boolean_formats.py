# -*- coding: utf-8 -*-

"""
gc3-query.boolean_formats    [9/2/2018 2:02 PM]
~~~~~~~~~~~~~~~~

<DESCR SHORT>

<DESCR>
"""

################################################################################
## Standard Library Imports

################################################################################
## Third-Party Imports
from bravado_core.formatter import SwaggerFormat, NO_OP
from bravado_core.exception import SwaggerValidationError

################################################################################
## Project Imports
from gc3_query.lib import *
from gc3_query.lib.util import str_to_bool, bool_to_str
from gc3_query.lib.open_api.schema import is_str_bool_like

from gc3_query.lib.gc3logging import get_logging

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


boolean = SwaggerFormat(
    format='boolean',
    to_wire=bool_to_str,
    to_python=str_to_bool,
    validate=is_str_bool_like,
    description='Converts "true" and "false" to/from equivalent booleans.')

