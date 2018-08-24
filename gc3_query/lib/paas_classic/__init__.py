# -*- coding: utf-8 -*-

"""
#@Filename : __init__.py
#@Date : [8/20/2018 10:10 AM]
#@Poject: gc3-query
#@AUTHOR : emharris

~~~~~~~~~~~~~~~~

<DESCR SHORT>

<DESCR>
"""

################################################################################
## Standard Library Imports

################################################################################
## Third-Party Imports

from bravado.requests_client import RequestsClient

################################################################################
## Project Imports

from gc3_query.lib.iaas_classic import *
from .paas_requests_http_client import PaaSRequestsHTTPClient

from gc3_query.lib import get_logging
_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

class PaaSServiceBase(IaaSServiceBase):
    open_api_specs_cfg: GC3Config = gc3_cfg.paas_classic.open_api_specs
    http_client_class = PaaSRequestsHTTPClient


    def __init__(self,
                 service_cfg: NestedOrderedDictAttrListBase,
                 idm_cfg: NestedOrderedDictAttrListBase,
                 http_client: Union[IaaSRequestsHTTPClient, None] = None,
                 from_url: Optional[bool] = False,
                 storage_delegates: Optional[List[str]] = None,
                 **kwargs: DictStrAny):
        super().__init__( service_cfg=service_cfg, idm_cfg=idm_cfg, http_client=http_client, from_url=from_url, storage_delegates=storage_delegates , **kwargs)
        _debug(f"{self.name} created")

    def get_bravado_service_operations(self, swagger_client, service_cfg: NestedOrderedDictAttrListBase):
        resource_decorator_name = dir(swagger_client).pop() if dir(swagger_client) else None
        if not resource_decorator_name:
            raise RuntimeError(f"Failed to find resource_decorator_name for {self}")
        bravado_service_operations = getattr(swagger_client, resource_decorator_name)
        return bravado_service_operations

    def populate_service_operations(self, bravado_service_operations: ResourceDecorator) -> OrderedDictAttrBase:
        """Return container of callable operations with names converted from camel to python/snake-case

        :param bravado_service_operations:
        :return:
        """
        so = OrderedDictAttrBase()
        for service_operation_name in dir(bravado_service_operations):
            so_camel_name = camelcase_to_snake(service_operation_name)
            service_operation = getattr(bravado_service_operations, service_operation_name)
            operation_headers = {"Accept": ','.join(service_operation.operation.produces),
                                 "Content-Type": ','.join(service_operation.operation.consumes)
                                 }
            # partial_service_operation = partial(service_operation, _request_options={"headers": {"Accept": "application/oracle-compute-v3+directory+json"}})
            partial_service_operation = partial(service_operation, _request_options={"headers": operation_headers})
            so[so_camel_name] = partial_service_operation
            so.__dict__[so_camel_name] = so[so_camel_name]
        return so