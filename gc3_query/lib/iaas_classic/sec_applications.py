# -*- coding: utf-8 -*-

"""
gc3-query.sec_applications    [9/4/2018 12:40 PM]
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

################################################################################
## Project Imports
from gc3_query.lib import *
from . import IaaSServiceBase
from .iaas_requests_http_client import IaaSRequestsHTTPClient

from gc3_query.lib import get_logging
_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


class SecApplications(IaaSServiceBase):

    def __init__(self,
                 service_cfg: Dict[str, Any],
                 idm_cfg: Dict[str, Any],
                 http_client: Union[IaaSRequestsHTTPClient, None] = None,
                 from_url: Optional[bool] = False,
                 export_delegates: Optional[List[str]]= None,
                 **kwargs: Dict[str, Any]):
        super().__init__(service_cfg=service_cfg,
                         idm_cfg=idm_cfg,
                         http_client=http_client,
                         from_url=from_url,
                         export_delegates=export_delegates,
                         **kwargs)
        _debug(f"{self.service_name} created using service_cfg: {self.service_cfg}")



    def get_all_sec_rules(self):
        container = f"{self.idm_container_name}/"
        http_future = self.service_operations.list_sec_rule(container=container)
        # http_future = self.service_operations.list_sec_rule(container=self.idm_root_container_name)
        # http_future = self.bravado_service_operations.listSecRule(container=self.idm_root_container_name)
        request_url = http_future.future.request.url
        service_response = http_future.response()
        # result_json = service_response.incoming_response.json()
        return service_response.resultging(name=__name__)