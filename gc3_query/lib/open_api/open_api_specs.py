# -*- coding: utf-8 -*-

"""
#@Filename : open_api_specs
#@Date : [8/9/2018 2:05 PM]
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

################################################################################
## Project Imports
from gc3_query.lib import *
from gc3_query.lib.base_collections import NestedOrderedDictAttrListBase
_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


class OpenApiSpecCatalog(NestedOrderedDictAttrListBase):

    def __init__(self, api_catalog_dir: Path, api_catalog_config: DictStrAny):
        self.api_catalog_dir = api_catalog_dir
        self.api_catalog_config = api_catalog_config
        api_specs: dict
        super().__init__(mapping=api_specs)
