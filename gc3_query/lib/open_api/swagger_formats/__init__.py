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
import sys, os

################################################################################
## Third-Party Imports
from dataclasses import dataclass, field
from bravado_core.formatter import SwaggerFormat

################################################################################
## Project Imports
from gc3_query.lib import *



from .boolean_string import BooleanString
from .boolean_string import boolean_string_format
from .integer import integer_format, mydouble, int64_format

formats: List[SwaggerFormat] = [boolean_string_format, integer_format, mydouble, int64_format]



