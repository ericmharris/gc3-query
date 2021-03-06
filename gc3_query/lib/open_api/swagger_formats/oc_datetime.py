# -*- coding: utf-8 -*-

"""
gc3-query.oc_datetime    [8/23/2018 10:15 AM]
~~~~~~~~~~~~~~~~

<DESCR SHORT>

<DESCR>
"""

################################################################################
## Standard Library Imports
import sys, os

################################################################################
## Third-Party Imports
import dateutil
from dataclasses import dataclass
import maya
from bravado_core.formatter import SwaggerFormat, NO_OP
from bravado_core.exception import SwaggerValidationError

################################################################################
## Project Imports
from gc3_query.lib.gc3logging import get_logging

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)



def NO_OP(x):
    return x


oc_datetime_format = SwaggerFormat(
    format='oc-datetime',
    to_wire=lambda dt: dt.iso8601(),
    to_python=lambda dt: maya.parse(dt),
    validate=NO_OP,  # jsonschema validates date-time
    description=(
        'Converts string:date-time <=> python datetime.datetime'))

paas_date_time =  SwaggerFormat(
        format='paas-date-time',
        to_wire=lambda dt: dt.iso8601(),
        to_python=lambda dt: maya.parse(dt),
        validate=NO_OP,  # jsonschema validates date-time
        description=(
            'Converts string:date-time <=> python datetime.datetime'))

date_time = SwaggerFormat(
    format='date-time',
    to_wire=lambda dt: (dt if dt.tzinfo else pytz.utc.localize(dt)).isoformat(),
    to_python=lambda dt: dateutil.parser.parse(dt),
    validate=NO_OP,  # jsonschema validates date-time
    description=('Converts string:date-time <=> python datetime.datetime'))

date = SwaggerFormat(
    format='date',
    to_wire=lambda d: d.isoformat(),
    to_python=lambda d: dateutil.parser.parse(d).date(),
    validate=NO_OP,  # jsonschema validates date
    description='Converts [wire]string:date <=> python datetime.date')