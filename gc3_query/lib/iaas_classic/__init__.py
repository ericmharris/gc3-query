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

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)



class IaaSBase:

    def __init__(self, atoml_cfg: dict, http_client: RequestsClient):
        pass



    @property
    def api_spec(self) -> str:
        """Returns Open API spec"""
        pass
