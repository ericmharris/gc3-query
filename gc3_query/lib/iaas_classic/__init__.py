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
import sys, os

################################################################################
## Third-Party Imports
from dataclasses import dataclass
from bravado.requests_client import RequestsClient
from bravado.client import SwaggerClient

################################################################################
## Project Imports
from gc3_query.lib import *
from gc3_query.lib import gc3_cfg
## TODO: either change or add a snake_case function for camelCase
from gc3_query.lib.util import camelcase_to_snake
from gc3_query.lib.iaas_classic.requests_client import IaaSRequestsClient

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)



class IaaSServiceBase:

    def __init__(self, service_cfg: Dict[str,Any], idm_cfg: Dict[str,Any], **kwargs: Dict[str,Any]):
        self.service_cfg = service_cfg
        self.idm_cfg = idm_cfg
        self.kwargs = kwargs
        self._service_name = service_cfg['service_name']
        self.http_client = IaaSRequestsClient(idm_cfg=self.idm_cfg, skip_authentication=self.kwargs.get('skip_authentication', False))


    @property
    def api_spec(self) -> str:
        """Returns Open API spec"""
        pass
