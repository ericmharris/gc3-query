# Copyright (c) 2016 Oracle and/or its affiliates. All rights reserved.
# created by sahit.gollapudi

__author__ = "sahit"

import io
import json
import hashlib
from collections import OrderedDict

INT = "INT"
STR = "STR"
BOOL = "BOOL"
LONG = "LONG"
LIST = "LIST"

class CommonUtil(object):
    
    CLOUD_STORAGE_ACCESS_TEMP_URL = "TempURL"
    CLOUD_STORAGE_ACCESS_USR_PWD = "UsrPwd"
    CLOUD_STORAGE_ACCESS_AUTH_TOKEN = "AuthToken"
    CLOUD_STORAGE_HEADER_TOKEN = 'X-Auth-Token'
    CLOUD_DELETE_HEADER_KEY = 'X-DELETE-AFTER'
    CLOUD_DELETE_HEADER_VALUE = 1800 #30 mins
    
    def get_value_from_json(json_args, key, data_type=STR):
        """
        Return the value of a specified key in json_args. Return empty str if key does not exist
        :param json_args:
        :param key:
        :param data_type:
        :return:
        """
        try:
            if json_args[key] is None:
                return None
    
            if data_type == INT:
                return int(json_args[key])
            elif data_type == LONG:
                return int(json_args[key])
            elif data_type == STR:
                return str(json_args[key])
            elif data_type == BOOL:
                return bool(json_args[key])
            elif data_type == LIST:
                return list(json_args[key])
    
        except (KeyError, ValueError, TypeError):
            if data_type == INT or data_type == LONG:
                return 0
            elif data_type == STR:
                return ""
            elif data_type == BOOL:
                return False
            elif data_type == LIST:
                return list()
            else:
                return ""
            
    def _build_md5_checksum(self, file_name):
        return hashlib.md5(open(file_name, 'rb').read()).hexdigest()
    
    def get_cloud_storage_access_mechanism(self, cloud_url, payload):
        #BUG FIX: 27477118: going forward only tempURL will be used. rest is for backward compatiblity
        if all(param in cloud_url for param in ['temp_url_sig', 'temp_url_expires']) or 'temp_url' in payload:
            return self.CLOUD_STORAGE_ACCESS_TEMP_URL
        elif all(key in payload for key in ['cloud_user', 'cloud_pwd']):
            return self.CLOUD_STORAGE_ACCESS_USR_PWD
        else:
            return self.CLOUD_STORAGE_ACCESS_AUTH_TOKEN
    
    @property 
    def cloud_delete_header_key(self):
        return self.CLOUD_DELETE_HEADER_KEY
    
    # return response headers removing the authorization token.
    def get_response_header_with_no_auth(self, headers):
        
        if headers is not None:
            dict_header = OrderedDict(headers)
            for param in ['cloud_auth_token', 'Authorization', 'cloud_pwd', self.CLOUD_STORAGE_HEADER_TOKEN]:
                if param in dict_header:
                    dict_header[param] = "*******"
            return dict_header
        # if nothing to delete return the default.
        return headers
        
class StatusCodes(object):
    
    ERROR_UPLOAD = 201
    ERROR_DOWNLOAD = 202
    ERROR_DELETE_LOCAL_OBJECT = 203
    ERROR_DELETE_CLOUD_OBJECT = 204
    ERROR_NOT_AUTHORIZED = 205  # 401 http code
    ERROR_GET_LOCAL_FREE_SPACE = 206
    ERROR_VERIFY_CLOUD_OBJECT = 207
    ERROR_VERIFY_REMOTE_STORAGE_ROOT = 208
    ERROR_DOWNLOAD_VALIDATION = 209
    ERROR_SET_DATE = 210
    ERROR_SETUP_CLOUD_STORAGE = 211
    ERROR_GET_SIZE = 212
    ERROR_REMOTE_RESOURCE_NOT_FOUND = 213  # 404 http code
    # 214 error code can be used if a new error code is to be added
    ERROR_LIST_CLOUD_OBJECTS = 214
    ERROR_CANNOT_RESOLVE_REMOTE_HOST = 215  # 418 http code
    ERROR_SSL_EXCEPTION = 216  # 419 http code
    ERROR_NOT_ENOUGH_SPACE_ON_REMOTE_DEVICE = 217  # 413 http code
    ERROR_TIMEOUT = 218  # connection timeout
    ERROR_LOCAL_RESOURCE_NOT_FOUND = 219
    PARTIALLY_DELETED_CLOUD_OBJECT = 220  # Partially deleted the object in cloud storage
    ERROR_NOT_ENOUGH_SPACE_ON_LOCAL_STORAGE = 221
    ERROR_BULK_DELETE_CLOUD_OBJECTS = 222
    SUCCESS = 0
    FAIL = 1
    