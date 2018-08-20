# -*- coding: utf-8 -*-

"""
#@Filename : __init__.py
#@Date : [8/9/2018 12:52 PM]
#@Poject: gc3-query
#@AUTHOR : emharris

~~~~~~~~~~~~~~~~

<DESCR SHORT>

<DESCR>
"""

################################################################################
## Standard Library Imports
import sys, os
import json

################################################################################
## Third-Party Imports
from pathlib import Path

from dataclasses import dataclass




################################################################################
## Project Imports
from gc3_query import OPEN_API_CATALOG_DIR, API_SPECS_DIR
from gc3_query.lib import *
from gc3_query.lib.gc3logging import get_logging

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

