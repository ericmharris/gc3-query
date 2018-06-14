# -*- coding: utf-8 -*-

"""
#@Filename : gc3keygen
#@Date : [6/14/2018 11:37 AM]
#@Poject: gc3-query
#@AUTHOR : eharris

~~~~~~~~~~~~~~~~

<DESCR SHORT>

<DESCR>
"""

################################################################################
## Standard Library Imports
import sys, os

################################################################################
## Third-Party Imports
import click
from dataclasses import dataclass


################################################################################
## Project Imports
from gc3_query import __version__
from gc3_query.lib import *
from gc3_query.lib.gc3keygen import *

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)








