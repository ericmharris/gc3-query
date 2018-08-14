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
from functools import partialmethod, partial, total_ordering

################################################################################
## Third-Party Imports

from bravado.client import ResourceDecorator
from bravado.client import SwaggerClient
from bravado.swagger_model import load_file

################################################################################
## Project Imports
from gc3_query.lib import *
from gc3_query.lib import gc3_cfg
## TODO: either change or add a snake_case function for camelCase
from gc3_query.lib.iaas_classic.iaas_requests_http_client import IaaSRequestsHTTPClient
from gc3_query.lib.iaas_classic.iaas_swagger_client import IaaSSwaggerClient, BRAVADO_CONFIG
from gc3_query.lib.open_api.open_api_spec_catalog import OpenApiSpecCatalog
from gc3_query.lib.utils import camelcase_to_snake
from gc3_query.lib.base_collections import OrderedDictAttrBase
from gc3_query.lib.signatures import GC3VersionTypedMixin
from gc3_query.lib.open_api.swagger_formats import BooleanString, boolean_string


_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

API_SPECS_DIR = BASE_DIR.joinpath('lib/iaas_classic/api_specs')
MONGODB_MODELS_DIR = BASE_DIR.joinpath('lib/iaas_classic/models')


class IaaSServiceBase(GC3VersionTypedMixin):
    idm_cfg: Dict[str, Any]
    service_cfg: Dict[str, Any]
    from_url: bool

    def __init__(self,
                 service_cfg: Dict[str, Any],
                 idm_cfg: Dict[str, Any],
                 http_client: IaaSRequestsHTTPClient = None,
                 from_url: bool = False,
                 storage_delegates: List[str] = None,
                 **kwargs: Dict[str, Any]):
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
        self.kwargs = kwargs
        self.service_name = service_cfg['service_name']

        self.oapi_spec_catalog = OpenApiSpecCatalog(api_catalog_config=gc3_cfg.iaas_classic.open_api_spec_catalog,
                                                    services_config=gc3_cfg.iaas_classic.services,
                                                    idm_cfg=self.idm_cfg,
                                                    from_url=from_url)
        self.open_api_spec = self.oapi_spec_catalog[self.service_name]

        self.bravado_config = BRAVADO_CONFIG

        self.http_client = http_client if http_client else IaaSRequestsHTTPClient(idm_cfg=self.idm_cfg, skip_authentication=self.kwargs.get('skip_authentication', False))
        self.swagger_client = IaaSSwaggerClient.from_spec(spec_dict=self.open_api_spec.spec_dict,
                                                      origin_url=self.idm_cfg.rest_endpoint,
                                                      http_client=self.http_client,
                                                      config=BRAVADO_CONFIG
                                                      )

        # This is the container from Bravado.client (SwaggerClient module) that holds CallableOperation created using the spec
        self.bravado_service_operations = getattr(self.swagger_client, service_cfg['service_name'])

        # This is populated with the CallableOperations from service_resources but the names are converted
        # from camelCase to python/snake-case (eg. discover_root_instance vs. discoverRootInstance)
        #
        self.service_operations = self.populate_service_operations(
            service_operations=getattr(self.swagger_client, service_cfg['service_name']))

        ### TODO:
        # self.gc3_type = GC3VersionedType(name=__class__.__name__,
        #                                  descr="OpenApiSpec is a wrapper around bravado.Spec for Oracle Cloud.",
        #                                  class_type=__class__,
        #                                  version=self.spec_dict.version)

        _debug(f"{self.name} created")

    @property
    def spec_dict(self) -> str:
        """Returns Open API spec"""
        return self.open_api_spec.spec_dict

    @property
    def name(self):
        return self.service_name

    @property
    def version(self) -> Union[Dict[str, Any], None, str]:
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

    def populate_service_operations(self, service_operations: ResourceDecorator) -> OrderedDictAttrBase:
        """Return container of callable operations with names converted from camel to python/snake-case

        :param service_operations:
        :return:
        """
        so = OrderedDictAttrBase()
        for service_operation_name in dir(service_operations):
            so_camel_name = camelcase_to_snake(service_operation_name)
            service_operation = getattr(service_operations, service_operation_name)
            operation_headers = {"Accept": ','.join(service_operation.operation.produces),
                                 "Content-Type": ','.join(service_operation.operation.consumes)
                                 }
            # partial_service_operation = partial(service_operation, _request_options={"headers": {"Accept": "application/oracle-compute-v3+directory+json"}})
            partial_service_operation = partial(service_operation, _request_options={"headers": operation_headers})
            so[so_camel_name] = partial_service_operation
            so.__dict__[so_camel_name] = so[so_camel_name]
        return so

    def get_idm_user_container_name(self, cloud_username: str = None) -> str:
        """ Return Compute-identityDomain/ or Compute-identityDomain/{cloud_username}/  eg. 'Compute-587626604/eric.harris@oracle.com' for gc30003

        Specify /Compute-identityDomain/user/ to retrieve the names of objects that you can access. Specify /Compute-identityDomain/ to retrieve the names of containers that contain objects that you can access.

        :return:
        """
        if cloud_username:
            return f"Compute-{self.idm_cfg.service_instance_id}/{cloud_username}"
            # return  f"/Compute-{self.idm_cfg.service_instance_id}/{cloud_username}"
        else:
            return self.idm_user_container_name
            # return  f"/Compute-{self.idm_cfg.service_instance_id}/"

    @property
    def idm_container_name(self) -> str:
        """Return Compute-identityDomain/, eg. 'Compute-587626604/' for gc30003

        Specify /Compute-identityDomain/user/ to retrieve the names of objects that you can access. Specify /Compute-identityDomain/ to retrieve the names of containers that contain objects that you can access.

        :return:
        """
        return self.idm_root_container_name

    @property
    def idm_user_container_name(self) -> str:
        """Return Compute-identityDomain/user/, eg. 'Compute-587626604/eric.harris@oracle.com' for gc30003

        Specify /Compute-identityDomain/user/ to retrieve the names of objects that you can access. Specify /Compute-identityDomain/ to retrieve the names of containers that contain objects that you can access.

        :return:
        """
        # return self.get_idm_user_container_name(cloud_username=gc3_cfg.user.cloud_username)
        return f"{self.idm_root_container_name}/{gc3_cfg.user.cloud_username}"


    @property
    def idm_root_container_name(self) -> str:
        """Return IDM container name used in multi-part naming (eg. Compute-587626604)

        :return:
        """
        return f"Compute-{self.idm_cfg.service_instance_id}"



