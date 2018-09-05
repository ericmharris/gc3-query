# -*- coding: utf-8 -*-

"""
#@Filename : IPReservations
#@Date : [8/14/2018 2:24 PM]
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
from dataclasses import dataclass

################################################################################
## Project Imports
from gc3_query.lib import *
from . import IaaSServiceBase
from .iaas_requests_http_client import IaaSRequestsHTTPClient

from gc3_query.lib import get_logging
_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


class IPReservations(IaaSServiceBase):

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




    def get_all_ip_reservations(self):
        """
    d = dict(
        account='/Compute-587626604/default',
        ip='129.150.219.3',
        name='/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-soar-d02-dbcs/db_1/vm-1/ipreservation',
        parentpool='/oracle/public/ippool',
        permanent=True,
        quota=None,
        tags=[],
        uri='https://compute.uscom-central-1.oraclecloud.com/ip/reservation/Compute-587626604/eric.harris%40oracle.com/dbaas/gc3-naac-soar-d02-dbcs/db_1/vm-1/ipreservation',
        used=True)

        :return:
        """
        container = f"{self.idm_container_name}"
        http_future = self.service_operations.list_ip_reservation(container=container)
        # http_future = self.service_operations.list_ip_reservation(container=self.idm_root_container_name)
        # http_future = self.bravado_service_operations.listSecRule(container=self.idm_root_container_name)
        request_url = http_future.future.request.url
        service_response = http_future.response()
        # result_json = service_response.incoming_response.json()
        return service_response.resultging(name=__name__)
