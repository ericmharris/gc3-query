# -*- coding: utf-8 -*-

"""
#@Filename : requests_client
#@Date : [7/30/2018 1:51 PM]
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
from urllib.parse import urlparse as urlparse3
from urllib.parse import ParseResult, urlunparse, unquote_plus, quote, urljoin

from bravado.http_client import HttpClient
from bravado.http_future import FutureAdapter
from bravado.http_future import HttpFuture
from bravado.requests_client import RequestsClient, RequestsFutureAdapter, RequestsResponseAdapter

################################################################################
## Project Imports
from gc3_query.lib import *
from gc3_query.lib import gc3_cfg

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


class IaaSRequestsClient(RequestsClient):
    """Synchronous HTTP client implementation with tweaks for Oracle Cloud.
    """

    def __init__(self, idm_cfg: Dict[str, Any], skip_authentication: bool = False):
        super().__init__()
        self.idm_cfg = idm_cfg
        self.skip_authentication = skip_authentication
        self.idm_domain_name = self.idm_cfg.name
        self.rest_endpoint: str = self.idm_cfg.rest_endpoint
        self.headers = {'Content-Type':'application/oracle-compute-v3+json',
                   'Accept':'application/oracle-compute-v3+directory+json',
                   }
        self.session.headers.update(self.headers)
        if gc3_cfg.user.use_proxy:
            _info(f"gc3_cfg.user.use_proxy={gc3_cfg.user.use_proxy}, configuring proxy.")
            self.proxies = {'http': gc3_cfg.network.http_proxy, 'https': gc3_cfg.network.https_proxy }
            self.session.proxies.update(self.proxies)
        else:
            _info(f"gc3_cfg.user.use_proxy={gc3_cfg.user.use_proxy}, not configuring proxy.")
            self.proxies = None


        _debug(f"rest_endpoint={self.rest_endpoint}")
        _debug(f"proxies={self.proxies}")
        _debug(f"idm_cfg={self.idm_cfg}")
        _debug(f"headers={self.headers}")

        if self.skip_authentication:
            _warning(f"skip_authentication={self.skip_authentication}, authentication disabled.")
            self.auth_cookie_header = None
        else:
            self.auth_cookie_header = self.authenticate()
            self.session.headers.update(self.auth_cookie_header)
            _debug(f"self.session.headers={self.session.headers}")





    def authenticate(self)->str:
        auth_url = f"{self.rest_endpoint}/authenticate/"
        idm_cred = gc3_cfg.get_credential(idm_domain_name=self.idm_cfg.name)
        json_data = {"user": f"/Compute-{self.idm_cfg.service_instance_id}/{idm_cred.username}", "password":idm_cred.password }
        response = self.session.post(url=auth_url, json=json_data)
        if response.ok:
            _info(f'Response OK: {response.ok}, Status Code: {response.status_code}, URL: {response.url}')
        else:
            _debug(f"Failed to authenticate user:  auth_url={auth_url}, self.idm_cfg={self.idm_cfg}")
            _error(f'Response OK: {response.ok}, Status Code: {response.status_code}, URL: {response.url}')
            raise RuntimeError(f"Failed to authenticate user:  auth_url={auth_url}, self.idm_cfg={self.idm_cfg}")

        cookie_header = {'Cookie': response.headers['Set-Cookie']}
        _debug(f"cookie_header={cookie_header}")
        # TODO: enable this
        # del(idm_cred)
        # del(json_data)
        # del(response)
        return cookie_header



    def request(self, request_params, operation=None, response_callbacks=None, also_return_response=False):
        """
        :param request_params: complete request data.
        :type_name request_params: dict
        :param operation: operation that this http request is for. Defaults
            to None - in which case, we're obviously just retrieving a Swagger
            Spec.
        :type_name operation: :class:`bravado_core.operation.Operation`
        :param response_callbacks: List of callables to post-process the
            incoming response. Expects args incoming_response and operation.
        :param also_return_response: Consult the constructor documentation for
            :class:`bravado.http_future.HttpFuture`.

        :returns: HTTP Future object
        :rtype: :class: `bravado_core.http_future.HttpFuture`
        """
        sanitized_params, misc_options = self.separate_params(request_params)
        sanitized_params = self.resanitize_params(sanitized_params)

        requests_future = RequestsFutureAdapter(
            self.session, self.authenticated_request(sanitized_params), misc_options
        )

        return HttpFuture(requests_future, RequestsResponseAdapter, operation, response_callbacks, also_return_response)

    def resanitize_params(self, request_params: Dict[str, Any]) -> Dict[str, Any]:
        """Updates request_params so they work better with OPC

        The bravado RequestsClient sanitizes  URL's using quote_plus() which converts/escapes '/' to '%2F'.

        url = 'https://compute.uscom-central-1.oraclecloud.com/instance/Compute-587626604%2Feric.harris%40oracle.com%2F'
        url_wanted = 'https://compute.uscom-central-1.oraclecloud.com/instance/Compute-587626604/eric.harris@oracle.com/'

        """
        _debug(f"input request_params={request_params}")
        url = request_params.get("url", None)
        # ParseResult(scheme='https', netloc='compute.uscom-central-1.oraclecloud.com', file_path='/instance/Compute-587626604%2Feric.harris%40oracle.com%2F', params='', query='', fragment='')
        parsed_url: ParseResult = urlparse3(url)
        unqoted_path = unquote_plus(parsed_url.path)
        requoted_path = quote(unqoted_path)
        parsed_url_d = parsed_url._asdict()

        ### https://compute.uscom-central-1.oraclecloud.com/instance/Compute-587626604/eric.harris%40oracle.com/
        # parsed_url_d['file_path'] = requoted_path
        # new_url = urlunparse(parsed_url_d.values())
        ### https://compute.uscom-central-1.oraclecloud.com/instance/Compute-587626604/eric.harris@oracle.com/
        parsed_url_d["file_path"] = unqoted_path
        new_url = urlunparse(parsed_url_d.values())

        request_params["url"] = new_url
        _debug(
            f"url={url} parsed_url={parsed_url}, unqoted_path={unqoted_path}, requoted_path={requoted_path}, new_url={new_url}"
        )
        _debug(f"returned request_params={request_params}")
        return request_params
