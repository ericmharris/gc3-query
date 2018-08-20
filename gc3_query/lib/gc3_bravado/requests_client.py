# -*- coding: utf-8 -*-

from urllib.parse import ParseResult, urlunparse, unquote_plus, quote
from urllib.parse import urlparse as urlparse3

from bravado.requests_client import RequestsClient

from gc3_query.lib import *
from gc3_query.lib import get_logging

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


# _critical(f"This implimentation no longer works using the latest version of gc3_bravado.  request() signature has changed.")

class OCRequestsClient(RequestsClient):
    """Synchronous HTTP client implementation with tweaks for Oracle Cloud.
    """
    # _critical(f"This implimentation no longer works using the latest version of gc3_bravado.  request() signature has changed.")

    # def request(self, request_params, operation=None, response_callbacks=None, also_return_response=False):
    #     """
    #     :param request_params: complete request data.
    #     :type_name request_params: dict
    #     :param operation: operation that this http request is for. Defaults
    #         to None - in which case, we're obviously just retrieving a Swagger
    #         Spec.
    #     :type_name operation: :class:`bravado_core.operation.Operation`
    #     :param response_callbacks: List of callables to post-process the
    #         incoming response. Expects args incoming_response and operation.
    #     :param also_return_response: Consult the constructor documentation for
    #         :class:`gc3_bravado.http_future.HttpFuture`.
    #
    #     :returns: HTTP Future object
    #     :rtype: :class: `bravado_core.http_future.HttpFuture`
    #     """
    #     sanitized_params, misc_options = self.separate_params(request_params)
    #     sanitized_params = self.resanitize_params(sanitized_params)
    #
    #     requests_future = RequestsFutureAdapter(
    #         self.session, self.authenticated_request(sanitized_params), misc_options
    #     )
    #
    #     return HttpFuture(requests_future, RequestsResponseAdapter, operation, response_callbacks, also_return_response)

    def resanitize_params(self, request_params: Dict[str, Any]) -> Dict[str, Any]:
        """Updates request_params so they work better with OPC

        The gc3_bravado RequestsClient sanitizes  URL's using quote_plus() which converts/escapes '/' to '%2F'.

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
        # sanitized_params, misc_options = super().separate_params(request_params=request_params)
        # sanitized_params: Dict[str,Any], misc_options: Dict[str,Any] = RequestsClient.separate_params(request_params=request_params)
        sanitized_params: Dict[str, Any]
        misc_options: Dict[str, Any]
        sanitized_params, misc_options = RequestsClient.separate_params(request_params=request_params)
        _debug(f"From RequestsClient baseclass: sanitized_params={sanitized_params}, misc_options={misc_options}")
        unquoted_url = unquote_plus(sanitized_params['url'])
        _debug(f"unquoted_url={unquoted_url}")
        sanitized_params['url'] = unquoted_url
        #
        # url = sanitized_params.get("url", None)
        # # ParseResult(scheme='https', netloc='compute.uscom-central-1.oraclecloud.com', file_path='/instance/Compute-587626604%2Feric.harris%40oracle.com%2F', params='', query='', fragment='')
        # parsed_url: ParseResult = urlparse3(url)
        # unqoted_path = unquote_plus(parsed_url.path)
        # requoted_path = quote(unqoted_path)
        # parsed_url_d = parsed_url._asdict()
        #
        # ### https://compute.uscom-central-1.oraclecloud.com/instance/Compute-587626604/eric.harris%40oracle.com/
        # # parsed_url_d['file_path'] = requoted_path
        # # new_url = urlunparse(parsed_url_d.values())
        # ### https://compute.uscom-central-1.oraclecloud.com/instance/Compute-587626604/eric.harris@oracle.com/
        # parsed_url_d["file_path"] = unqoted_path
        # new_url = urlunparse(parsed_url_d.values())
        #
        # sanitized_params["url"] = new_url
        # _debug(f"url={url} parsed_url={parsed_url}, unqoted_path={unqoted_path}, requoted_path={requoted_path}, new_url={new_url}")
        # _debug(f"returned request_params={sanitized_params}")

        return sanitized_params, misc_options
