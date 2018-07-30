# -*- coding: utf-8 -*-

"""
#@Filename : instances
#@Date : [7/30/2018 9:25 AM]
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
from . import IaaSServiceBase


_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

class Instances(IaaSServiceBase):

    service_name = 'Instances'

    def __init__(self, service_cfg: Dict[str, Any], idm_cfg: Dict[str, Any]):
        super().__init__(service_cfg, idm_cfg)


