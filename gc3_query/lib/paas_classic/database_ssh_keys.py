# -*- coding: utf-8 -*-

"""
gc3-query.database_ssh_keys    [9/8/2018 11:44 AM]
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
from paas_classic import PaaSServiceBase
from . import *
_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


dbcs_ssh_key = dict(
    componentType='DB',
    computeKeyName='/Compute-587626604/dhiru.vallabhbhai@oracle.com/dbaas.gc3ntagocsd801.DB.ora_user',
    credName='vmspublickey',
    credType='SSH',
    description='Service user ssh public key which can be used to access the service VM instances',
    identityDomain='gc30003',
    lastUpdateMessage='newly created',
    lastUpdateStatus='success',
    lastUpdateTime='2018-02-13T18:52:10.063+0000',
    osUserName='opc',
    parentType='SERVICE',
    publicKey=
    'ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAgEAwSv6Q9B0MRXvoZQj+vKE829fAiUajPcnhSP4VX1btzsgO7i5BjJtKtWOnA3rlCQc0BbskHDUPO1bPJqfYEP1y9N4EmQSAMwWUSLviMe8FXD19nWBZAuG83c1qek+Q2UdR5HU1lCTb1TG7onZ8H4nCbbIB4zYTld+dMD9cgPwwHtV9FxOWPzB8GIfVo2C+sygecz85WLxtmBZVd/QHEvF6VctnAfaiW7+w68ho5tTTdOz1jKL/sGCqxNj7TuR27w4CQIpsitDCT/zFJNnEI8rUHvmrmfW5xO5Ik0893IRaKuu0w7knV/dSI+wqWYbDCGIavLhQL591iGFDf7vhSWvexlg+SEij06QBaXUP6sNuLOCE9fq3qPVYDwMLaAlw4WFmQC1ENNASPaHNREyg7Yh6yr5i/ozyHgS8wPCs7ur1Z+ukBt9x5592LELF8YPisw31u7SaZAKvoRBj4pgAwzJ/kbIi/FwNJNGRz2o4UYgsEcbI3tX0q39q/x2PgEzDKjX7HwyrHTBnjQFpOBQkS0t8OBAByCXIO2MSufdiToKBV3Z+HBg8CLAoU+GMawoiyFdwyVLK7WY6U5iDELqkZep5XGEyoGcN7dKaICiwg7nNtEYTQlfzetDmKBdbEr/33Zr58wZBSg/HyodmVfxbUXu7hE14kyeNc4CbbFqFsvTjVM= rsa-key-20180207',
    serviceEntitlementId='587626608',
    serviceName='gc3ntagocsd801',
    serviceState='RUNNING',
    serviceType='DBaaS')

class DatabaseSSHKeys(PaaSServiceBase):

    def __init__(self,
                 service_cfg: NestedOrderedDictAttrListBase,
                 idm_cfg: NestedOrderedDictAttrListBase,
                 http_client: Union[IaaSRequestsHTTPClient, None] = None,
                 from_url: Optional[bool] = False,
                 export_delegates: Optional[List[str]] = None,
                 **kwargs: DictStrAny):
        """




        :param service_cfg:
        :param idm_cfg:
        :param http_client:
        :param from_url:
        :param export_delegates:
        :param kwargs:
        """
        super().__init__(service_cfg=service_cfg, idm_cfg=idm_cfg, http_client=http_client, from_url=from_url, export_delegates=export_delegates, **kwargs)
        _debug(f"{self.name} created")

    def get_all_domain_data(self):
        """

        :return:
        """
        http_future = self.service_operations.get_domain(identityDomainId=self.idm_cfg.name)
        service_response: BravadoResponse = http_future.response()
        metadata: BravadoResponseMetadata = service_response.metadata
        result = service_response.result
        results = service_response.result['services']
        json_result = service_response.incoming_response.json()
        json_results = json_result['services']
        pass_service_response = PaaSServiceResponse(results=results, json_results=json_results, metadata=metadata, uses_models=True)
        return pass_service_response

    def dump(self) -> BravadoResponse:
        http_future = self.service_operations.get_credentials(identityDomainId=self.idm_cfg.name)
        service_response: BravadoResponse = http_future.response()
        return service_response

