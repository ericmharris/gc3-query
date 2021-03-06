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
from functools import partial
from copy import deepcopy

################################################################################
## Third-Party Imports
from sortedcontainers import SortedDict

from bravado.client import ResourceDecorator
from bravado.response import  BravadoResponse, BravadoResponseMetadata
from bravado_core.spec import Spec
from bravado.requests_client import RequestsClient
from bravado.client import CallableOperation


################################################################################
## Project Imports
from gc3_query.lib import *
from gc3_query.lib import gc3_cfg
from gc3_query.lib.gc3_config import GC3Config
from gc3_query.lib.base_collections import OrderedDictAttrBase, NestedOrderedDictAttrListBase
## TODO: either change or add a snake_case function for camelCase
from gc3_query.lib.iaas_classic.iaas_requests_http_client import IaaSRequestsHTTPClient
from gc3_query.lib.iaas_classic.iaas_swagger_client import IaaSSwaggerClient
from gc3_query.lib.open_api.open_api_spec import OpenApiSpec
from gc3_query.lib.open_api.open_api_spec_catalog import OpenApiSpecCatalog
from gc3_query.lib.signatures import GC3VersionTypedMixin
from gc3_query.lib.util import camelcase_to_snake
from gc3_query.lib.export_delegates.response_export import ResponseExport
from gc3_query.lib.open_api.service_responses import IaaSServiceResponse
from gc3_query.lib.gc3_bravado import bravado_cfg

from gc3_query.lib import get_logging

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


