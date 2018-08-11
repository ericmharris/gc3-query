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
from gc3_query.lib.open_api.open_api_spec import OpenApiSpec

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)



class OracleApiSpecOverlay(NestedOrderedDictAttrListBase):
    """A dict of updates that are applied to correct mistakes in a OpenApiSpec. (eg. spec_dict['schemes'] = ['https'])

    """

    def __init__(self, open_api_spec: OpenApiSpec, overlays_spec_dict: DictStrAny=None):
        super().__init__(mapping=overlays_spec_dict)
        self.open_api_spec = open_api_spec
        self['schemes'] = ['https']



    def overlay_spec_dict(self, spec_dict: DictStrAny) -> DictStrAny:
        """Return a copy of spec_dict with corrections applied/overlayed

        :param spec_dict:
        :return:
        """
        spec_dict_copy = deepcopy(spec_dict)
        return self.update(spec_dict_copy.update(self))




    def apply_overlays(self, overlay_spec_dict):
        """

        :param overlay_spec_dict:
        :return:
        """
