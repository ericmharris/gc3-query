# -*- coding: utf-8 -*-

"""
gc3-query.export_delegate_base    [8/23/2018 5:26 PM]
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


@dataclass
class ResponseExport:
    result: Any
    results: List[Any]
    metadata: BravadoResponseMetadata
    incoming_response: RequestsResponseAdapter
    uses_models: bool
    bravado_config: Dict[str,any] = field(init=False)
    num_results: int = field(init=False)
    raw_result: str = field(init=False)


    def __post_init__(self):
        pass
