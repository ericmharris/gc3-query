# -*- coding: utf-8 -*-

"""
#@Filename : sec_rules
#@Date : [8/8/2018 12:59 PM]
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

################################################################################
## Project Imports
from gc3_query.lib import *
from . import IaaSServiceBase
from .iaas_requests_http_client import IaaSRequestsHTTPClient

from gc3_query.lib import get_logging
_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


class SecRules(IaaSServiceBase):

    def __init__(self,
                 service_cfg: Dict[str, Any],
                 idm_cfg: Dict[str, Any],
                 http_client: Union[IaaSRequestsHTTPClient, None] = None,
                 from_url: Optional[bool] = False,
                 storage_delegates: Optional[List[str]]= None,
                 **kwargs: Dict[str, Any]):
        super().__init__(service_cfg=service_cfg,
                         idm_cfg=idm_cfg,
                         http_client=http_client,
                         from_url=from_url,
                         storage_delegates=storage_delegates,
                         **kwargs)
        _debug(f"{self.service_name} created using service_cfg: {self.service_cfg}")



    def get_all_sec_rules(self):
        http_future = self.service_operations.list_sec_rule(container=self.idm_root_container_name)
        # http_future = self.bravado_service_operations.listSecRule(container=self.idm_root_container_name)
        request_url = http_future.future.request.url
        service_response = http_future.response()
        result_json = service_response.incoming_response.json()
        return result_json