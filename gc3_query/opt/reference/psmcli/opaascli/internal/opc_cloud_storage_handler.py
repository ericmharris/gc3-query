# Copyright (c) 2016 Oracle and/or its affiliates. All rights reserved.
# created by sahit.gollapudi

__author__ = "sahit"

import os
import io
import json
import mmap
import requests
import logging
from collections import OrderedDict
from requests.auth import _basic_auth_str
try:
    from .common_util import CommonUtil, StatusCodes as cloud_storage_controller
except:
    from common_util import CommonUtil, StatusCodes as cloud_storage_controller

logger = logging.getLogger(__name__)

class OPCCloudStorageHandler(object):

    def __init__(self):
        self._common_util = CommonUtil()
        self._storage_cloud_access_mechanism = None

    def do_request(self, method=None,request_url=None, headers=None, data=None, files=None, params=None, stream=None):
        try:
            logger.debug("Request: url: %s, headers: %s, method: %s" % (request_url, self._common_util.get_response_header_with_no_auth(headers), method))
            response = requests.request(method=method, url=request_url, headers=headers, data=data, files=files, params=params, stream=stream)
            logger.debug("Response: Method: %s, url: %s, headers: %s" % (response.request.method, response.request.url, response.headers))

            return response

        except (requests.exceptions.ConnectionError, requests.exceptions.InvalidURL, requests.exceptions.HTTPError) as e:
            errMsg = "Exception: %s" % e
            logger.error(errMsg)
            raise requests.exceptions.ConnectionError(errMsg)
        except requests.exceptions.RequestException as e:
            errMsg = "Exception: %s" % e
            logger.error(errMsg)
            raise requests.exceptions.RequestException(errMsg)

    def _get_response_content(self, response):
        try:
            content = response.json()
        except:
            content = response.content.decode('ascii')

        if not isinstance(content, dict):
            content = json.loads(content)

        return content

    def _upload_archive(self, opc_cloud_storage_json):

        cloud_usr = None
        cloud_pwd = None
        cloud_auth_token = None
        delete_header = False

        cloud_storage_url =  opc_cloud_storage_json['temp_url'] if 'temp_url' in opc_cloud_storage_json else opc_cloud_storage_json['cloud_storage_url']
        # determine which authorization format needs to be used.
        self._storage_cloud_access_mechanism = self._common_util.get_cloud_storage_access_mechanism(cloud_storage_url, opc_cloud_storage_json)
        if self._storage_cloud_access_mechanism == self._common_util.CLOUD_STORAGE_ACCESS_TEMP_URL:
            cloud_url = cloud_storage_url
        else:
            if self._storage_cloud_access_mechanism == self._common_util.CLOUD_STORAGE_ACCESS_USR_PWD:
                cloud_usr = opc_cloud_storage_json['cloud_user']
                cloud_pwd = opc_cloud_storage_json['cloud_pwd']
            elif self._storage_cloud_access_mechanism == self._common_util.CLOUD_STORAGE_ACCESS_AUTH_TOKEN:
                cloud_auth_token = opc_cloud_storage_json['cloud_auth_token']
            cloud_url = cloud_storage_url + "/" + opc_cloud_storage_json['archive_url']

        source = opc_cloud_storage_json['source']
        #checksum = self._common_util._build_md5_checksum(source)
        #print("checksum: {}".format(checksum))
        if 'delete' in opc_cloud_storage_json and opc_cloud_storage_json['delete']:
            delete_header = True

        upload_result = self._upload_to_storage_cloud(cloud_url, \
                                                        source, \
                                                        usr=cloud_usr, \
                                                        pwd=cloud_pwd, \
                                                        auth_token=cloud_auth_token, \
                                                        delete_header=delete_header
                                                        )

        return upload_result

    def _upload_to_storage_cloud(self, url, source, usr=None, pwd=None, auth_token=None, delete_header=False):
        headers = OrderedDict()
        if self._storage_cloud_access_mechanism == self._common_util.CLOUD_STORAGE_ACCESS_AUTH_TOKEN:
            headers[self._common_util.CLOUD_STORAGE_HEADER_TOKEN] = auth_token
        elif self._storage_cloud_access_mechanism == self._common_util.CLOUD_STORAGE_ACCESS_USR_PWD:
            headers["Authorization"] = _basic_auth_str(usr,pwd)

        if delete_header:
            headers[self._common_util.cloud_delete_header_key] = str(self._common_util.CLOUD_DELETE_HEADER_VALUE)

        headers['Content-Length'] = str(os.stat(source).st_size)
        #files = {'file' : open(source, 'rb')}
        try:
            with open(source, 'rb') as fileObj:
                mmapped_data = mmap.mmap(fileObj.fileno(), 0, access=mmap.ACCESS_READ)
                response = self.do_request(method='PUT', request_url=url, headers=headers, data=mmapped_data, stream=True) #files={'archive' : (os.file_path.basename(source), fileObj, 'application/x-gzip')})
                mmapped_data.close()
        except (IOError,KeyError) as e:
            logger.error("Error while uploading the archive: {0}".format(str(e)))
            raise Exception("Unable to upload the archive to Oracle Storage Cloud. Contact Oracle Support Services...")

        http_code = response.status_code
        upload_result = CloudStorageResultResponse()
        self._get_valid_error_msgs_upload(http_code, upload_result)

        return upload_result

    def _get_valid_error_msgs_upload(self, http_code, upload_result):
        '''
            To be in consistent with OPC_CLOUD_STORAGE api's
        '''
        status_message = "Exception occured while trying to upload the object to Oracle Storage Cloud"
        # BUG FIX 27477118: 201 is for non-bmc and 200 is for BMC.
        if http_code == 201 or http_code == 200:
            status_message = "Uploaded the object to the Oracle Storage Cloud Service container..."
            upload_result.set_status_code(cloud_storage_controller.SUCCESS)
        elif http_code == 404:
            status_message = "Unable to upload the object: " \
                             "the URL to Oracle Storage Cloud Service container is incorrect..."
            upload_result.set_status_code(cloud_storage_controller.ERROR_REMOTE_RESOURCE_NOT_FOUND)
        elif http_code == 413:
            status_message = "Unable to upload the object to the Oracle Storage Cloud Service container. " \
                             "Not enough space on the Oracle Storage Cloud Service container...."
            upload_result.set_status_code(
                cloud_storage_controller.ERROR_NOT_ENOUGH_SPACE_ON_REMOTE_DEVICE)
        elif http_code == 401:
            status_message = "Unable to upload the object to the Oracle Storage Cloud Service container. " \
                             "User not authorized..."
            upload_result.set_status_code(cloud_storage_controller.ERROR_NOT_AUTHORIZED)
        elif http_code == 504:
            status_message = "Unable to upload the object to the Oracle Storage Cloud Service container. " \
                             "Gateway timeout..."
            upload_result.set_status_code(cloud_storage_controller.ERROR_TIMEOUT)
        elif http_code == 408:
            status_message = "Unable to upload the object to the Oracle Storage Cloud Service container. " \
                             "Connection timeout..."
            upload_result.set_status_code(cloud_storage_controller.ERROR_TIMEOUT)
        elif http_code == 418:  # customized http code for "could not resolve host error"
            status_message = "Unable to upload the object to the Oracle Storage Cloud Service container: " \
                             "Could not resolve host. The given remote host was not resolved..."
            upload_result.set_status_code(
                cloud_storage_controller.ERROR_CANNOT_RESOLVE_REMOTE_HOST)
        elif http_code == 419:  # customized http code for ssl error
            status_message = "Unable to upload the object to the Oracle Storage Cloud Service " \
                             "container..."
            upload_result.set_status_code(cloud_storage_controller.ERROR_SSL_EXCEPTION)
        elif http_code == 999:
            status_message = "Unable to upload the object to the Oracle Storage Cloud Service container: " \
                             "The HTTP Code: %s. Contact Oracle Support Services..." % http_code
            upload_result.set_status_code(cloud_storage_controller.ERROR_UPLOAD)
        else:
            status_message = "Unable to upload the object to the Oracle Storage Cloud Service container. " \
                             "The HTTP Code: %s..." % (http_code)
            upload_result.set_status_code(cloud_storage_controller.ERROR_UPLOAD)

        upload_result.set_message(status_message)
        upload_result.set_http_code(http_code)


# Response class for pyCurl upload and download artifacts
class CloudStorageResultResponse:
    """
    Class which handles the result of cloud storage handler

        Members:
            status_code: the status code which indicates the success or failures
            message: the status message of cloud storage operation
            http_code: the http code returned from cloud storage server if exist
            http_response: the http response object from cloud storage server if exist
    """

    def __init__(self, status_code=None, message=None, http_code=None, http_response=None):
        self.status_code = status_code
        self.message = message
        self.http_code = http_code
        self.http_response = http_response

    def get_status_code(self):
        return self.status_code

    def set_status_code(self, status_code):
        self.status_code = status_code

    def get_message(self):
        return self.message

    def set_message(self, message):
        self.message = message

    def get_http_code(self):
        return self.http_code

    def set_http_code(self, http_code):
        self.http_code = http_code

    def get_http_response(self):
        return self.http_response

    def set_http_response(self, http_response):
        self.http_response = http_response
