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

from bravado.client import SwaggerClient
################################################################################
## Third-Party Imports
from bravado.client import inject_headers_for_remote_refs

################################################################################
## Project Imports
from gc3_query.lib import *
from gc3_query.lib.gc3_bravado import bravado_config
# from gc3_query.lib.open_api.swagger_formats import gc3_formats
from gc3_query.lib.gc3_bravado import bravado_cfg

# BRAVADO_CORE_CONFIG: DictStrAny = gc3_cfg.bravado.core_config.as_dict()
# BRAVADO_CORE_CONFIG['formats'] = gc3_formats
# BRAVADO_CLIENT_CONFIG: DictStrAny = gc3_cfg.bravado.client_config.as_dict()
# BRAVADO_CONFIG: DictStrAny = gc3_cfg.bravado.core_config.as_dict_melded_with(gc3_cfg.bravado.client_config)
# BRAVADO_CONFIG['formats'] = gc3_formats



from gc3_query.lib import get_logging
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

        # config = config if config else gc3_cfg.BRAVADO_CONFIG
        config: DictStrAny = bravado_cfg.BRAVADO_CONFIG


        http_client.set_basic_auth(host='https://compute.uscom-central-1.oraclecloud.com', username="/Compute-587626604/eric.harris@oracle.com", password="V@nadium123!")

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



    # @classmethod
    # def from_spec(cls, spec_dict, origin_url=None, http_client=None,
    #               config=None):
    #     """
    #     Build a :class:`SwaggerClient` from a Swagger spec in dict form.
    #
    #     :param spec_dict: a dict with a Swagger spec in json-like form
    #     :param origin_url: the url used to retrieve the spec_dict
    #     :type  origin_url: str
    #     :param config: Configuration dict - see spec.CONFIG_DEFAULTS
    #
    #     :rtype: :class:`bravado_core.spec.Spec`
    #     """
    #     http_client = http_client or RequestsClient()
    #     config = config or {}
    #
    #     # Apply bravado config defaults
    #     bravado_config = BravadoConfig.from_config_dict(config)
    #     # remove bravado configs from config dict
    #     for key in set(bravado_config._fields).intersection(set(config)):
    #         del config[key]
    #     # set bravado config object
    #     config['bravado'] = bravado_config
    #
    #     swagger_spec = Spec.from_dict(
    #         spec_dict, origin_url, http_client, config,
    #     )
    #     return cls(swagger_spec, also_return_response=bravado_config.also_return_response)
