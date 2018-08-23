# -*- coding: utf-8 -*-

"""
#@Filename : json_bool
#@Date : [8/13/2018 4:05 PM]
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
from bravado_core.formatter import SwaggerFormat
from bravado_core.exception import SwaggerValidationError

################################################################################
## Project Imports
from gc3_query.lib import *
from gc3_query.lib.gc3logging import get_logging

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


class JsonBool:
    str_to_bool: Dict[str, bool] = dict(true=True, false=False)

    def __init__(self, from_wire: str):
        self.from_wire= from_wire
        self._as_boolean = self.str_to_bool[from_wire.lower()]
        _debug(f'created')
        # if self.validate(boolish):
        #     self.as_boolean = self.json_bool_values[boolish]
        # if self.boolish_literal != self.boolish:
        #     _warning(f"case sensitive data passed, self.boolish_literal={self.boolish_literal}")

    @classmethod
    def validate(cls, from_wire: str) -> bool:
        _debug(f"from_wire={from_wire}")
        try:
            as_boolean = cls.str_to_bool[from_wire.lower()]
        except KeyError:
            raise SwaggerValidationError(f"Value={from_wire} not recognized as JsonBool")
        return isinstance(as_boolean, bool)

    def __bool__(self):
        return self.as_boolean

    @property
    def as_boolean(self):
        as_boolean = self.str_to_bool[self.from_wire.lower()]
        return as_boolean

    @property
    def as_wire(self):
        return self.from_wire

    @classmethod
    def bool_to_wire(cls, b):
        _bool_to_wire = 'true' if b else 'false'
        return _bool_to_wire

    @classmethod
    def str_to_python(cls, s):
        _str_to_python = cls.str_to_bool.get(s, False)
        return _str_to_python


json_bool_format = SwaggerFormat(
    # name of the format as used in the Swagger spec
    format='json-bool',

    # Callable to convert a python object to_wire representations
    to_wire=lambda json_bool_instance: json_bool_instance.as_wire,

    # Callable to convert a from_wire to a python object
    to_python=lambda s: JsonBool(s),

    # Callable to validate the cidr in string form
    validate=JsonBool.validate,
    description='Converts "true" and "false" to/from equivalent booleans.'
)
