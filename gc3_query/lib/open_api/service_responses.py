# -*- coding: utf-8 -*-

"""
gc3-query.service_response    [8/24/2018 11:41 AM]
~~~~~~~~~~~~~~~~

<DESCR SHORT>

<DESCR>
"""

################################################################################
## Standard Library Imports
import sys, os

################################################################################
## Third-Party Imports
from dataclasses import dataclass, field
from bravado.response import BravadoResponseMetadata
from bravado.requests_client import RequestsResponseAdapter

################################################################################
## Project Imports
from gc3_query.lib import *

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


### TODO:  If it's possible, make the interface between any major component a SwaggerAPI defined service.  So,
###        data sent between cloud and us is a Swagger Service Call, and once we're done processing it, the data needs to be sent
###         to Mongo, the screen/stdout, excel, whatever ... that should use something like a Swagger/API interface too.
@dataclass
class ServiceResponse:
    results: List[Any]
    json_results: Dict
    metadata: BravadoResponseMetadata
    uses_models: bool
    bravado_config: Dict[str,any] = field(init=False)
    num_results: int = field(init=False)

    def __post_init__(self):
        self.bravado_config = gc3_cfg.BRAVADO_CONFIG
        self.num_results = len(self.results)

    def __len__(self):
        return self.num_results


@dataclass
class PaaSServiceResponse(ServiceResponse):
    pass

@dataclass
class IaaSServiceResponse(ServiceResponse):
    pass
