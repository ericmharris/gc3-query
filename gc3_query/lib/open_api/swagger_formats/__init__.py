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

from .json_bool import JsonBool
from .json_bool import json_bool_format
from .integer import integer_format, mydouble, int64_format
from .oc_datetime import date, date_time
from .oc_datetime import oc_datetime_format, paas_date_time
from .boolean_formats import bool_in_str

################################################################################
## Project Imports



gc3_formats: List[SwaggerFormat] = [bool_in_str, json_bool_format, oc_datetime_format, paas_date_time, integer_format, mydouble, int64_format, date, date_time]





