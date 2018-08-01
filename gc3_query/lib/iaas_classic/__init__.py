# -*- coding: utf-8 -*-

"""
#@Filename : __init__.py
#@Date : [7/29/2018 11:25 AM]
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
import bravado
from bravado.requests_client import RequestsClient
from bravado.client import SwaggerClient
from bravado.client import SwaggerClient, ResourceDecorator
from bravado.client import SwaggerClient, CallableOperation
from gc3_query.lib.bravado.requests_client import OCRequestsClient
from bravado.requests_client import RequestsResponseAdapter
from bravado.swagger_model import load_file
from bravado_core.exception import MatchingResponseNotFound
from bravado.exception import HTTPBadRequest
from bravado.http_future import HttpFuture

################################################################################
## Project Imports
from gc3_query.lib import *
from gc3_query.lib import gc3_cfg
## TODO: either change or add a snake_case function for camelCase
from gc3_query.lib.utils import camelcase_to_snake
from gc3_query.lib.iaas_classic.requests_client import IaaSRequestsHTTPClient
from gc3_query.lib.utils import camelcase_to_snake
from gc3_query.lib.base_collections import OrderedDictAttrBase


_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

API_SPEC_DIR = BASE_DIR.joinpath('lib/iaas_classic/api_specs')


class IaaSServiceBase:

    def __init__(self, service_cfg: Dict[str,Any], idm_cfg: Dict[str,Any], http_client: IaaSRequestsHTTPClient=None, **kwargs: Dict[str, Any]):
        """


        :param service_cfg:
        :param idm_cfg:
        :param kwargs:
        """
        self.service_cfg = service_cfg
        self.idm_cfg = idm_cfg
        self.kwargs = kwargs
        self._service_name = service_cfg['service_name']
        self.http_client = http_client if http_client else IaaSRequestsHTTPClient(idm_cfg=self.idm_cfg,
                                                                                  skip_authentication=self.kwargs.get(
            'skip_authentication', False))

        # swagger_client = SwaggerClient.from_url(spec_url=spec_file_uri, http_client=requests_client, config={'also_return_response': True})

        # .../site-packages/bravado_core/spec.py:40
        self.swagger_client_config = dict(gc3_cfg.iaas_classic.iaas_service_client_config)
        self.swagger_client = SwaggerClient.from_spec(spec_dict=self.api_spec,
                                                 origin_url=self.idm_cfg.rest_endpoint,
                                                 http_client=self.http_client,
                                                 config=self.swagger_client_config)

        # This is the container from Bravado.client (SwaggerClient module) that holds CallableOperation created using the spec
        self.bravado_service_operations = getattr(self.swagger_client, service_cfg['service_name'])

        # This is populated with the CallableOperations from service_resources but the names are converted
        # from camelCase to python/snake-case (eg. discover_root_instance vs. discoverRootInstance)
        #
        self.service_operations = self.populate_service_operations(service_operations=getattr(self.swagger_client, service_cfg['service_name']))

    @property
    def api_spec(self) -> str:
        """Returns Open API spec"""
        spec_file_path = API_SPEC_DIR.joinpath(self.service_cfg.spec_file)
        spec_dict = load_file(spec_file_path)
        spec_dict['schemes'].append('https')
        return spec_dict


    def populate_service_operations(self, service_operations: ResourceDecorator) -> OrderedDictAttrBase:
        """Return container of callable operations with names converted from camel to python/snake-case

        :param service_operations:
        :return:
        """
        so = OrderedDictAttrBase()
        for service_operation_name in dir(service_operations):
            so_camel_name = camelcase_to_snake(service_operation_name)
            so[so_camel_name] =  getattr(service_operations, service_operation_name)
            so.__dict__[so_camel_name] = so[so_camel_name]
        return so


    def get_idm_container_name(self, cloud_username:str = None) -> str:
        """ Return /Compute-identityDomain/ or /Compute-identityDomain/{cloud_username}/  eg. '/Compute-587626604/eric.harris@oracle.com' for gc30003

        Specify /Compute-identityDomain/user/ to retrieve the names of objects that you can access. Specify /Compute-identityDomain/ to retrieve the names of containers that contain objects that you can access.

        :return:
        """
        if cloud_username:
            return  f"/Compute-{self.idm_cfg.service_instance_id}/{cloud_username}/"
        else:
            return  f"/Compute-{self.idm_cfg.service_instance_id}/"

    @property
    def idm_container_name(self) -> str:
        """Return /Compute-identityDomain/, eg. '/Compute-587626604/' for gc30003

        Specify /Compute-identityDomain/user/ to retrieve the names of objects that you can access. Specify /Compute-identityDomain/ to retrieve the names of containers that contain objects that you can access.

        :return:
        """
        return self.get_idm_container_name()


    @property
    def idm_user_container_name(self) -> str:
        """Return /Compute-identityDomain/user/, eg. '/Compute-587626604/eric.harris@oracle.com' for gc30003

        Specify /Compute-identityDomain/user/ to retrieve the names of objects that you can access. Specify /Compute-identityDomain/ to retrieve the names of containers that contain objects that you can access.

        :return:
        """
        return self.get_idm_container_name(cloud_username=gc3_cfg.user.cloud_username)

