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
    http_client_class = PaaSRequestsHTTPClient


    def __init__(self,
                 service_cfg: NestedOrderedDictAttrListBase,
                 idm_cfg: NestedOrderedDictAttrListBase,
                 http_client: Union[IaaSRequestsHTTPClient, None] = None,
                 from_url: Optional[bool] = False,
                 storage_delegates: Optional[List[str]] = None,
                 **kwargs: DictStrAny):
        super().__init__( service_cfg=service_cfg, idm_cfg=idm_cfg, http_client=http_client, from_url=from_url, storage_delegates=storage_delegates , **kwargs)
