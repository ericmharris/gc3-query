# Copyright (c) 2016 Oracle and/or its affiliates. All rights reserved.
# created by sahit.gollapudi
__author__ = "sahit"

import os
import sys
import getpass
import base64
import json
import uuid
import time
import shutil
import logging
import requests
from collections import OrderedDict
from urllib.parse import urlparse, quote
from datetime import datetime
try:
    from executor import RequestExecutor
    from utils import Utils
    from __init__ import __version__
    from opcservice import OPCService
    from messages import Messages, ErrorMessages, LocalizationConstants
    from exceptions import PSMUsageError, OSSUploadError, OSSDetailsError, AccsStreamLogError
    from internal.opc_cloud_storage_handler import OPCCloudStorageHandler
except:
    from .executor import RequestExecutor
    from .utils import Utils
    from .__init__ import __version__
    from .opcservice import OPCService
    from .messages import Messages, ErrorMessages, LocalizationConstants
    from .exceptions import PSMUsageError, OSSUploadError, OSSDetailsError, AccsStreamLogError
    from .internal.opc_cloud_storage_handler import OPCCloudStorageHandler

class CustomAccsPushExecutor(RequestExecutor):
    '''
        Custom Impl for Accs Push.
    '''
    def __init__(self, reqParamHandler, usage, prog):
        super().__init__(reqParamHandler)
        self.usage = usage
        self.prog = prog
        self.max_app_size = 5368709122 # 5 GB #262144000 #250 MB
        self.max_limit_accs = 1048576000 #1000 MB
        self.max_limit_archive_warning = 262144000 # 250 MB
        self.isGitAuthRequired = False
        self._git_username = ''
        self._git_password = ''
        self._git_repo_url = 'gitRepoUrl'
        self._git_username_lbl = 'git-username'
        self._git_password_lbl = "git-password"
        self._git_username_param = 'gitUserName'
        self._git_password_param = 'gitPassword'
        self._archive_path = 'archivePath'
        self._archive_url = 'archiveURL'
        self._storage_url_key = ''
        self._region = 'region'
        self._site = ''
        # container name is of the form 'identityDomain-public'
        self._container_name = "%s-public"
        self._subscriptionId = 'subscriptionId'
        self.archive_args_list = [self._archive_url, self._archive_path]

    def pre_execute_request(self):
        # if gitRepoUrl is passed then ask for git credentials
        if self._git_repo_url in self.reqParamHandler.cmd_params_values:
            self._prompt_git_credential()
            if self.isGitAuthRequired:
                self.reqParamHandler.cmd_params_values[self._git_username_param] = self._git_username
                self.reqParamHandler.cmd_params_values[self._git_password_param] = self._git_password

        #print(self.reqParamHandler.cmd_params_values)
        # validate for archivePath and archiveURL. Only one should be
        # specifed either archivePath or archiveUrl
        if all(elem in self.reqParamHandler.cmd_params_values for elem in self.archive_args_list):
            archive_args = map(lambda x: "-{0}/{1}".format(self.reqParamHandler.arg_parameter_list[x].alias_name, \
                                                              self.reqParamHandler.arg_parameter_list[x].argument_option_name), \
                                                              self.archive_args_list)
            err_msg = ErrorMessages.OPAAS_CLI_SPECIFY_ONE_ARGUMENT_ERROR.format(" or ".join(list(archive_args)))
            raise PSMUsageError(usage = "usage: %s" % self.usage, prog = self.prog, err_msg = err_msg)

        if self._archive_path in self.reqParamHandler.cmd_params_values:
            isArchivePathDir = False
            # 1) Check if archive path is a directory to be zipped
            # or it is a zip file.
            archive_path = self.reqParamHandler.cmd_params_values[self._archive_path]
            archive_path_arg = "-{0}/{1}".format(self.reqParamHandler.arg_parameter_list[self._archive_path].alias_name, \
                                                self.reqParamHandler.arg_parameter_list[self._archive_path].argument_option_name)
            # raise an exception if the path doesnt exist.
            if not os.path.exists(archive_path):
                err_msg = ErrorMessages.OPAAS_CLI_NO_SUCH_FILE_EXISTS_ERROR.format(archive_path_arg, archive_path)
                raise PSMUsageError(usage = "usage: %s" % self.usage, prog = self.prog, err_msg = err_msg)

            # FIX: BUG 27477118.
            # Store the filename as 'key', to be used in the cloud_storage_endpoint
            self._storage_url_key = os.path.basename(archive_path)

            # Store the region (if provided by the user) as 'site', to be used in the cloud_storage_endpoint
            if self._region in self.reqParamHandler.cmd_params_values:
                self._site = self.reqParamHandler.cmd_params_values[self._region]

            # Determine the storage URL, container, auth mechanism and max_upload_size
            response_json, max_upload_size = self._get_cloud_storage_details()
            # convert the max_upload size to bytes
            if max_upload_size is not None:
                self.max_limit_accs = self._utils.convert_size_to_bytes(int(max_upload_size))

            # Check if the given path is a dir.
            if os.path.isdir(archive_path):
                # create a zip in the temp dir: TODO
                isArchivePathDir = True
                if archive_path.endswith('/'):
                    archive_path = archive_path[:-1]
                temp_name = self._utils._tmp + os.sep + os.path.basename(archive_path)
                zip_extension = "zip"
                archive_path = shutil.make_archive(temp_name, zip_extension, archive_path)

            # 2) check if the zipped file size is less than equal to 5 GB.
            archive_path_size = os.stat(archive_path).st_size
            if archive_path_size > self.max_limit_accs:
                err_msg = ErrorMessages.OPAAS_CLI_MAX_LIMIT_ERROR.format(archive_path_arg, self._utils.get_human_readable_size(self.max_limit_accs), self.reqParamHandler.cmd_params_values['archivePath'])
                raise PSMUsageError(usage = "usage: %s" % self.usage, prog = self.prog, err_msg = err_msg)

            # display warning msg if size is greater than 250 MB
            if archive_path_size > self.max_limit_archive_warning:
                sys.stdout.write(Messages.OPAAS_CLI_ACCS_PUSH_SIZE_GREATER_THAN_LIMIT_WARNING % (self._utils.get_human_readable_size(archive_path_size), \
                                                                                                 self._utils.get_human_readable_size(self.max_limit_archive_warning)))
            # display a msg to the user as it takes time to execute
            sys.stdout.write(Messages.OPAAS_CLI_LONG_CMD_EXEC_INFO_MSG)
            # 3) Upload the file to the cloud storage and compute Archive URL TODO
            try:
                archive_url = self._upload_app_to_cloud(archive_path, response_json)

                # 4) on success, store the archiveUrl into the requestHandler object TODO
                self.reqParamHandler.cmd_params_values[self._archive_url] = archive_url
                # remove the archivePath from the dict.
                del self.reqParamHandler.cmd_params_values[self._archive_path]

                # Log the command to be executed after custom changes
                self.reqParamHandler.log_command_executed()
            finally:
                if isArchivePathDir:
                    os.remove(temp_name + "." + zip_extension)

        # 5) call the main execute_request which is commented below.
        self.execute_request()

    def _upload_app_to_cloud(self, archive_path, response_json):

        # TODO: remove these lines
        # Determine the storage URL, container and auth mechanism

        # build opc_cloud_json_args to upload the archive.
        opc_cloud_storage_json = OrderedDict()
        try:
            cloud_container = response_json['container']
            opc_cloud_storage_json['cloud_storage_url'] = response_json['storageURL']
            # BUG FIX: 27477118: For bmc: authToken is not sent in the response.
            # check for tempURL and add that to the payload.
            if 'authToken' in response_json:
                opc_cloud_storage_json['cloud_auth_token'] = response_json['authToken'] #None
            if 'tempURL' in response_json:
                opc_cloud_storage_json['temp_url'] = response_json['tempURL']
                opc_cloud_storage_json['object_key'] = response_json['objectKey']
            opc_cloud_storage_json['delete'] = True

            # if temp_url is provided then archive_url = object_key
            if 'temp_url' in opc_cloud_storage_json:
                archive_url = opc_cloud_storage_json['object_key']
            else:
                # If temp_url is not provided, the format for archiveUrl is container/uuid/filename. use the '/' for consistency
                archive_url = "/".join([cloud_container, str(uuid.uuid4()), os.path.basename(archive_path)])

            opc_cloud_storage_json['source'] = archive_path
            opc_cloud_storage_json['archive_url'] = archive_url
            opc_cloud_storage_handler = OPCCloudStorageHandler()
            upload_result = opc_cloud_storage_handler._upload_archive(opc_cloud_storage_json)

            if upload_result.get_status_code() == 0:
                # upload was successful
                logger.info("{0}: {1}".format(upload_result.get_http_code(), upload_result.get_message()))
                return archive_url
            else:
                logger.error("{0}: {1}".format(upload_result.get_http_code(), upload_result.get_message()))
                raise OSSUploadError(http_code = upload_result.get_http_code(), err_msg = upload_result.get_message())
        except KeyError as e:
            logger.error(str(e))
            raise OSSDetailsError()


    def _get_cloud_storage_details(self):
        # Headers
        headers = OrderedDict()
        identityDomain = self._utils.getValueFromConfigFile(self._utils.identity_domain)
        containerName = self._container_name % (identityDomain)
        headers[self._utils.authorization_header_key] = self._utils.getAuthToken()
        headers[self._utils.identity_domain_header_key] = identityDomain
        headers[self._utils.cli_request_key] = 'cli' # Value doesn't matter
        headers[self._utils.cli_header_version_key] = __version__
        subscriptionId = None

        if self._subscriptionId in self.reqParamHandler.cmd_params_values:
            subscriptionId = self.reqParamHandler.cmd_params_values[self._subscriptionId]

        opc_service = OPCService()
        # Get cloud Storage details
        request_url = self._utils.getValueFromConfigFile(self._utils.default_uri) + \
                        self._utils._cloud_storage_endpoint.replace('{' + self._utils.identity_domain + '}', identityDomain)

        # FIX: BUG 27477118.
        # append 'site'(if exists), 'container', 'key' as  query params
        # if 'site' is provided by the user
        if self._site:
            request_url = request_url + '?site=' + self._site + '&container=' + containerName + '&key=' +self._storage_url_key
        else:
            # if 'site' is not provided
            request_url = request_url + '?container=' + containerName + '&key=' +self._storage_url_key

        if subscriptionId:
            request_url = request_url + "&subscriptionId=" + subscriptionId

        response_json, max_upload_size = opc_service.get_details(method='GET',request_url=request_url, headers=headers)

        return response_json, max_upload_size

    def _prompt_git_credential(self):
        # prompts for git credentials.
        isGitRepoPublic = None
        isGitRepoPublic_prompt = lambda: input(Messages.OPAAS_CLI_IS_GIT_REPOSITORY_PUBLIC_PROMPT)
        isGitRepoPublic = isGitRepoPublic_prompt()

        if not isGitRepoPublic:
            isGitRepoPublic = self._utils._git_public_repo_response_no
        else:
            while isGitRepoPublic not in self._utils._git_public_repo_response_list:
                if not isGitRepoPublic:
                    isGitRepoPublic = self._utils._git_public_repo_response_no
                    break
                else:
                    sys.stdout.write(Messages.OPAAS_CLI_TEAR_DOWN_RESPONE_MSG.format(isGitRepoPublic, \
                                        self._utils.getStringFromList(self._utils._git_public_repo_response_list)))
                    isGitRepoPublic = isGitRepoPublic_prompt()

        if isGitRepoPublic.lower() == self._utils._git_public_repo_response_no:
            print(Messages.OPAAS_CLI_GIT_CREDENTIAL_PROMPT)
            userPrompt = lambda: (input("%s: " % self._git_username_lbl))
            user = userPrompt()
            # username cannot be empty.
            while not user:
                print(ErrorMessages.OPAAS_CLI_FIELD_EMPTY_ERROR_DISPLAY % self._git_username_lbl)
                user = userPrompt()
            pprompt = lambda: (getpass.getpass('%s: ' % self._git_password_lbl))
            passwd = pprompt()
            # Password cannot be empty.
            while not passwd:
                print(ErrorMessages.OPAAS_CLI_FIELD_EMPTY_ERROR_DISPLAY % self._git_password_lbl)
                passwd = pprompt()
            self.isGitAuthRequired = True
            self._git_username = user
            self._git_password = passwd

