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
from gc3_query.lib.iaas_classic.iaas_responses import IaaSServiceResponse
from .iaas_requests_http_client import IaaSRequestsHTTPClient
from gc3_query.lib.base_collections import NestedOrderedDictAttrListBase

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


class Instances(IaaSServiceBase):

    def __init__(self, service_cfg: Dict[str, Any], idm_cfg: Dict[str, Any], http_client: IaaSRequestsHTTPClient = None,
                 from_url: bool = False, storage_delegates: List[str] = None, **kwargs: Dict[str, Any]):
        super().__init__(service_cfg=service_cfg,
                         idm_cfg=idm_cfg,
                         http_client=http_client,
                         from_url=from_url,
                         storage_delegates=storage_delegates,
                         **kwargs)
        _debug(f"{self.service_name} created using service_cfg: {self.service_cfg}")


    def get_instance_details(self, name: str, swagger_client_config: DictStrAny = None) -> IaaSServiceResponse:
        """

        :return:
        """
        http_future = self.bravado_service_operations.getInstance(name=name)
        request_url = http_future.future.request.url
        service_response = http_future.response()
        # result = service_response.result
        # http_response = service_response.incoming_response
        instance_details = IaaSServiceResponse(service_response=service_response)
        return instance_details

