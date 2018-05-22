# Copyright (c) 2015 Oracle and/or its affiliates. All rights reserved.
# created by sahit.gollapudi


"""scripts.opcservice: opcservice module within the opc package"""


import requests
import sys
import json
import zipfile
import io
import os
import keyring
import logging 
from collections import OrderedDict
from requests.auth import _basic_auth_str
try:
    from utils import Utils
    from messages import Messages, ErrorMessages,LocalizationConstants
    from exceptions import OSSDetailsError, PSMOAuthError, WCJobPollingError, AccsStreamLogError
except:
    from .utils import Utils
    from .messages import Messages, ErrorMessages, LocalizationConstants
    from .exceptions import OSSDetailsError, PSMOAuthError, WCJobPollingError, AccsStreamLogError

# Logger
logger = logging.getLogger(__name__)

class OPCService(object):
    # Set the request parameters

    def __init__(self):
        self._cnf = Utils()
        self._fileSeparator = "/"
    
    def checkCredentials (self, token, identityDomain, urlHostName, return_cli_artifacts_upgrade=False):  
        """
            :type return_cli_artifacts_upgrade: bool
            :param return_cli_artifacts_upgrade: is true when it is called for upgrade cli to retrieve the header info.
        """
        # to check if the credentials are valid.
        urlHost = urlHostName
        urlChkConnection = '/paas/api/v1.1/cli/' + identityDomain + '/client?type=connection' 
        
        url = urlHost + urlChkConnection

        try:
            logger.info(Messages.OPAAS_CLI_CHK_CONN)
            logger.debug("Request: url: %s, headers: %s" % (url, {self._cnf.cli_request_key : 'cli', self._cnf.identity_domain_header_key : identityDomain}))
            
            response = requests.get(url, headers={'Authorization' : token, self._cnf.cli_request_key : 'cli', self._cnf.identity_domain_header_key : identityDomain}, timeout=60)

            # Check for HTTP codes for 200
            logger.debug("Response: Method: %s, url: %s, headers: %s" % (response.request.method, response.request.url, self._cnf.get_response_header_with_no_auth(response.headers)))      
            
            if response.status_code == 200: 
                if return_cli_artifacts_upgrade:
                    return response.headers[self._cnf.build_version_key] if self._cnf.build_version_key in response.headers else None
                else:
                    return True
            else:
                logger.error(ErrorMessages.OPAAS_CLI_CHK_CONN_FAIL_ERROR % response.status_code)
                return response.status_code 
                        
        except (requests.exceptions.ConnectionError, requests.exceptions.InvalidURL, requests.exceptions.HTTPError) as e:
            logger.error(ErrorMessages.OPAAS_CLI_CONNECTION_ERROR % e)
            # invalid URI with connection refused.
            return 111
        except requests.exceptions.RequestException as e:
            logger.error(ErrorMessages.OPAAS_CLI_REQUESTS_ERROR % e)
            errMsg = "{}".format(e)
            if 'Invalid URL' in errMsg:
                return 111
            return False 
                  
    # Explicitly passing the auth_token & setupTable to ensure writing to setUp.conf is atomic
    def callRestApiGetServiceTypes(self, explicit, auth_token=None, setupTable=None):
        """
            :type explicit: boolean
            :param explicit: true if the setup is run explicitly.
            
            :type auth_token: str
            :param auth_token: auth_token
            
            :type setupTable: dict
            :param setupTable: a dict that consists of all the setup values
        """
        # Do the HTTP get request
        
        # Get the values from setupTable if 'explicit'
        cli_artifacts_versions = None
        try:
            if explicit:
                urlHost = setupTable[self._cnf.default_uri]
                identityDomain = setupTable[self._cnf.identity_domain]
                token = auth_token
            else:
                urlHost = self._cnf.getValueFromConfigFile(self._cnf.default_uri)
                identityDomain = self._cnf.getValueFromConfigFile(self._cnf.identity_domain)
                token = self._cnf.getAuthToken()
                
            if not token:
                logger.debug(ErrorMessages.OPASS_CLI_TOKEN_NOT_FOUND_ERROR)
                return False,None
           
            opcDir = self._cnf.opc_data_dir
            serviceIndexFile = self._cnf.opc_data_dir + self._cnf.service_index_filename   
            urlGetServiceCatalog = '/paas/api/v1.1/cli/' + identityDomain + '/client?type=catalog' 

            logger.info(Messages.OPAAS_CLI_DOWNLOAD_CATALOG)
            logger.debug("Request: url: %s, headers: %s" % (urlHost + urlGetServiceCatalog, {self._cnf.cli_request_key : 'cli', self._cnf.identity_domain_header_key : identityDomain}))
            
            response = requests.get(urlHost + urlGetServiceCatalog, headers={'Authorization' : token, self._cnf.cli_request_key : 'cli', self._cnf.identity_domain_header_key : identityDomain})

            # Check for HTTP codes other than 200
            logger.debug("Response: Method: %s, url: %s, headers: %s" % (response.request.method, response.request.url, self._cnf.get_response_header_with_no_auth(response.headers)))      
            
            if response.status_code != 200:
               logger.error(ErrorMessages.OPAAS_CLI_STATUS_CODE_ERROR_DISPLAY % response.status_code)
               sys.stdout.write(ErrorMessages.OPAAS_CLI_STATUS_CODE_ERROR_DISPLAY % response.status_code)
               return False,None              
            
            logger.info(Messages.OPAAS_CLI_DOWNLOAD_CATALOG_SUCCESS)
            # read the content as a zip file.
            zipDocument = zipfile.ZipFile(io.BytesIO(response.content))
            ret = zipDocument.testzip()
            
            if ret is not None:
                logger.error(ErrorMessages.OPAAS_CLI_BAD_RESPONSE_ZIPFILE)
                sys.stderr.write(ErrorMessages.OPAAS_CLI_BAD_RESPONSE_ZIPFILE_DISPLAY)
                return False,None
            else:
                if explicit:
                    # check for build no. if exist then update the build no no matter what. no check is required
                    # to see if the build no is changed from previous.  
                    cli_artifacts_versions = response.headers[self._cnf.build_version_key] if self._cnf.build_version_key in response.headers else None     
                    if cli_artifacts_versions is None:
                        logger.error(ErrorMessages.OPASS_CLI_VERSION_NOT_FOUND_ERROR)
                        sys.stderr.write(ErrorMessages.OPAAS_CLI_SETUP_VERSION_ERR_DISPLAY)
                        return False, None
                    
                if not os.path.exists(opcDir):
                    os.makedirs(opcDir)
                # remove the files in the directory bfr extracting
                self._cnf.removeFilesFromDir(opcDir, ".json")
                # extract to the directory
                zipDocument.extractall(path=opcDir)
            
            if explicit:
                # check if the file exist. to ensure that the extraction was successful.
                with open(serviceIndexFile) as json_file:
                     data = json.load(json_file, object_pairs_hook=OrderedDict)
                sys.stdout.write('----------------------------------------------------\n')
                sys.stdout.write(str(Messages.OPAAS_CLI_SETUP_SUCCESS_MSG))
                services = data['services']
                for service, value in services.items():
                    # BUG Fix: 27112221. to display service name from service mapping
                    if service.lower() in LocalizationConstants.ServiceMapping:
                        service = LocalizationConstants.ServiceMapping[service.lower()]
                    sys.stdout.write("  o %s : %s\n" % (service, value))
                sys.stdout.write('----------------------------------------------------\n')
                return True,cli_artifacts_versions
            
            return True,None 
        
        except requests.exceptions.RequestException as e:
            logger.error(ErrorMessages.OPAAS_CLI_REQUESTS_ERROR % e)
            sys.stderr.write ("Error : {}\n".format(e))
            return False,None
        except requests.exceptions.ConnectionError as e:
            errMsg = ErrorMessages.OPAAS_CLI_CONNECTION_ERROR % e
            logger.error(errMsg)
            sys.stderr.write ("Error : {}\n".format(e))
            return False,None

    # api used to download the client for psm upgrade.
    def callRestApiToDownloadClient(self):
        # Do the HTTP get request
        try:
            
            token = self._cnf.getAuthToken()
            if not token:
               return
           
            tmp_storage = self._cnf.tmp_storage_win if self._cnf.isWindows() else self._cnf.tmp_storage_linux
            serviceIndexFile = self._cnf.opc_data_dir + self._cnf.service_index_filename

            urlHost = self._cnf.getValueFromConfigFile(self._cnf.default_uri)
            identityDomain = self._cnf.getValueFromConfigFile(self._cnf.identity_domain)
            urlGetClientZip = '/paas/api/v1.1/cli/' + identityDomain + '/client' 
            
            logger.info(Messages.OPAAS_CLI_DOWNLOAD_KIT)
            logger.debug("Request: url: %s, headers: %s" % (urlHost + urlGetClientZip, {self._cnf.cli_request_key : 'cli', self._cnf.identity_domain_header_key : identityDomain}))
            
            # call to download the cli.
            response = requests.get(urlHost + urlGetClientZip, headers={'Authorization' : token, self._cnf.cli_request_key : 'cli', self._cnf.identity_domain_header_key : identityDomain})
            
            logger.debug("Response: Method: %s, url: %s, headers: %s" % (response.request.method, response.request.url, self._cnf.get_response_header_with_no_auth(response.headers)))      

            # Check for HTTP codes other than 200
            if response.status_code != 200:
               logger.error(ErrorMessages.OPAAS_CLI_DOWNLOAD_KIT_ERROR % response.status_code)
               sys.stdout.write(ErrorMessages.OPAAS_CLI_STATUS_CODE_ERROR_DISPLAY % response.status_code)
               # Error will result in no zip file and hence exit.
               sys.exit(1)
               # comment the above one for testing once the kit has downloaded and uncomment the below line.
               # return tmp_storage            
            
            # read the content as a zip file.
            zipDocument = zipfile.ZipFile(io.BytesIO(response.content))
            ret = zipDocument.testzip()
            
            if ret is not None:
                logger.error(ErrorMessages.OPAAS_CLI_DOWNLOAD_KIT_CORRUPTED_DISPLAY)
                sys.stdout.write(ErrorMessages.OPAAS_CLI_DOWNLOAD_KIT_CORRUPTED_DISPLAY)
                sys.exit(1)
            
            logger.info(Messages.OPAAS_CLI_DOWNLOAD_KIT_SUCCESS)
            # storing the zip into a location. TODO: add platform here.
            with open(tmp_storage, "wb") as code:
                code.write(response.content)               
            
            # return the filename with the location.
            return tmp_storage
        except requests.exceptions.RequestException as e:
            logger.error(ErrorMessages.OPAAS_CLI_REQUESTS_ERROR % e)
            sys.stderr.write ("Error : {}\n".format(e)) 
            sys.exit(1)
                  
    def get_details(self, method=None, request_url=None, headers=None, data=None, files=None, params=None, details_type=None):
        
        max_upload_size = None
                
        try:
            logger.debug("Request: url: %s, headers: %s, method: %s, data: %s" % (request_url, self._cnf.get_response_header_with_no_auth(headers), method, self._cnf.changeValueOfPwd(data)))
            response = requests.request(method=method, url=request_url, headers=headers, data=data, files=files, params=params)
            # Check for HTTP codes other than 200
            logger.debug("Response: Method: %s, url: %s, headers: %s" % (response.request.method, response.request.url, self._cnf.get_response_header_with_no_auth(response.headers)))      
            # print("respone status code:%s"%response.status_code)
            # print("response json:%s"%response.json())
            if not response or (response and response.status_code >= 300):
                if response is not None:
                    try:
                        logger.error("Error while trying to get details with status code {0}: {1}".format(response.status_code, response.content.decode('ascii')))
                        response_error_json = response.content.decode('ascii')
                        if response_error_json:
                            sys.stderr.write(response_error_json + "\n")
                    except:
                        pass
                self._raise_get_details_error(details_type=details_type)
            
            content = self._get_response_content(response)
            if self._cnf._max_archive_upload_size in response.headers:
                max_upload_size = response.headers[self._cnf._max_archive_upload_size]
            
            return content, max_upload_size
        except (requests.exceptions.ConnectionError, requests.exceptions.InvalidURL, requests.exceptions.HTTPError) as e:
            errMsg = ErrorMessages.OPAAS_CLI_CONNECTION_ERROR % e
            logger.error(errMsg)
            self._raise_get_details_error(details_type=details_type)
        except requests.exceptions.RequestException as e:
            errMsg = ErrorMessages.OPAAS_CLI_REQUESTS_ERROR % e
            logger.error(errMsg)
            self._raise_get_details_error(details_type=details_type)
        
    def _get_response_content(self, response):
        try:
            content = response.json()
        except:
            content = response.content.decode('ascii')
        
        if not isinstance(content, dict):
            content = json.loads(content)
        
        return content 
    
    def _raise_get_details_error(self, details_type=None):
        if details_type == self._cnf.oauth_details_type:
            raise PSMOAuthError()
        elif details_type == self._cnf._wc_details_type:
            raise WCJobPollingError()
        elif details_type == self._cnf._accs_stream_log_details_type:
            raise AccsStreamLogError()
        else:
            raise OSSDetailsError()
     
    def get_oauth_access_token (self, setupTable=None, user=None, passwd=None, refresh_token=False):
        if refresh_token:
            client_id = self._cnf.getValueFromConfigFile(self._cnf.oauth_client_id)
            client_secret = self._cnf.getValueFromConfigFile(self._cnf.oauth_client_secret)
            uri = self._cnf.getValueFromConfigFile(self._cnf._oauth_idcs_url)
            auth_token = _basic_auth_str(client_id, client_secret)
            user = self._cnf.getValueFromConfigFile(self._cnf.username)
            passwd = self._cnf.getUserPasswd()
            defaultUri = self._cnf.getValueFromConfigFile(self._cnf.default_uri)
        else:
            client_id = setupTable[self._cnf.oauth_client_id] 
            client_secret = setupTable[self._cnf.oauth_client_secret] 
            uri = setupTable[self._cnf._oauth_idcs_url] #"https://psmdemo2.identity.c9dev1.oc9qadev.com/oauth2/v1/token"
            auth_token = _basic_auth_str(client_id, client_secret) 
            user=user 
            passwd = passwd 
            defaultUri = setupTable[self._cnf.default_uri]
            
        # remove the trailing slash if it exists:
        if defaultUri.endswith(os.sep):
            defaultUri = defaultUri[:-1]
        '''
        example of retrieving access token 
        curl -k -i -X POST -u <Client ID>:<Client secret> https://<identity tenant url>/oauth2/v1/token 
        -d 'grant_type=password&username=<username>&password=<user password>&scope=<URI encoded PSM API to be accessed>'
        '''
        # use 'urn:opc:resource:consumer::all' in the scope inorder to get access to all the PSM api's
        data = "grant_type=password&username={0}&password={1}&scope={2}urn:opc:resource:consumer::all".format(user,\
                                                                                                passwd,\
                                                                                                defaultUri)
        
        headers = OrderedDict()
        headers[self._cnf.authorization_header_key] = auth_token
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        oauthresponse, max_upload_size = self.get_details(method="POST", request_url=uri, headers=headers, data=data, details_type=self._cnf.oauth_details_type) 
        access_token = None
        expires_in = None
        try:
            #logger.info(oauthresponse)
            access_token = oauthresponse["access_token"]
            expires_in = oauthresponse["expires_in"]
        except KeyError as k:
            logger.error('Access token response for OAuth: %s, error: %s' % (oauthresponse, k))
        
        return access_token, expires_in
    
    def execute_request(self, method=None, request_url=None, headers=None, data=None, files=None, params=None):    
        errMsg = None
        try:
            logger.debug("Request: url: %s, headers: %s, method: %s, data: %s" % (request_url, self._cnf.get_response_header_with_no_auth(headers), method, self._cnf.changeValueOfPwd(data)))
            response = requests.request(method=method, url=request_url, headers=headers, data=data)
            # Check for HTTP codes other than 200
            logger.debug("Response: Method: %s, url: %s, headers: %s" % (response.request.method, response.request.url, self._cnf.get_response_header_with_no_auth(response.headers)))      
            
            return response.status_code, response, errMsg
            
        except (requests.exceptions.ConnectionError, requests.exceptions.InvalidURL, requests.exceptions.HTTPError) as e:
            errMsg = ErrorMessages.OPAAS_CLI_CONNECTION_ERROR % e
            logger.error(errMsg)
        except requests.exceptions.RequestException as e:
            errMsg = ErrorMessages.OPAAS_CLI_REQUESTS_ERROR % e
            logger.error(errMsg)
            
        return None, None, errMsg