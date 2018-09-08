# -*- coding: utf-8 -*-

"""
gc3-query.OracleEmailModel    [9/8/2018 1:12 PM]
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
from gc3_query.lib import *
#from gc3_query.lib.gc3logging import get_logging
from . import *

from gc3_query.lib import get_logging
_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


class OracleEmailFormatModel(EmbeddedDocument):
    pass