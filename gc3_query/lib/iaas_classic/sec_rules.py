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
import sys, os
from functools import lru_cache

################################################################################
## Third-Party Imports
from dataclasses import dataclass
from bravado.requests_client import RequestsClient
from bravado.client import SwaggerClient

################################################################################
## Project Imports
from gc3_query.lib import *
from gc3_query.lib import gc3_cfg
from . import IaaSServiceBase
from gc3_query.lib.iaas_classic.iaas_responses import IaaSServiceResponse
from .iaas_requests_http_client import IaaSRequestsHTTPClient
from gc3_query.lib.base_collections import NestedOrderedDictAttrListBase

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


class SecRules(IaaSServiceBase):
    service_name = 'SecRules'

    def __init__(self,
                 service_cfg: Dict[str, Any],
                 idm_cfg: Dict[str, Any],
                 http_client: IaaSRequestsHTTPClient = None,
                 from_url: bool = False,
                 **kwargs: Dict[str, Any]):
        super().__init__(service_cfg=service_cfg,
                         idm_cfg=idm_cfg,
                         http_client=http_client,
                         from_url=from_url,
                         **kwargs)
        _debug(f"{self.service_name} created using service_cfg: {self.service_cfg}")