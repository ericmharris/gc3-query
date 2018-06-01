# Copyright (c) 2015 Oracle and/or its affiliates. All rights reserved.
# created by abhijit.jere

import requests
import json
import logging
from collections import OrderedDict
from urllib.parse import quote
try:
    from handlers import RequestParamHandler, ResponseHandler
    from utils import Utils
    from __init__ import __version__
    from messages import Messages, ErrorMessages
    from opcservice import OPCService
except:
    from .handlers import RequestParamHandler, ResponseHandler
    from .utils import Utils
    from .__init__ import __version__
    from .messages import Messages, ErrorMessages
    from .opcservice import OPCService

#=== CONSTANTS ================================================================
logger = logging.getLogger(__name__)

#=== CLASSES ==================================================================
class RequestExecutor():
    # The object which holds RequestParamHandler
    def __init__(self, reqParamHandler):
        '''
            :type_name reqParamHandler: RequestParamHandler
            :param reqParamHandler: RequestParamHandler object
        '''
        self._reqParamHandler = reqParamHandler
        self._utils = Utils()
        self.check_and_refresh_access_token()

    @property
    def reqParamHandler(self):
        return self._reqParamHandler

    def pre_execute_request(self):
        raise NotImplementedError("Not Implemented")

    def check_and_refresh_access_token(self):
        service = OPCService()
        # check if the access token is expired
        refresh_token = self._utils.isAccessTokenExpired()
        # if token is expired, refresh the access token
        if refresh_token:
            access_token, expires_in = service.get_oauth_access_token(refresh_token=refresh_token)
            self._utils.persistTokenAndExpiryTime(access_token, expires_in)

    def execute_request(self):
        '''
         1) Build HTTP request
         2) Execute HTTP request (Call the REST endpoint)
         3) Pass on the response to ResponseHandler
        '''

        # Build and Execute HTTP request (Call the REST endpoint)
        try:
            response = self._build_and_execute_request(self.reqParamHandler)
            req = response.request
            logger.debug("Response: Method: %s, url: %s, headers: %s." % (req.method, req.url, self._utils.get_response_header_with_no_auth(response.headers)))
            # Request succeeded, pass on the response to ResponseHandler
            # send the command dict values to the handlers.

            ResponseHandler(response).process_response(self.reqParamHandler.command_dict_values, \
                                                       self.reqParamHandler.cmd_name, \
                                                       self.reqParamHandler.output_format_cmd_level, \
                                                       self.reqParamHandler.wait_until_complete_cmd_level, \
                                                       self.reqParamHandler.srv_name, \
                                                       self.reqParamHandler.additional_response_values)
        except requests.exceptions.ConnectionError as ce:
            logger.error(ErrorMessages.OPAAS_CLI_CONNECTION_ERROR % ce)
            raise requests.exceptions.ConnectionError(ErrorMessages.OPAAS_CLI_CONNECTION_ERROR_DISPLAY % ce)
        except requests.exceptions.Timeout as te:
            logger.error(ErrorMessages.OPAAS_CLI_TIMEOUT_ERROR % te)
            raise requests.exceptions.Timeout(ErrorMessages.OPAAS_CLI_TIMEOUT_ERROR_DISPLAY % te)
        except requests.exceptions.InvalidURL as ie:
            logger.error(ErrorMessages.OPAAS_CLI_INVALID_URL_ERROR % ie)
            raise requests.exceptions.InvalidURL(ErrorMessages.OPAAS_CLI_INVALID_URL_ERROR_DISPLAY % request.url)
        except requests.exceptions.RequestException as e:
            logger.error(ErrorMessages.OPAAS_CLI_REQUESTS_ERROR % e)
            raise e

    def _build_and_execute_request(self, reqParamHandler):
        '''
        Build and Execute HTTP request
        '''
        utils = Utils()
        defaultUri = utils.getValueFromConfigFile(utils.default_uri)
        method = reqParamHandler.method
        uri = reqParamHandler.uri
        content_type = reqParamHandler.contenttype
        headers = OrderedDict()
        bodyParams = dict()
        queryParams = dict()

        # Set identityDomainId
        identityDomain = utils.getValueFromConfigFile(utils.identity_domain)
        uri = uri.replace('{identityDomainId}', identityDomain)

        # headers
        headers[utils.authorization_header_key] = utils.getAuthToken()
        headers[utils.identity_domain_header_key] = identityDomain
        headers[utils.cli_request_key] = 'cli' # Value doesn't matter
        headers[utils.cli_header_version_key] = __version__
        # Requests Module sets its own content type_name with boundary conditions for multipart/form-data .
        # for example: 'Content-Type': 'multipart/form-data; boundary=104ea81ca5814458b30984687aacb591'
        if content_type is not None and content_type != 'multipart/form-data':
            headers['Content-Type'] = content_type

        # path, query and body queryParams
        for param, value in reqParamHandler.cmd_params_values.items():
            paramType = reqParamHandler.param_dict[param]['paramType']
            type = reqParamHandler.param_dict[param]['type_name']
            if paramType == 'path':
                # BUG FIX: 27474210. Added quote to encode the path params.
                uri = uri.replace('{' + param + '}', quote(value))
            elif paramType == 'query':
                queryParams[param] = value
            elif paramType == 'body':
                if type.lower() in ('json', 'file'):
                    # if content type_name is multipart then populate bodyparams as key, value.
                    # else populate bodyparam by updating the dict.
                    if content_type is not None and content_type.strip() == 'multipart/form-data':
                        bodyParams[param] = value
                    else:
                        if bool(bodyParams):
                            bodyParams.update(value)
                        else:
                            bodyParams = value
                elif type.lower() == 'list':
                    # FIX: Bug 22517700 - parse list into nested json.
                    nested_dict = {}
                    for key_value in value:
                        if ':' in key_value:
                            # Split the first occurence of the split sept ':'
                            # as the value before the first ':', is the key and
                            # after ':' is the value. FIX: BUG 24961678
                            k,v = key_value.split(':', 1)
                            nested_dict[k] = v
                        else:
                            nested_dict[key_value] = ""
                    bodyParams[param] = nested_dict
                else:
                    bodyParams[param] = utils.convertInputToJson(value)
            else:
                logger.debug('Unknown parameter type_name \'' + paramType + '\' for parameter \'' + param + '\'.')
                print('Unknown parameter type_name \'' + paramType + '\' for parameter \'' + param + '\'.')

        # data needs json object, hence json.dumps being used.
        # if the bodyParams/queryParams is empty then send None.
        files = None
        data = None
        # Fix: BUG 22504436: added files parameter for multipart/form-data content-type_name.
        if content_type is not None and content_type.strip() == 'multipart/form-data':
            # FIX: BUG 22572441, 22572329: Fixed the form data by populating files using tuples.
            files_tuple = []
            wrap_inside_list = []
            for k,v in bodyParams.items():
                wrapInsideValue = reqParamHandler.param_dict[k]['wrapInside'] if 'wrapInside' in reqParamHandler.param_dict[k] else None
                if (isinstance(v, dict)):
                    files_tuple.append((k, (k, str(json.dumps(v)))))
                elif wrapInsideValue:
                    wrap_inside_list.append(wrapInsideValue)
                else:
                    files_tuple.append((k, ('', str(v))))

            # create the payload with the wrapInside keywords value
            # BUG FIX: 22779287
            if len(wrap_inside_list) != 0:
                # removing duplicates
                wrap_inside_list = set(wrap_inside_list)
                for value in wrap_inside_list:
                    payload_dict = dict()
                    for k,v in bodyParams.items():
                        if 'wrapInside' in reqParamHandler.param_dict[k] and reqParamHandler.param_dict[k]['wrapInside'] ==  value:
                            payload_dict[k] = v
                    files_tuple.append((value, ('', str(json.dumps(payload_dict)))))

            # files has to be populated, so the content-type_name is set by the requests module.
            # Hence, using empty string even if no params were specified.
            if len(files_tuple) == 0:
                # Fix: BUG 22756412: to send an empty payload when content type_name is multipart/form-data
                files = {'options': ('', str(dict()), content_type)}
            else:
                files = files_tuple
            # END.
        else:
            # BUG FIX: 27507188. send the string as is. There is no need to convert
            if isinstance(bodyParams, str) and bodyParams and len(bodyParams.strip()) > 0:
                data = bodyParams
            else:
                data = json.dumps(bodyParams) if bool(bodyParams) else self._chkEmptyPayload(method)

        params = queryParams if bool(queryParams) else None
        request_url = defaultUri + uri
        logger.debug("Request: Method: %s, url: %s, data: %s, files: %s, headers: %s." % (method, request_url, utils.changeValueOfPwd(data), files, utils.get_response_header_with_no_auth(headers)))
        # Execute request and get response object
        response = requests.request(method=method, url=request_url, headers=headers, data=data, files=files, params=params)

        return response

    # For GET requests in EDG and PROD env, need to send None.
    def _chkEmptyPayload(self, method):
        if method.lower() == 'get':
            return None
        else:
            return json.dumps(dict())
