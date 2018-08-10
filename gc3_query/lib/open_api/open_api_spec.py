# -*- coding: utf-8 -*-

"""
#@Filename : open_api_spec
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
from copy import deepcopy

################################################################################
## Third-Party Imports
from dataclasses import dataclass
from bravado_core.spec import Spec
from bravado.swagger_model import load_file, load_url


################################################################################
## Project Imports
from gc3_query.lib import *
from gc3_query.lib.base_collections import NestedOrderedDictAttrListBase

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)





class OpenApiSpec():

    def __init__(self,  api_catalog_config: DictStrAny, service_cfg: Dict[str, Any], from_url:bool = False, **kwargs):
        self.api_catalog_config = api_catalog_config
        self.service_cfg = service_cfg
        self.name = service_cfg.name
        self.kwargs = kwargs
        self.rest_endpoint = kwargs.get('rest_endpoint', None)

        self.spec_file_path = OPEN_API_CATALOG_DIR.joinpath(api_catalog_config.api_catalog_name).joinpath(service_cfg.service_name)
        self._spec_dict = self.load_spec(from_url=from_url)
        self._api_spec = self.create_api_spec(spec_dict=self._spec_dict)
        self.api_spec = NestedOrderedDictAttrListBase(mapping=self._api_spec)


    def load_spec(self, from_url:bool) -> DictStrAny:
        if from_url:
            spec_url = f"{self.service_cfg.spec_furl}".format_map(self.service_cfg)
            _debug(f"spec_url={spec_url}")
            spec_dict: dict = load_url(spec_url=spec_url)
            self.from_url = True
        else:
            spec_file_path = str(self.spec_file_path)
            spec_dict: dict = load_file(spec_file=spec_file_path)
            self.from_url = False
        return spec_dict


    def create_api_spec(self, spec_dict: DictStrAny) -> DictStrAny:
        """Returns a new spec_dict that sucks less

        :param spec_dict:
        :return:
        """
        spec_dict = deepcopy(spec_dict)
        spec_dict['schemes'] = ['https']
        return spec_dict


    def get_spec(self, rest_endpoint: Union[str, None] = None) -> Spec:
        rest_endpoint = rest_endpoint if rest_endpoint else self.rest_endpoint
        if not rest_endpoint:
            raise RuntimeError("rest_endpoint not provided in either method call or in **wkargs={self.kwargs}")
        core_spec: Spec = Spec(spec_dict=self._api_spec, origin_url=rest_endpoint, http_client=None, config=gc3_cfg.swagger_client_config)
        return core_spec

