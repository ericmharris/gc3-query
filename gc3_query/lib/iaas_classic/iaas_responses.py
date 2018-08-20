# -*- coding: utf-8 -*-

"""
#@Filename : iaas_responses
#@Date : [8/6/2018 10:52 AM]
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

from bravado.response import BravadoResponseMetadata

################################################################################
## Project Imports
from gc3_query.lib import *
from gc3_query.lib.base_collections import NestedOrderedDictAttrListBase

from gc3_query.lib import get_logging
_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


class IaaSResponseMetadata(NestedOrderedDictAttrListBase):

    def __init__(self, response_metadata: BravadoResponseMetadata):
        data = dict(elapsed_time=response_metadata.elapsed_time,
                    is_fallback_result=response_metadata.is_fallback_result,
                    processing_end_time=response_metadata.processing_end_time,
                    request_elapsed_time=response_metadata.request_elapsed_time,
                    request_end_time=response_metadata.request_end_time,
                    start_time=response_metadata.start_time,
                    status_code=response_metadata.status_code,
                    username=gc3_cfg.user.cloud_username
                    )



        super().__init__(mapping=data)
        _debug(f"{self.__class__.__name__} created.")


class IaaSServiceResponse(NestedOrderedDictAttrListBase):

    def __init__(self, service_response: BravadoResponseMetadata):
        results: list = service_response.incoming_response.json()['result']
        assert len(results)==1
        result: dict = results.pop()
        result['metadata'] = IaaSResponseMetadata(service_response.metadata)
        super().__init__(mapping=result)
        _debug(f"{self.__class__.__name__} created.")


class IaaSServiceResponses():

    def __init__(self, service_response: BravadoResponseMetadata):
        responses = []
        results: list = service_response.incoming_response.json()['result']
        result: dict = results.pop()
        result['metadata'] = IaaSResponseMetadata(service_response.metadata)
        for result in results:
            responses.append()
        super().__init__(mapping=result)
        _debug(f"{self.__class__.__name__} created.")
