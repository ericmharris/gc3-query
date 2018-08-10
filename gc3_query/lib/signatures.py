# -*- coding: utf-8 -*-

"""
#@Filename : signatures
#@Date : [8/10/2018 1:39 PM]
#@Poject: gc3-query
#@AUTHOR : emharris

~~~~~~~~~~~~~~~~

<DESCR SHORT>

<DESCR>
"""

################################################################################
## Standard Library Imports
import sys, os
import re

################################################################################
## Third-Party Imports
from dataclasses import dataclass, field

################################################################################
## Project Imports
from gc3_query.lib import *
from gc3_query.lib import gc3_cfg

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

re_version_numbers = re.compile('\d+')

@dataclass()
class GC3Type:

    name: str
    descr: str
    class_type: type
    class_name: str = field(init=False)

    def __post_init__(self):
        self.class_name = self.class_type.__name__




@dataclass(order=True)
class GC3VersionedType():


    name: str
    re_version_list: List[int] = field(init=False)
    descr: str
    class_type: type
    class_name: str = field(init=False)
    version: str

    def __post_init__(self):
        self.class_name = self.class_type.__name__
        re_version_list = re_version_numbers.findall(self.version)
        self.re_version_list = [int(i) for i in re_version_list]

