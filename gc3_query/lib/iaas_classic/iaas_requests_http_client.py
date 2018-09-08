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

################################################################################
## Third-Party Imports
from urllib.parse import unquote_plus

from bravado.requests_client import RequestsClient, BasicAuthenticator
from requests.auth import HTTPBasicAuth
from requests.auth import _basic_auth_str

################################################################################
## Project Imports
from gc3_query.lib import *
from gc3_query.lib import gc3_cfg

from gc3_query.lib import get_logging
_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


class IaaSRequestsHTTPBasicAuth(HTTPBasicAuth):

    def __init__(self, username, password):
        super().__init__(username, password)

    def __call__(self, r):
        r.headers['Authorization'] = _basic_auth_str(self.username, self.password)
        return r

class IaaSRequestsBasicAuthenticator(BasicAuthenticator):

    def __init__(self, host, username, password):
        super().__init__(host, username, password)

    def __call__(self, *args, **kwargs):
        pass


class IaaSRequestsHTTPClient(RequestsClient):
    """Synchronous HTTP client implementation with tweaks for Oracle Cloud.
    """

    def __init__(self, idm_cfg: Dict[str, Any], skip_authentication: bool = False):
        super().__init__()
        self.idm_cfg = idm_cfg
        self.skip_authentication = skip_authentication
        self.idm_domain_name = self.idm_cfg.name
        self.rest_endpoint: str = self.idm_cfg.rest_endpoint
        # self.headers = {'Content-Type': 'application/oracle-compute-v3+json',
        #                 'Accept': 'application/oracle-compute-v3+json, json, text/html',
        #                 }
        # self.session.headers['Content-Type'] = 'application/oracle-compute-v3+json'
        if gc3_cfg.user.use_proxy:
            _info(f"gc3_cfg.user.use_proxy={gc3_cfg.user.use_proxy}, configuring proxy.")
            self.proxies = {'http': gc3_cfg.network.http_proxy, 'https': gc3_cfg.network.https_proxy}
            self.session.proxies.update(self.proxies)
        else:
            _info(f"gc3_cfg.user.use_proxy={gc3_cfg.user.use_proxy}, not configuring proxy.")
            self.proxies = None

        _debug(f"rest_endpoint={self.rest_endpoint}")
        _debug(f"proxies={self.proxies}")
        _debug(f"idm_cfg={self.idm_cfg}")
        # _debug(f"headers={self.headers}")

        if self.skip_authentication:
            _warning(f"skip_authentication={self.skip_authentication}, authentication disabled.")
            self.auth_cookie_header = None
        else:
            self.auth_cookie_header = self.authenticate()
            # self.session.headers.update(self.auth_cookie_header)
            _debug(f"self.session.headers={self.session.headers}")

    @property
    def authenticated(self):
        return 'nimbula' in self.session.cookies

    def authenticate(self) -> dict:
        auth_url = f"{self.rest_endpoint}/authenticate/"
        idm_cred = gc3_cfg.get_credential(idm_domain_name=self.idm_cfg.name)

        # BULLSHIT, this doesn't work! If you are using a traditional cloud account or if your account creation email contains information about the identity domain as shown in the following example,
        # then you must use the following format for the two-part user name:
        # /Compute-identityDomainName/username
        #
        # If you are using a cloud account with Identity Cloud Service (IDCS) or if your account creation email does not contain information about the identity domain,
        # then you must use the following format for the two-part user name:
        # /Compute-serviceInstanceID/username


        json_data = {"user": f"/Compute-{self.idm_cfg.service_instance_id}/{idm_cred.username}", "password": idm_cred.password}
        # json_data = {"user": f"/Compute-{self.idm_cfg.name}/{idm_cred.username}", "password": idm_cred.password}
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

    @staticmethod
    def separate_params(request_params: DictStrAny) -> Tuple[DictStrAny, DictStrAny]:
        """Splits the passed in dict of request_params into two buckets, and Replace %xx escapes in the URL by their single-character
        equivalent.

        - sanitized_params are valid kwargs for constructing a
          requests.Request(..)
        - misc_options are things like timeouts which can't be communicated
          to the Requests library via the requests.Request(...) constructor.

        :param request_params: kitchen sink of request params. Treated as a
            read-only dict.
        :returns: tuple(sanitized_params, misc_options)
        """
        _debug(f"input request_params={request_params}")
        sanitized_params: Dict[str, Any]
        misc_options: Dict[str, Any]
        sanitized_params, misc_options = RequestsClient.separate_params(request_params=request_params)
        _debug(f"From RequestsClient baseclass: sanitized_params={sanitized_params}, misc_options={misc_options}")
        unquoted_url = unquote_plus(sanitized_params['url'])
        _debug(f"unquoted_url={unquoted_url}")
        sanitized_params['url'] = unquoted_url
        return sanitized_params, misc_options

