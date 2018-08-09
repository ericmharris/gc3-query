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

from .open_api_spec import OpenApiSpec

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


class OpenApiSpecCatalog(NestedOrderedDictAttrListBase):

    def __init__(self, api_catalog_config: DictStrAny, services_config: Dict[str, Any], from_url: bool = False):
        super().__init__()
        self.api_catalog_name = api_catalog_config.api_catalog_name
        spec_catalog_path = OPEN_API_CATALOG_DIR.joinpath(api_catalog_config.api_catalog_name)

        for service_cfg in services_config.values():
            open_api_spec = OpenApiSpec(api_catalog_config=api_catalog_config, service_cfg=service_cfg, from_url=from_url)
            _debug(f"Loaded service={open_api_spec.name}")
            self[open_api_spec.name] = open_api_spec




