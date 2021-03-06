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
from copy import deepcopy

################################################################################
## Third-Party Imports

from bravado.requests_client import RequestsClient
from bravado.client import CallableOperation
################################################################################
## Project Imports

from gc3_query.lib.iaas_classic import *
from gc3_query.lib.open_api.service_responses import PaaSServiceResponse
from .paas_requests_http_client import PaaSRequestsHTTPClient
from gc3_query.lib.export_delegates.response_export import ResponseExport

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
                 export_delegates: Optional[List[str]] = None,
                 **kwargs: DictStrAny):
        super().__init__( service_cfg=service_cfg, idm_cfg=idm_cfg, http_client=http_client, from_url=from_url, export_delegates=export_delegates , **kwargs)
        _debug(f"{self.name} created")

    def _find_bravado_service_operations(self, swagger_client, service_cfg: NestedOrderedDictAttrListBase):
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
            service_operation: CallableOperation = getattr(bravado_service_operations, service_operation_name)
            # operation_headers = {"Accept": ','.join(service_operation.operation.produces),
            #                      "Content-Type": ','.join(service_operation.operation.consumes)
            #                      }
            operation_headers = {"Accept": ','.join(service_operation.operation.produces),
                                 "Content-Type": ','.join(service_operation.operation.consumes)
                                 }
            operation_headers.update(self.http_client.authentication_headers)
            # partial_service_operation = partial(service_operation, _request_options={"headers": {"Accept": "application/oracle-compute-v3+directory+json"}})
            partial_service_operation: CallableOperation = partial(service_operation, _request_options={"headers": operation_headers})
            so[so_camel_name] = partial_service_operation
            so.__dict__[so_camel_name] = so[so_camel_name]
        return so

    def dump(self, dumper_service_operation_name: str) -> BravadoResponse:
        # return super().dump()
        raise NotImplementedError('Must impliment in the child class')
        return service_response