class CustomAccsStreamLogExecutor(RequestExecutor):
    '''
        Custom command executor for accs stream-logs command
    '''
    def __init__(self, reqParamHandler, usage, prog):
        super().__init__(reqParamHandler)
        self.usage = usage
        self.prog = prog
        self.opc_service = OPCService()
        self._rest_post_api = 'POST'
        self._rest_get_api = 'GET'
        self._stream_logs_poll_frequency = 2  # seconds.
        self._stream_log_access_token = "access_token"
        self._log_viewer_url = "logViewerUrl"
        self._stream_log_partition = "partition"
        self._accept_type = "acceptType"
        self._cur_time = datetime.now()
        self._cur_time_stamp = time.mktime(self._cur_time.timetuple())
        self._consumer_group_instance_id = "instance_id"
        self._consumer_group_base_uri = "base_uri"
        self._consumer_group_url = "/consumers/%s_%s_%s" % (self._utils.getValueFromConfigFile(self._utils.identity_domain), \
                                                            self.reqParamHandler.cmd_params_values['name'], \
                                                            self._cur_time_stamp)
        self._consumer_group_subscription_url = "/assignments"
        self._post_new_offset_value_url = "%s/positions%s"
        self._stream_log_params_url = "/records?timeout=10000&amp;max_bytes=10000"
        self._log_content_type = 'application/vnd.kafka.json.v2+json'
        self._log_accept_header_type_kafka_v2 = 'application/vnd.kafka.v2+json'
        self._log_accept_header_type_kafka = 'application/vnd.kafka+json'
        self._log_accept_header_type_json = 'application/json'

    def pre_execute_request(self):
        headers = OrderedDict()
        defaultUri = self._utils.getValueFromConfigFile(self._utils.default_uri)
        method = self.reqParamHandler.method
        uri = self.reqParamHandler.uri
        content_type = self.reqParamHandler.contenttype

        # Set identityDomainId
        identityDomain = self._utils.getValueFromConfigFile(self._utils.identity_domain)
        uri = uri.replace('{identityDomainId}', identityDomain)

        # headers
        headers[self._utils.authorization_header_key] = self._utils.getAuthToken()
        headers[self._utils.identity_domain_header_key] = identityDomain
        headers[self._utils.cli_request_key] = 'cli' # Value doesn't matter
        headers[self._utils.cli_header_version_key] = __version__

        if content_type is not None:
            headers['Content-Type'] = content_type

        # Path param
        for param, value in self.reqParamHandler.cmd_params_values.items():
            paramType = self.reqParamHandler.param_dict[param]['paramType']
            type = self.reqParamHandler.param_dict[param]['type_name']
            if paramType == 'path':
                uri = uri.replace('{' + param + '}', value)

        request_url = defaultUri + uri
        response_json, _ = self.opc_service.get_details(method=method,request_url=request_url, headers=headers, details_type=self._utils._accs_stream_log_details_type)

        if isinstance(response_json, dict) and all(key in response_json for key in [self._stream_log_access_token, self._log_viewer_url, self._stream_log_partition]):
            self._create_consumer_group(response_json)
        else:
            logger.error(ErrorMessages.OPAAS_CLI_NO_ACCESS_TOKEN_LOG_VIEWER_URL_ERROR)
            raise AccsStreamLogError()

    def _create_consumer_group(self, stream_log_json):
        log_viewer_access_token = stream_log_json[self._stream_log_access_token]
        log_viewer_url = stream_log_json[self._log_viewer_url]
        log_viewer_partition = stream_log_json[self._stream_log_partition]

        # payload for the create consumer group. The consumer group will be
        # created with the format: consumer-group-HHMM
        payload_consumer_group = dict()
        payload_consumer_group["name"] = "consumer-group"
        payload_consumer_group["format"] = "json"
        payload_consumer_group["auto.offset.reset"] = "latest"
        #payload_consumer_group["auto.commit.enable"] = "false"

        # log_viewer url : https://LACD6D348A7E64D88B0CA59A3A1A46-psmdemo1.uscom-central-1.c9dev1.oc9qadev.com:443/restproxy/topics/psmdemo1-LACD6D348A7E64D88B0CA59A3A1A46
        # parse the URL to construct the consumer group URL
        get_url_and_topic_pattern = log_viewer_url.split('/topics/')

        self._consumer_group_url = get_url_and_topic_pattern[0] + self._consumer_group_url
        #print (self._consumer_group_url)

        # headers
        headers = dict()
        # The token is of the type_name "Bearer token"
        headers[self._utils.authorization_header_key] = log_viewer_access_token
        headers['Content-Type'] = self._log_content_type
        headers['Accept'] = ",".join([self._log_accept_header_type_kafka_v2, self._log_accept_header_type_kafka, self._log_accept_header_type_json])

        headers[self._utils.cli_request_key] = 'cli' # Value doesn't matter
        headers[self._utils.cli_header_version_key] = __version__

        response_json, _ = self.opc_service.get_details(method = self._rest_post_api, request_url = self._consumer_group_url, headers=headers, \
                                                        data=json.dumps(payload_consumer_group), details_type=self._utils._accs_stream_log_details_type)

        if isinstance(response_json, dict) and all (key in response_json for key in [self._consumer_group_instance_id, self._consumer_group_base_uri]):
            #logger.debug(Messages.OPAAS_CLI_CREATE_CONSUMER_GRP_SUCCESS)
            self._subscribe_consumer_group(response_json, headers, get_url_and_topic_pattern, log_viewer_partition)
        else:
            logger.error(ErrorMessages.OPAAS_CLI_UNABLE_TO_CREATE_CONSUMER_GRP_ERROR)
            raise AccsStreamLogError()

    def _subscribe_consumer_group(self, consumer_grp_create_response_json, headers, get_url_and_topic_pattern, log_viewer_partition):
        consumer_group_base_uri = consumer_grp_create_response_json[self._consumer_group_base_uri]
        self._consumer_group_subscription_url = consumer_group_base_uri + self._consumer_group_subscription_url

        # get the topic pattern from the log_viewer_url.
        if len(get_url_and_topic_pattern) < 2:
            logger.error(ErrorMessages.OPAAS_CLI_PARSING_TOPIC_PATTERN_ERROR)
            raise AccsStreamLogError()

        # remove the accept type_name from the header.
        del headers['Accept']
        # data is the payload that needs to be sent with the request.
        data = dict()
        data["topic"] = get_url_and_topic_pattern[1]
        data["partition"] = log_viewer_partition

        payload = dict()
        payload["partitions"] = [data]

        method = self._rest_post_api

        status_code, _, errMsg = self.opc_service.execute_request(method=method, request_url=self._consumer_group_subscription_url, \
                                                                  headers=headers, data=json.dumps(payload))

        if (status_code and status_code >= 200 and status_code < 300) and errMsg is None:
            self._stream_logs(consumer_group_base_uri, headers, payload)
        else:
            # there was an error while trying to subscribe to the consumer grp.
            logger.error(ErrorMessages.OPAAS_CLI_SUBSCRIPTION_FAILED_ERROR)
            raise AccsStreamLogError()


    def _stream_logs(self, consumer_group_base_uri, headers, payload):
        log_viewer_url = consumer_group_base_uri + self._stream_log_params_url

        # maintain counter to identify the number of consecutive calls.
        counter = 0
        method = self._rest_get_api
        # add the accept type_name to the header and
        # remove the content type_name as its not needed
        headers['Accept'] = self._log_content_type
        del headers['Content-Type']

        # headers for posting new offset value.
        headers_post_new_offset = dict()
        headers_post_new_offset[self._utils.authorization_header_key] = headers[self._utils.authorization_header_key]
        headers_post_new_offset['Content-Type'] = self._log_content_type
        headers_post_new_offset[self._utils.cli_request_key] = 'cli' # Value doesn't matter
        headers_post_new_offset[self._utils.cli_header_version_key] = __version__
        # payload for new offset value.
        payload_new_offset = dict()

        # disable the warnings for ssl verification.
        # requests.packages.urllib3.disable_warnings()
        # Fetch logs for application topic. The logs are polled every 2 seconds
        # the logs are displayed on the console (similar to tail -f).
        # if there is no response for 30 consecutive polls, exit gracefully.
        offset_bfr_reset = 0
        new_offset_value = 0
        default_offset_trigger = 2000
        post_new_offset = False
        isNewOffsetSet = False
        offset_reset_succeeded = False
        is_offset_start_beginning = False
        retries = 30
        show_log_if_set_new_offset_fails = False
        while True:
            # Counter has reached max count with no response consecutively. break.
            if counter == retries:
                logger.debug(Messages.OPAAS_CLI_MAX_RETRY_STREAM_LOG_MSG % counter)
                sys.stdout.write(Messages.OPAAS_CLI_NO_LOGS_TO_STREAM)
                break

            # reset the logs with new offset value.
            if post_new_offset:
                if is_offset_start_beginning:
                    self._post_new_offset_value_url = self._post_new_offset_value_url % (consumer_group_base_uri, '/beginning')
                    payload_new_offset = payload
                else:
                    payload_new_offset['offsets'] = payload['partitions']
                    payload_new_offset['offsets'][0]['offset'] = new_offset_value
                    self._post_new_offset_value_url = self._post_new_offset_value_url % (consumer_group_base_uri, '')

                status_code, _, errMsg = self.opc_service.execute_request(method=self._rest_post_api, request_url=self._post_new_offset_value_url, \
                                                            headers=headers_post_new_offset, data=json.dumps(payload_new_offset))
                if (status_code and status_code < 200 and status_code > 300):
                    show_log_if_set_new_offset_fails = True

                post_new_offset = False
                isNewOffsetSet = True

            _, response, errMsg = self.opc_service.execute_request(method=method, request_url=log_viewer_url, headers=headers)

            # if the errMsg is not none or no response, it means there was an while trying to poll
            # logs. and hence increment the counter and continue with the polling.
            if errMsg is not None or not response or (response and response.status_code >= 300):
                if response:
                    logger.error(ErrorMessages.OPAAS_CLI_STREAM_LOGS_ERROR.format(response.status_code, response.content.decode('ascii')))
                    response_error_json = response.content.decode('ascii')
                    if response_error_json:
                        sys.stderr.write(response_error_json + "\n")
                raise AccsStreamLogError()

            try:
                output = response.json(object_pairs_hook=OrderedDict)
            except:
                if self._utils.isNotBlank(response.content):
                    output = response.content
                    if isinstance(output, bytes):
                        output = output.decode('ascii')
                else:
                    output = response.reason if self._utils.isNotBlank(response.reason) else response.text

            # the output is of list type_name with jsons. and parse the output
            # to just display the value key of each jsons for the log.
            if output and isinstance(output, list):
                counter = 0 if retries == 30 else 0
                for item in output:
                    if isinstance(item, dict):
                        # check for offset. if returned offset is greater than 2000, then
                        # offset = item['offset'] - 2000. post the new offset.
                        #  and subsequently check if the offset returned
                        # is less than the old offset value. if not then keep querying
                        # until the returned offset is less than the old offset value and then
                        # show the log and recalculate the new offset value
                        # if the offset returned is less than 2000, then POST the new offset to
                        # the beginning of the logs. And show the logs from the start.
                        if 'offset' in item and not offset_reset_succeeded:
                            if item['offset'] >= default_offset_trigger and not isNewOffsetSet:
                                new_offset_value = item['offset'] - default_offset_trigger
                                offset_bfr_reset = item['offset']
                                post_new_offset = True
                                break
                            elif item['offset'] < default_offset_trigger and not isNewOffsetSet:
                                post_new_offset = True
                                is_offset_start_beginning = True
                                break
                            # once the new Offset is set, check for the offset value returned is greater
                            # than the previous offset returned.
                            if isNewOffsetSet and not show_log_if_set_new_offset_fails and not is_offset_start_beginning:
                                if item['offset'] >= offset_bfr_reset:
                                    retries = 15
                                    counter += 1
                                    break;
                                else:
                                    offset_reset_succeeded = True
                                    retries = 30

                        if 'value' in item:
                             sys.stdout.write(item['value'] + "\n")
            else:
                # no response. increment the counter.
                counter += 1
                # wait for 2 seconds bfr polling the logs for another time.
                # wait for 2 seconfs if there is no output returned.
                time.sleep(self._stream_logs_poll_frequency)

#=================CONSTANTS==================#
# Custom impl Class Mapping:
CUSTOM_IMPL_MAP = {
                    LocalizationConstants.ACCS_SERVICE_TYPE : {
                                LocalizationConstants.ACCS_PUSH : CustomAccsPushExecutor,
                                LocalizationConstants.ACCS_VIEW_LOGS : CustomAccsStreamLogExecutor
                            }
}

logger = logging.getLogger(__name__)
