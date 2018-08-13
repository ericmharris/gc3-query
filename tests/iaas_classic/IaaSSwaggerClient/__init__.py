# -*- coding: utf-8 -*-

"""
#@Filename : __init__.py
#@Date : [8/13/2018 1:27 PM]
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

################################################################################
## Project Imports
from gc3_query.lib import *
from gc3_query.lib import gc3_cfg

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)