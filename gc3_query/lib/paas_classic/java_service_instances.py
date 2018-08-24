# -*- coding: utf-8 -*-

"""
gc3-query.java_service_instances    [8/24/2018 10:20 AM]
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
from . import *

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

class JavaServiceInstances(PaaSServiceBase):

    def __init__(self,
                 service_cfg: NestedOrderedDictAttrListBase,
                 idm_cfg: NestedOrderedDictAttrListBase,
                 http_client: Union[IaaSRequestsHTTPClient, None] = None,
                 from_url: Optional[bool] = False,
                 export_delegates: Optional[List[str]] = None,
                 **kwargs: DictStrAny):
        super().__init__(service_cfg=service_cfg, idm_cfg=idm_cfg, http_client=http_client, from_url=from_url, export_delegates=export_delegates, **kwargs)
        _debug(f"{self.name} created")

    def get_all_domain_data(self):
        """

        :return:
        """
        http_future = self.service_operations.get_domain(identityDomainId=self.idm_cfg.name)
        service_response: BravadoResponse = http_future.response()
        result = service_response.result
        metadata: BravadoResponseMetadata = service_response.metadata
        domains = result['services']
        return domains