class IaaSServiceBase(GC3VersionTypedMixin):
    idm_cfg: NestedOrderedDictAttrListBase
    service_cfg: NestedOrderedDictAttrListBase
    from_url: bool
    gc3_cfg: NestedOrderedDictAttrListBase
    open_api_specs_cfg: GC3Config = gc3_cfg.iaas_classic.open_api_specs
    http_client_class = IaaSRequestsHTTPClient

    def __init__(self,
                 service_cfg: NestedOrderedDictAttrListBase,
                 idm_cfg: NestedOrderedDictAttrListBase,
                 http_client: Union[IaaSRequestsHTTPClient, None] = None,
                 from_url: Optional[bool] = False,
                 export_delegates: Optional[List[str]] = None,
                 **kwargs: DictStrAny):
        """

        :param service_cfg:
        :param idm_cfg:
        :param http_client:
        :param from_url:
        :param kwargs:
        """
        self.from_url = from_url
        self.service_cfg = service_cfg
        self.idm_cfg = idm_cfg
        self.service_name = service_cfg['service_name']
        self.export_delegates = export_delegates

        # self.bravado_config: DictStrAny = gc3_cfg.bravado.client_config.as_dict()
        # self.bravado_config.update(gc3_cfg.bravado.core_config.as_dict())

        # self.bravado_config: DictStrAny = gc3_cfg.BRAVADO_CONFIG
        # from gc3_query.lib.gc3_bravado import bravado_cfg
        self.bravado_config: DictStrAny = bravado_cfg.BRAVADO_CONFIG

        if kwargs.get('spec_dict', False) and kwargs.get('swagger_spec', False):
            raise RuntimeError(f"Supplying both a spec_dict and swagger_spec not allowed")
        self.kwargs = {'swagger_spec': kwargs.get('swagger_spec', False),  # bravado_core.spec.Spec
                       'mock_version': kwargs.get('mock_version', False),  # Used for unit tests,
                       'skip_authentication': kwargs.get('skip_authentication', False),  # self.http_client won't authenticate against the IDM
                       'spec_dict': kwargs.get('spec_dict', False),  # Spec values
                       }
        self.kwargs.update(kwargs)

        # self.oapi_spec_catalog = OpenApiSpecCatalog(api_catalog_config=gc3_cfg.iaas_classic.open_api_spec_catalog,
        #                                             services_config=gc3_cfg.iaas_classic.services,
        #                                             idm_cfg=self.idm_cfg,
        #                                             from_url=from_url)
        # self.open_api_spec: OpenApiSpec = kwargs['swagger_spec'] if 'swagger_spec' in kwargs else self.oapi_spec_catalog[self.service_name]
        # self.open_api_spec: OpenApiSpec = self.oapi_spec_catalog[self.service_name]

        #### OpenApiSpec init
        # gc3_config = GC3Config(atoml_config_dir=config_dir)
        # service_cfg = gc3_config.iaas_classic.services[service]
        # open_api_specs_cfg = gc3_config.iaas_classic.open_api_specs
        # idm_cfg = gc3_config.idm.domains.gc30003
        # # oapi_spec = OpenApiSpec(service_cfg=service_cfg, open_api_specs_cfg=api_catalog_config)
        # oapi_spec = OpenApiSpec(service_cfg=service_cfg, open_api_specs_cfg=open_api_specs_cfg, idm_cfg=idm_cfg)

        self.open_api_spec: OpenApiSpec = OpenApiSpec(service_cfg=self.service_cfg,
                                                      open_api_specs_cfg=self.open_api_specs_cfg,
                                                      idm_cfg=self.idm_cfg)

        self._spec_dict: DictStrAny = kwargs.get('spec_dict', False) or self.open_api_spec.spec_dict
        self._swagger_spec: Spec = kwargs.get('swagger_spec', None)

        self.http_client = http_client if http_client else self.http_client_class(idm_cfg=self.idm_cfg, skip_authentication=self.kwargs.get('skip_authentication', False))
        self.swagger_client = IaaSSwaggerClient.from_spec(spec_dict=self.spec_dict, http_client=self.http_client, config=self.bravado_config )

        # This is the container from Bravado.client (SwaggerClient module) that holds CallableOperation created using the spec
        # self.bravado_service_operations = getattr(self.swagger_client, service_cfg['service_name'])
        self.bravado_service_operations = self._find_bravado_service_operations(swagger_client=self.swagger_client, service_cfg=self.service_cfg)

        # This is populated with the CallableOperations from service_resources but the names are converted
        # from camelCase to python/snake-case (eg. discover_root_instance vs. discoverRootInstance)
        self.service_operations = self.populate_service_operations(bravado_service_operations=self.bravado_service_operations)

        ### TODO:
        # self.gc3_type = GC3VersionedType(name=__class__.__name__,
        #                                  descr="OpenApiSpec is a wrapper around bravado.Spec for Oracle Cloud.",
        #                                  class_type=__class__,
        #                                  version=self.spec_dict.version)

        _debug(f"{self.name} created")

    @property
    def spec_dict(self) -> DictStrAny:
        """Returns Open API spec"""
        return self._spec_dict

    # @property
    # def open_api_spec(self) -> Union[OpenApiSpec, Spec]:
    #     """Returns Open API spec"""
    #     return self.open_api_spec

    @property
    def swagger_spec(self) -> Spec:
        swagger_spec: Spec = self._swagger_spec if self._swagger_spec else self.open_api_spec.spec
        #### bravado_core.spec.Spec#client_spec_dict
        # Return a copy of spec_dict with x-scope metadata removed so that it
        #         is suitable for consumption by Swagger clients.
        client_spec_dict = swagger_spec.client_spec_dict
        return client_spec_dict

    @property
    def name(self):
        return self.service_name

    @property
    def version(self) -> Union[DictStrAny, None, str]:
        if self.kwargs.get('mock_version', False):
            return self.kwargs.get('mock_version')
        return self.spec_dict['info']['version']

    @property
    def description(self) -> str:
        return self.descr

    @property
    def descr(self) -> str:
        descr = self.spec_dict['info']['description']
        return descr

    @property
    def rest_endpoint(self):
        return self.open_api_spec.rest_endpoint

    def _find_bravado_service_operations(self, swagger_client, service_cfg: NestedOrderedDictAttrListBase):
        resource_decorator_name = dir(swagger_client).pop() if dir(swagger_client) else None
        if not resource_decorator_name:
            raise RuntimeError(f"Failed to find resource_decorator_name for {self}")
        bravado_service_operations = getattr(swagger_client, resource_decorator_name)
        return bravado_service_operations

    # def get_bravado_service_operations(self, swagger_client, service_cfg: NestedOrderedDictAttrListBase):
    #     bravado_service_operations = getattr(swagger_client, service_cfg['service_name'])
    #     return bravado_service_operations

    def populate_service_operations(self, bravado_service_operations: ResourceDecorator) -> OrderedDictAttrBase:
        """Return container of callable operations with names converted from camel to python/snake-case

        :param bravado_service_operations:
        :return:
        """
        so = OrderedDictAttrBase()
        for service_operation_name in dir(bravado_service_operations):
            so_camel_name = camelcase_to_snake(service_operation_name)
            service_operation: CallableOperation = getattr(bravado_service_operations, service_operation_name)

            ## Need to make sure 'application/json' is in the request or models will never work.
            ## TODO:  Move this to OpenAPI code
            if 'application/json' not in service_operation.operation.produces:
                service_operation.operation.produces.insert(0, 'application/json')

            operation_headers = {"Accept": ','.join(service_operation.operation.produces),
                                 "Content-Type": ','.join(service_operation.operation.consumes)
                                 }
            # partial_service_operation = partial(service_operation, _request_options={"headers": {"Accept": "application/oracle-compute-v3+directory+json"}})
            partial_service_operation: CallableOperation = partial(service_operation, _request_options={"headers": operation_headers})
            so[so_camel_name] = partial_service_operation
            so.__dict__[so_camel_name] = so[so_camel_name]
        return so



    def dump(self) -> BravadoResponse:
        container = f"{self.idm_container_name}/"
        for service_operation_name in self.service_operations:
            if service_operation_name.startswith('list'):
                dumper_service_operation = self.service_operations[service_operation_name]
                break
        # http_future = self.service_operations.list_instance(container=container)
        http_future = dumper_service_operation(container=container)
        request_url = http_future.future.request.url
        service_response = http_future.response()
        return service_response

    def dump_using_idm_name(self) -> BravadoResponse:
        container = f"Compute-{self.idm_cfg.name}/"
        for service_operation_name in self.service_operations:
            if service_operation_name.startswith('list'):
                dumper_service_operation = self.service_operations[service_operation_name]
                break
        # http_future = self.service_operations.list_instance(container=container)
        http_future = dumper_service_operation(container=container)
        request_url = http_future.future.request.url
        service_response = http_future.response()
        return service_response


    def get_idm_user_container_name(self, cloud_username: str = None) -> str:
        """ Return Compute-identityDomain/ or Compute-identityDomain/{cloud_username}/  eg. 'Compute-587626604/eric.harris@oracle.com' for gc30003

        Specify /Compute-identityDomain/user/ to retrieve the names of objects that you can access. Specify /Compute-identityDomain/ to retrieve the names of containers that contain objects that you can access.

        :return:
        """
        if cloud_username:
            return f"{self.idm_cfg.formal_name}/{cloud_username}"
            # return  f"/Compute-{self.idm_cfg.formal_name}/{cloud_username}"
        else:
            return self.idm_user_container_name
            # return  f"/Compute-{self.idm_cfg.formal_name}/"

    @property
    def idm_container_name(self) -> str:
        """Return Compute-identityDomain/, eg. 'Compute-587626604/' for gc30003

        Specify /Compute-identityDomain/user/ to retrieve the names of objects that you can access. Specify /Compute-identityDomain/ to retrieve the names of containers that contain objects that you can access.
        # /Compute-identityDomainName/username
        # /Compute-serviceInstanceID/username

        :return:
        """
        return self.idm_root_container_name

    @property
    def idm_user_container_name(self) -> str:
        """Return Compute-identityDomain/user/, eg. 'Compute-587626604/eric.harris@oracle.com' for gc30003

        Specify /Compute-identityDomain/user/ to retrieve the names of objects that you can access. Specify /Compute-identityDomain/ to retrieve the names of containers that contain objects that you can access.
        # /Compute-identityDomainName/username
        # /Compute-serviceInstanceID/username

        :return:
        """
        # return self.get_idm_user_container_name(cloud_username=gc3_cfg.user.cloud_username)
        return f"{self.idm_root_container_name}/{gc3_cfg.user.cloud_username}"

    @property
    def idm_root_container_name(self) -> str:
        """Return IDM container name used in multi-part naming (eg. Compute-587626604)

        :return:
        """
        return f"{self.idm_cfg.formal_name}"
