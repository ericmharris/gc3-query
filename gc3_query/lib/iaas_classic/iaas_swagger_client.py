# -*- coding: utf-8 -*-

"""
#@Filename : swagger_client
#@Date : [8/5/2018 1:11 PM]
#@Poject: gc3-query
#@AUTHOR : emharris

~~~~~~~~~~~~~~~~

<DESCR SHORT>

<DESCR>
"""

################################################################################
## Standard Library Imports
import sys, os
from copy import deepcopy

################################################################################
## Third-Party Imports
from dataclasses import dataclass
from melddict import MeldDict

################################################################################
## Project Imports
from gc3_query.lib import *
from dataclasses import dataclass
import bravado
from bravado.requests_client import RequestsClient
from bravado.client import SwaggerClient
from bravado.client import SwaggerClient, ResourceDecorator, inject_headers_for_remote_refs
from bravado.client import SwaggerClient, CallableOperation
from bravado.requests_client import RequestsResponseAdapter
from bravado.swagger_model import load_file
from bravado_core.exception import MatchingResponseNotFound
from bravado.exception import HTTPBadRequest
from bravado.http_future import HttpFuture
from bravado.swagger_model import Loader



BRAVADO_CORE_CONFIG: DictStrAny = gc3_cfg.bravado.core_config.as_dict()
BRAVADO_CLIENT_CONFIG: DictStrAny = gc3_cfg.bravado.client_config.as_dict()
BRAVADO_CONFIG: DictStrAny = gc3_cfg.bravado.core_config.as_dict_melded_with(gc3_cfg.bravado.client_config)

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


class IaaSSwaggerClient(SwaggerClient):

    @classmethod
    def from_api_catalog_url(cls, spec_url, rest_endpoint, http_client=None, request_headers=None, config=None):
        """Build a :class:`SwaggerClient` from a url to the Swagger
        specification for a RESTful API.

        :param spec_url: url pointing at the swagger API specification
        :type spec_url: str
        :param http_client: an HTTP client used to perform requests
        :type  http_client: :class:`bravado.http_client.HttpClient`
        :param request_headers: Headers to pass with http requests
        :type  request_headers: dict
        :param config: Config dict for bravado and bravado_core.
            See CONFIG_DEFAULTS in :module:`bravado_core.spec`.
            See CONFIG_DEFAULTS in :module:`bravado.client`.

        :rtype: :class:`bravado_core.spec.Spec`
        """
        _debug(u"Loading from %s", spec_url)

        config = config if config else BRAVADO_CONFIG


        # http_client = http_client if http_client else RequestsClient()
        # http_client.set_basic_auth(host='https://compute.uscom-central-1.oraclecloud.com', username="/Compute-gc30003/eric.harris@oracle.com", password="V@nadium123!")
        http_client.set_basic_auth(host='https://compute.uscom-central-1.oraclecloud.com', username="/Compute-587626604/eric.harris@oracle.com", password="V@nadium123!")
        # if 'Content-Type' not in http_client.session.headers:
        #     http_client.session.headers['Content-Type'] = 'application/oracle-compute-v3+json'
        #     raise RuntimeError(f"shouldn't be here because we don't use Requestslient()")
        # loader = Loader(http_client, request_headers=request_headers)
        # loader = Loader(http_client=http_client)
        #
        # ## TODO: schemas need to be set to https
        # spec_dict = loader.load_spec(spec_url)
        # spec_schemes_correct = 'https' in set(spec_dict.get('schemes', ['']))
        # if not spec_schemes_correct:
        #     spec_dict['schemes'] = ['https']
        #     _debug(f"Updated spec_dict['schemes'] = {spec_dict['schemes']}")

        raise RuntimeError('TODO:  use OpenApiSpecCatalog')
        # spec_client = SwaggerClient.from_url(spec_url=spec_url)
        # spec_dict = deepcopy(spec_client.swagger_spec.spec_dict)
        # spec_dict['schemes'] = ['https']

        # RefResolver may have to download additional json files (remote refs)
        # via http. Wrap http_client's request() so that request headers are
        # passed along with the request transparently. Yeah, this is not ideal,
        # but since RefResolver has new found responsibilities, it is
        # functional.
        if request_headers is not None:
            http_client.request = inject_headers_for_remote_refs(
                http_client.request, request_headers)

        return cls.from_spec(spec_dict=spec_dict, origin_url=rest_endpoint, http_client=http_client, config=config)




