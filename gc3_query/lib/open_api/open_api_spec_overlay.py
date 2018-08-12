# -*- coding: utf-8 -*-

"""
#@Filename : spec_overlays
#@Date : [8/11/2018 12:06 PM]
#@Poject: gc3-query
#@AUTHOR : emharris

~~~~~~~~~~~~~~~~

<DESCR SHORT>

<DESCR>
"""

################################################################################
## Standard Library Imports
import sys, os
from copy import deepcopy

################################################################################
## Third-Party Imports
from dataclasses import dataclass, field

################################################################################
## Project Imports
from gc3_query.lib import *
from gc3_query.lib import gc3_cfg
from gc3_query.lib.base_collections import NestedOrderedDictAttrListBase

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

class OpenApiSpecOverlay():
    """A dict of updates that are applied to correct mistakes in a OpenApiSpec. (eg. spec_dict['schemes'] = ['https'])

    """

    def __init__(self, open_api_spec: 'OpenApiSpec', overlays_spec_dict: DictStrAny=None):
        self.open_api_spec = open_api_spec
        self.spec_dir_path = OPEN_API_CATALOG_DIR.joinpath(open_api_spec.api_catalog_config.api_catalog_name).joinpath(open_api_spec.service_cfg.service_name)
        self.spec_overlay_file_path = self.spec_dir_path.joinpath(f"{open_api_spec.service_cfg.service_name}_overlay.json")
        self.overlays_spec_dict = NestedOrderedDictAttrListBase(mapping=overlays_spec_dict)
        self.overlays_spec_dict['schemes'] = ['https']


    def apply_overlays(self, overlay_spec_dict):
        """

        :param overlay_spec_dict:
        :return:
        """
        pass
