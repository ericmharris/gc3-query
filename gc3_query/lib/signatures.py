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
import re
from functools import total_ordering

################################################################################
## Third-Party Imports
from dataclasses import dataclass, field

################################################################################
## Project Imports

from gc3_query.lib import *
from gc3_query.lib import get_logging
_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

re_version_numbers = re.compile(r'\d+')


@dataclass(order=True)
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


class GC3TypedMixin:
    """Mixin allows for __eq__ with any class providing name and descr

    """

    @property
    def gc3_type(self):
        gc3_type = GC3Type(name=self.name,
                           descr=self.descr,
                           class_type=self.__class__)
        return gc3_type

    def __eq__(self, other):
        return self.gc3_type == other.gc3_type


@total_ordering
class GC3VersionTypedMixin:
    """Mixin allows for __eq__ with any class providing name, descr, and version

    """

    @property
    def gc3_type(self):
        gc3_type = GC3Type(name=self.name,
                           descr=self.descr,
                           class_type=self.__class__)
        return gc3_type

    @property
    def gc3_ver_type(self):
        gc3_ver_type = GC3VersionedType(name=self.name,
                                        descr=self.descr,
                                        class_type=self.__class__,
                                        version=self.version)
        return gc3_ver_type

    def __eq__(self, other):
        is_eq = self.gc3_ver_type == other.gc3_ver_type
        return is_eq

    def __gt__(self, other):
        is_gt = self.gc3_ver_type > other.gc3_ver_type
        return is_gt
