# -*- coding: utf-8 -*-

"""
#@Filename : gc3_config
#@Date : [7/29/2018 12:13 PM]
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
from dataclasses import dataclass
from melddict import MeldDict

################################################################################
## Project Imports

from gc3_query.lib import *
from gc3_query import GC3_QUERY_HOME
from gc3_query.lib.atoml.atoml_config import ATomlConfig

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

atoml_config_dir = GC3_QUERY_HOME.joinpath('etc/config')
_debug(f"atoml_config_dir={atoml_config_dir}")
at_config = ATomlConfig(directory_paths=atoml_config_dir)
gc3_cfg = at_config.toml


