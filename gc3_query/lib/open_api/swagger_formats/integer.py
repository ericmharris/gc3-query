# -*- coding: utf-8 -*-

"""
#@Filename : integer
#@Date : [8/14/2018 2:35 PM]
#@Poject: gc3-query
#@AUTHOR : emharris

~~~~~~~~~~~~~~~~

<DESCR SHORT>

<DESCR>
"""

################################################################################
## Standard Library Imports
import sys, os
from decimal import Decimal
import re

################################################################################
## Third-Party Imports
import dateutil
import pytz
# from bson.int64 import long
from dataclasses import dataclass, field
from bravado_core.formatter import SwaggerFormat
from bravado_core.exception import SwaggerValidationError

################################################################################
## Project Imports

from gc3_query.lib import *
from gc3_query.lib.gc3logging import get_logging
_debug, _info, _warning, _error, _critical = get_logging(name=__name__)



def NO_OP(x):
    return x




DEFAULT_FORMATS = {
    'byte': SwaggerFormat(
        format='byte',
        to_wire=lambda b: b if isinstance(b, str) else str(b),
        to_python=lambda s: s if isinstance(s, str) else str(s),
        validate=NO_OP,  # jsonschema validates string
        description='Converts [wire]string:byte <=> python byte'),
    'date': SwaggerFormat(
        format='date',
        to_wire=lambda d: d.isoformat(),
        to_python=lambda d: dateutil.parser.parse(d).date(),
        validate=NO_OP,  # jsonschema validates date
        description='Converts [wire]string:date <=> python datetime.date'),
    # Python has no double. float is C's double in CPython
    'double': SwaggerFormat(
        format='double',
        to_wire=lambda d: d if isinstance(d, float) else float(d),
        to_python=lambda d: d if isinstance(d, float) else float(d),
        validate=NO_OP,  # jsonschema validates number
        description='Converts [wire]number:double <=> python float'),
    'date-time': SwaggerFormat(
        format='date-time',
        to_wire=lambda dt: (dt if dt.tzinfo else pytz.utc.localize(dt)).isoformat(),
        to_python=lambda dt: dateutil.parser.parse(dt),
        validate=NO_OP,  # jsonschema validates date-time
        description=(
            'Converts string:date-time <=> python datetime.datetime')),
    'float': SwaggerFormat(
        format='float',
        to_wire=lambda f: f if isinstance(f, float) else float(f),
        to_python=lambda f: f if isinstance(f, float) else float(f),
        validate=NO_OP,  # jsonschema validates number
        description='Converts [wire]number:float <=> python float'),
    'int32': SwaggerFormat(
        format='int32',
        to_wire=lambda i: i if isinstance(i, int) else int(i),
        to_python=lambda i: i if isinstance(i, int) else int(i),
        validate=NO_OP,  # jsonschema validates integer
        description='Converts [wire]integer:int32 <=> python int'),
    'int64': SwaggerFormat(
        format='int64',
        to_wire=lambda i: i if isinstance(i, long) else long(i),
        to_python=lambda i: i if isinstance(i, long) else long(i),
        validate=NO_OP,  # jsonschema validates integer
        description='Converts [wire]integer:int64 <=> python long'),
}

integer_format = SwaggerFormat(
        format='integer',
        to_wire=lambda i: i if isinstance(i, int) else int(i),
        to_python=lambda i: i if isinstance(i, int) else int(i),
        validate=NO_OP,  # jsonschema validates integer
        description='Converts [wire]integer:int32 <=> python int')


int64_format = SwaggerFormat(
    format='int64',
    to_wire=lambda i: i if isinstance(i, long) else long(i),
    to_python=lambda i: i if isinstance(i, long) else long(i),
    validate=NO_OP,  # jsonschema validates integer
    description='Converts [wire]integer:int64 <=> python long')


is_decimal = re.compile(r'^\d+(?:\.\d+)?$')

def validate_decimaltype(x):
  """Validate input is a str in valid decimal format"""
  if not (isinstance(x, str) and is_decimal.match(x)):
      raise SwaggerValidationError()

mydouble = SwaggerFormat(
  format='double',
  to_wire=lambda x: str(x) if isinstance(x, Decimal) else str(Decimal(x)),
  to_python=lambda x: x if isinstance(x, Decimal) else Decimal(x),
  validate=validate_decimaltype,
  description="model format double internally as Decimal()"
)