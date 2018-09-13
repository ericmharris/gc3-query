# -*- coding: utf-8 -*-

"""
gc3-query.sec_ip_list_model    [9/12/2018 12:25 PM]
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
from . import *
_debug, _info, _warning, _error, _critical = get_logging(name=__name__)



class SecIPListFormatModel(DynamicEmbeddedDocument):
    """
    """
    name = StringField()
    object_name = StringField()
    object_type = StringField()

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        _debug(f"{self.__class__.__name__}.__init__(args={args}, values={values}):")
