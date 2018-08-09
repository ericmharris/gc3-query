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
    service_name = 'Instances'

    def __init__(self, service_cfg: Dict[str, Any], idm_cfg: Dict[str, Any], http_client: IaaSRequestsHTTPClient = None,
                 from_url: bool = False, storage_delegates: List[str] = None, **kwargs: Dict[str, Any]):
        super().__init__(service_cfg=service_cfg,
                         idm_cfg=idm_cfg,
                         http_client=http_client,
                         from_url=from_url,
                         storage_delegates=storage_delegates,
                         **kwargs)
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

    # @property
    # @lru_cache(maxsize=1)
    # def idm_root_container_name(self) -> str:
    #     """
    #
    #     :return:
    #     """
    #     http_future = self.bravado_service_operations.discoverRootInstance(
    #         _request_options={"headers": {"Accept": "application/oracle-compute-v3+directory+json"}})
    #     request_url = http_future.future.request.url
    #     service_response = http_future.response()
    #     # result = service_response.result
    #     # http_response = service_response.incoming_response
    #     root_instance_result = service_response.incoming_response.json().get('result', None)
    #     root_instance_name = root_instance_result[0] if root_instance_result else None
    #     return root_instance_name.replace('/', '')

    # @property
    # def idm_root_container_name(self) -> str:
    #     """
    #
    #     :return:
    #     """
    #     http_future = self.bravado_service_operations.discoverRootInstance(
    #         _request_options={"headers": {"Accept": "application/oracle-compute-v3+directory+json"}})
    #     request_url = http_future.future.request.url
    #     service_response = http_future.response()
    #     # result = service_response.result
    #     # http_response = service_response.incoming_response
    #     root_instance_result = service_response.incoming_response.json().get('result', None)
    #     root_instance_name = root_instance_result[0] if root_instance_result else None
    #     if root_instance_name[-1] is '/':
    #         return root_instance_name[0:-1]
    #     return root_instance_name


    def get_all_instances_details(self) -> List[IaaSServiceResponse]:
        root_container_name = self.idm_root_container_name
        http_future = self.bravado_service_operations.listInstance(container=self.idm_root_container_name)
        service_response = http_future.response()
        result_json = service_response.incoming_response.json().get('result', None)
        return


