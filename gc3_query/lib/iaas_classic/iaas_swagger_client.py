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

################################################################################
## Third-Party Imports
from dataclasses import dataclass

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
        http_client = http_client or RequestsClient()
        loader = Loader(http_client, request_headers=request_headers)
        spec_dict = loader.load_spec(spec_url)

        # RefResolver may have to download additional json files (remote refs)
        # via http. Wrap http_client's request() so that request headers are
        # passed along with the request transparently. Yeah, this is not ideal,
        # but since RefResolver has new found responsibilities, it is
        # functional.
        if request_headers is not None:
            http_client.request = inject_headers_for_remote_refs(
                http_client.request, request_headers)

        return cls.from_spec(spec_dict=spec_dict, origin_url=rest_endpoint, http_client=http_client, config=config)
