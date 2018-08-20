# -*- coding: utf-8 -*-

"""
#@Filename : IPAddressReservations
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

################################################################################
## Project Imports
from gc3_query.lib import *
from . import IaaSServiceBase
from .iaas_requests_http_client import IaaSRequestsHTTPClient

from gc3_query.lib import get_logging
_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


class IPAddressReservations(IaaSServiceBase):

    def __init__(self, service_cfg: Dict[str, Any], idm_cfg: Dict[str, Any], http_client: IaaSRequestsHTTPClient = None,
                 from_url: bool = False, storage_delegates: List[str] = None, **kwargs: Dict[str, Any]):
        super().__init__(service_cfg=service_cfg,
                         idm_cfg=idm_cfg,
                         http_client=http_client,
                         from_url=from_url,
                         storage_delegates=storage_delegates,
                         **kwargs)
        _debug(f"{self.service_name} created using service_cfg: {self.service_cfg}")



from gc3_query.lib import get_logging
_debug, _info, _warning, _error, _critical = get_logging(name=__name__)