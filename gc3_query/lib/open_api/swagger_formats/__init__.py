# -*- coding: utf-8 -*-

"""
#@Filename : __init__.py
#@Date : [8/13/2018 4:04 PM]
#@Poject: gc3-query
#@AUTHOR : emharris

~~~~~~~~~~~~~~~~

<DESCR SHORT>

<DESCR>
"""

################################################################################
## Standard Library Imports

################################################################################
## Third-Party Imports
from gc3_query.lib import *
from bravado_core.formatter import SwaggerFormat

from .boolean_string import BooleanString
from .boolean_string import boolean_string_format
from .integer import integer_format, mydouble, int64_format

################################################################################
## Project Imports

formats: List[SwaggerFormat] = [boolean_string_format, integer_format, mydouble, int64_format]



