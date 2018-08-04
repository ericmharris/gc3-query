# -*- coding: utf-8 -*-

"""
#@Filename : instances
#@Date : [7/30/2018 9:25 AM]
#@Poject: gc3-query
#@AUTHOR : emharris

~~~~~~~~~~~~~~~~

<DESCR SHORT>

<DESCR>
"""

################################################################################
## Standard Library Imports
import sys, os
from functools import lru_cache

################################################################################
## Third-Party Imports
from dataclasses import dataclass
from bravado.requests_client import RequestsClient
from bravado.client import SwaggerClient

################################################################################
## Project Imports
from gc3_query.lib import *
from gc3_query.lib import gc3_cfg
from . import IaaSServiceBase
from .iaas_requests_http_client import IaaSRequestsHTTPClient


_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

class Instances(IaaSServiceBase):

    service_name = 'Instances'

    def __init__(self, service_cfg: Dict[str, Any], idm_cfg: Dict[str, Any], http_client: IaaSRequestsHTTPClient=None, **kwargs: Dict[
        str, Any]):
        super().__init__(service_cfg, idm_cfg, **kwargs)
        _debug(f"{self.service_name} created using service_cfg: {self.service_cfg}")



    def get_instance_name(self, name: str, swagger_client_config: DictStrAny = None) -> DictStrAny:
        pass



    # TODO:  need to be able to override call configuration
    # swagger_client_config = {'validate_responses': True,
    #           'validate_requests': True,
    #           'validate_swagger_spec': True,
    #           'use_models': True,
    #           'include_missing_properties': True,
    #           'default_type_to_object': False,
    #           'internally_dereference_refs': False,
    #           'also_return_response': True}
    def get_instance_details(self, name: str, swagger_client_config: DictStrAny = None) -> DictStrAny:
        """

        :return:
        """
        pass


