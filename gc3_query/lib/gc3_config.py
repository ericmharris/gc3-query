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
from collections.abc import Iterable, MutableMapping, MutableSequence

################################################################################
## Third-Party Imports
from dataclasses import dataclass
from melddict import MeldDict

################################################################################
## Project Imports

from gc3_query.lib import *
from gc3_query import GC3_QUERY_HOME
from gc3_query.lib.atoml.atoml_config import ATomlConfig
from gc3_query.lib.base_collections import OrderedDictAttrBase, ListBase

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

# atoml_config_dir = GC3_QUERY_HOME.joinpath('etc/config')
# _debug(f"atoml_config_dir={atoml_config_dir}")
# at_config = ATomlConfig(directory_paths=atoml_config_dir)
# gc3_cfg = at_config.toml



class ConfigListBase(ListBase):

    def __init__(self, data=None):
        super().__init__()
        if isinstance(data, MutableSequence):
            for v in data:
                if isinstance(v, MutableSequence):
                    self.append(ConfigListBase(v))
                if isinstance(v, MutableMapping):
                    self.append(ConfigOrderedDictAttrBase(v))
                else:
                    self.append(v)


class ConfigOrderedDictAttrBase(OrderedDictAttrBase):

    def __init__(self, mapping):
        super().__init__()

        for k,v in mapping.items():
            if isinstance(v, MutableSequence):
                self[k] = ConfigListBase(v)
            if isinstance(v, MutableMapping):
                self[k] = ConfigOrderedDictAttrBase(v)
            else:
                self[k] = v


class GC3Config(ConfigOrderedDictAttrBase):

    def __init__(self):
        atoml_config_dir = GC3_QUERY_HOME.joinpath('etc/config')
        _debug(f"atoml_config_dir={atoml_config_dir}")
        at_config = ATomlConfig(directory_paths=atoml_config_dir)
        gc3_cfg = at_config.toml
        super().__init__(mapping=gc3_cfg)


gc3_cfg = GC3Config()





