# Copyright (c) 2015 Oracle and/or its affiliates. All rights reserved.
# created by sahit.gollapudi, abhijit.jere
import requests
import sys
import io
import re
import os
import yaml
import json
import logging
import time
from collections import OrderedDict
from pkg_resources import parse_version
try:
    from exceptions import ResponseNullError, DataNotFoundError
    from formatter import OUTPUT_FORMATTER
    from utils import Utils, FormatText
    from opcservice import OPCService
    from messages import Messages, ErrorMessages
    from __init__ import __version__
except:
    from .exceptions import ResponseNullError, DataNotFoundError
    from .formatter import OUTPUT_FORMATTER
    from .utils import Utils, FormatText
    from .opcservice import OPCService
    from .messages import Messages, ErrorMessages
    from .__init__ import __version__

#=== CLASSES ================================================================

class AdditionalResponseValues(object):
    def __init__(self):
        self._operation_status_uri = None
        """
            :type operation_status_uri: str
            :param operation_status_uri: uri for the operation status rest endpoint 
        """
    @property
    def operation_status_uri(self):
        return self._operation_status_uri
    
    @operation_status_uri.setter 
    def operation_status_uri(self, value):
        self._operation_status_uri = value

class RequestParamHandler(object):
    # The object which holds the service name, cmd name 
    # and the parameter values for that cmd. 
    
    def __init__(self, srv_name, cmd_name,
                options_args_parsed,
                arg_parameter_list, cmd_dict,
                param_dict,additional_response_values):
        """
            :type srv_name: str
            :param srv_name: service name.
            
            :type cmd_name: str
            :param cmd_name: command name.
            
            :type options_args_parsed: namespace object
            :param options_args_parsed: holds the namespace object with the cmd line values.
            
            :type arg_parameter_list: dict
            :param arg_parameter_list: holds the instance of OPCArgument for all available parameters.
            
            :type method: str
            :param method: rest api method type.
            
            :type uri: str
            :param uri: url for the rest api.
            
            :type contenType: str
            :param contentType: contentType for post, put, delete operations..     
            
            :type param_dict: dict
            :param param_dict: values for that command parameters.
        """
        self.utils = Utils()
        self._srv_name = srv_name
        self._cmd_name = cmd_name
        self._cmd_list_dict = cmd_dict
        self._options_args_parsed = options_args_parsed
        self._arg_parameter_list = arg_parameter_list
        self._method = self._cmd_list_dict['method']
        self._uri = self._cmd_list_dict['uri'] 
        self._content_type = self._cmd_list_dict['contentType'] if 'contentType' in self._cmd_list_dict else None
        self._param_dict = param_dict
        self._cmd_params_values = {}
        # value modified if outputformat is specified at command level
        self._output_format_cmd_level = None
        # value modified if waitUntilComplete is specified at command level
        self._wait_until_complete_cmd_level = None
        # build the values from the args.
        self._build_option_value()
        self._additional_response_values = additional_response_values
    
    @property
    def output_format_cmd_level(self):
        return self._output_format_cmd_level
    
    @output_format_cmd_level.setter 
    def output_format_cmd_level(self, value):
        self._output_format_cmd_level = value
    
    @property
    def wait_until_complete_cmd_level(self):
        return self._wait_until_complete_cmd_level
    
    @wait_until_complete_cmd_level.setter 
    def wait_until_complete_cmd_level(self, value):
        self._wait_until_complete_cmd_level = value
        
    @property
    def command_dict_values(self):
        return self._cmd_list_dict
    
    @command_dict_values.setter
    def command_dict_values(self, value):
        self._cmd_list_dict = value 
    
    @property
    def srv_name(self):
        return self._srv_name
    
    @property
    def cmd_name(self):
        return self._cmd_name
    
    @property
    def options_args_parsed(self):
        return self._options_args_parsed
    
    @property
    def param_dict(self):
        return self._param_dict
    
    @property
    def method(self):
        return self._method
    
    @property
    def uri(self):
        return self._uri
    
    @property
    def contenttype(self):
        return self._content_type
    
    @property
    def cmd_params_values(self):
        return self._cmd_params_values
    
    @cmd_params_values.setter
    def cmd_params_values(self, value):
        self._cmd_params_values = value
    
    @property 
    def arg_parameter_list(self):
        return self._arg_parameter_list
    
    @arg_parameter_list.setter 
    def arg_parameter_list(self, value):
        self._arg_parameter_list = value
    
    @property 
    def additional_response_values(self):
        return self._additional_response_values
    
    @additional_response_values.setter 
    def additional_response_values(self, value):
        self._additional_response_values = value
        
    def _build_option_value(self):
        # this is to extract the values passed ib the command line
        # for the options specified for each command.
        # convert options_args_parsed using vars as its a namespace object
        args_parsed = vars(self.options_args_parsed)
        
        # check for output format at cmd level. if exists then set the value
        # for the executor to pass it on to the response handler.
        if "outputFormat" in self.command_dict_values:
            self.output_format_cmd_level = self.command_dict_values["outputFormat"]
        if self.utils.output_format_override in args_parsed and args_parsed[self.utils.output_format_override] is not None:            
            self.output_format_cmd_level = args_parsed[self.utils.output_format_override]
            logger.debug('the output format is overriden: %s', self.output_format_cmd_level)
         
        # check for waitUntilComplete at cmd level. if exists then set the value
        # for the executor to pass it on to the response handler. 
        if self.utils.wait_until_complete in args_parsed and args_parsed[self.utils.wait_until_complete] is not None:            
            self.wait_until_complete_cmd_level = args_parsed[self.utils.wait_until_complete]
            logger.debug('wait-until-complete is specified: %s', self.wait_until_complete_cmd_level)  
             
        # arg parameter list has the instance of OPCArgument.
        arg_parameter_list = self.arg_parameter_list
        for arg_instance in arg_parameter_list.values():
            name = arg_instance.dest_name
            if name in args_parsed:
                value = args_parsed[name]
                # reading the value of the args if its of instance file
                if isinstance(value, io.TextIOWrapper):
                    streamValue = value.read()
                    # initializing the value to None.
                    value = None
                    # JIRA FIX: PSM 15720: validating the payload syntactically 
                    json_error = False
                    yaml_error = False                    
                    try:
                        # read for json file input first.
                        value = json.loads(streamValue)                   
                    except ValueError as e:
                        json_error = True
                        logger.error("Error while parsing the input as json: %s", e)
                        logger.info("Trying to parse the file as Yaml.")
                    
                    # check if value empty, send content as is if its yaml.
                    if value is None or not isinstance(value, dict):
                        try:
                            yaml.load(streamValue)
                            value = streamValue
                        except yaml.YAMLError as exc:
                            yaml_error = True
                            logger.error("Error while parsing the input as yaml: %s", exc)
                    
                    if json_error and yaml_error:
                        raise SyntaxError("Error: File does not contain valid JSON or YaML.")
                    
                    '''
                    if value is None:
                        lines = streamValue.split('\n')
                        clean_lines = [l.strip() for l in lines if l.strip()]
                        value = ''.join(clean_lines)
                    '''
                # add each param name and value in to cmd params dict for executor to build the request.
                if value is not None:
                    self.cmd_params_values[name] = value
        
        # this is to add the hidden constant values to send it 
        # accross the rest endpoints.
        if bool(self.param_dict):
            for key, value in self.param_dict.items():
                if 'hiddenConstant' in value:
                    self.cmd_params_values[key] = value['hiddenConstant']
                # FIX: BUG 22736148. Sending a default value in the payload if 
                # the rest api requires an empty payload to be sent.
                if 'defaultValue' in value and key not in self.cmd_params_values:
                    self.cmd_params_values[key] = self.utils.parseValueForBoolean(value['defaultValue'])
                # ER: 23711216 Display a warning if the parameter is deprecated and 
                # check if the value needs to be ignored or parsed.
                if 'deprecated' in value and value['deprecated'] and key in self.cmd_params_values: 
                    self._parse_deprecate_param(key, value)
        
        # log the command executed          
        self.log_command_executed()
           
    def log_command_executed(self):
        # add the command executed to the log.
        logger.debug("command executed: %s", ' '.join([Messages.OPAAS_CLI_TOP_LEVEL_SCRIPT_NAME.strip(), self.srv_name, self.cmd_name, ' '.join(self.cmd_params_values.keys())]))

    def _parse_deprecate_param(self, key, value):
        deprecated_arguments, use_parameter_if_deprecated = ([] for i in range(2))
        # populate the arguments that are deprecated.
        if self.arg_parameter_list[key].argument_option_alias_name is not None:
            deprecated_arguments.append(self.arg_parameter_list[key].argument_option_alias_name)
        deprecated_arguments.append(self.arg_parameter_list[key].argument_option_name)
        # This change of supersededBy is to maintain the mapping of 
        # the deprecated parameter with the parameter mentioned in supersededBy
        if 'supersededBy' in value:
            superseded_by_name = value['supersededBy']
            # if superseded value, then show deprecated value and the value that can be used instead.
            if self.arg_parameter_list[superseded_by_name].argument_option_alias_name is not None:
                use_parameter_if_deprecated.append(self.arg_parameter_list[superseded_by_name].argument_option_alias_name)
            use_parameter_if_deprecated.append(self.arg_parameter_list[superseded_by_name].argument_option_name)
            if superseded_by_name not in self.cmd_params_values:
                # # BUG FIX: 27259031. Replace the deprecated param's value with the supersededBy param's value.
                self.cmd_params_values[superseded_by_name] = self.cmd_params_values[key]
                
            # ignore the deprecated param value. 
            del self.cmd_params_values[key]
                       
        sys.stdout.write('{0}. {1}\n'.format(Messages.OPAAS_CLI_PARAM_DEPRECATED_INFO % '/'.join(deprecated_arguments),
                                             Messages.OPAAS_CLI_USE_PARAM_IF_DEPRECATED_INFO % '/'.join(use_parameter_if_deprecated)
                                             if len(use_parameter_if_deprecated) > 1 else ""))   
    

#====== Response Handlers ========
class ResponseHandlerFactory(object):
    """
        A factory that returns the desired response handler
        based on the content_type
    """
    
    def __init__(self):
        pass

    def create_handler(self, applicationType):
        # We observed many custom media types for json, e.g. application/vnd.com.oracle.oracloud.provisioning.Pod+json
        # and application/vnd.com.oracle.oracloud.provisioning.Service+json. Using standard 'application/json' handler
        # for such instances.
        if Messages.OPAAS_CLI_JSON_KEY in applicationType:
            applicationType = 'application/json'
        elif Messages.OPAAS_CLI_TEXT_KEY in applicationType:
            applicationType = 'text/plain'
        else:
            # defaulting mediatype to 'text/plain' if an unknown media type is encountered.
            applicationType = 'text/plain'
        logger.debug("The Content-type: %s", applicationType)
        resolver = RESPONSE_HANDLERS[applicationType]
        return resolver()
   

# pub api to build the factory response resolver.
def create_response_handler(applicationType):
    return ResponseHandlerFactory().create_handler(applicationType)           


class BaseResponseHandler(object):
    """
        This class has the ability to parse the response based on the content
        type and will return the processed response with an error msg if any
        or returns the content from the response.
    """
    def __init__(self):
        self._utils = Utils()
    
    def _handle_response_error(self, respone):
        """
           to be implemented by the subclasses. By default it will raise 
           an Exception.
        """
        raise NotImplementedError("Not Implemented")

    def _handle_response_output(self, response):
        """
           to be implemented by the subclasses. By default it will raise 
           an Exception.
        """
        raise NotImplementedError("Not Implemented")
    
    def _format_response(self, data):
        """
           to be implemented by the subclasses. By default it will raise 
           an Exception.
        """
        raise NotImplementedError("Not Implemented")
            
class JSONResponseHandler(BaseResponseHandler):
    
    def _handle_response_output(self, response):
        # TODO: to work on the formatting of json if any unknown issues arise.
        try:
            output = response.json(object_pairs_hook=OrderedDict)  # {'output':'output'}
        except:
            if self._utils.isNotBlank(response.content):
                output = response.content
                if isinstance(output, bytes):
                    output = output.decode('ascii')
            else:
                output = response.reason if self._utils.isNotBlank(response.reason) else response.text 
        return output  
    
    def _handle_response_error(self, response):
        # TODO: to parse the error more generically for all error types
        error_content = None
        try:
            error_content = response.json()
        except:
            error_content = response.content.decode('ascii')
            
        if error_content:
            return self._format_response(error_content)
        return error_content   
    
    def _format_response(self, data):
        formatter = OUTPUT_FORMATTER[Messages.OPAAS_CLI_JSON_KEY](content=data)
        parsed_content = formatter._format_error_content()
        return ("\n%s" % parsed_content)

class TextResponseHandler(BaseResponseHandler):
    
    def _handle_response_output(self, response):
        # TODO: to work on the remaining parsing options if any
        try:
            content = response.content
            if isinstance(content, bytes):
                content = content.decode('ascii')
        except:
            content = response.reason if self._utils.isNotBlank(response.reason) else response.text 
        return content
    
    def _handle_response_error(self, response):
        reason = []
        response_reason = None
        if self._utils.isNotBlank(response.reason):
            response_reason = response.reason 
            reason.append(response.reason)
        if self._utils.isNotBlank(response.text):
            if response_reason is not None and response_reason.strip() == response.text.strip():
                pass                    
            else:
                reason.append(response.text)
        reason = '. '.join(reason)  
        if reason:
            return self._format_response(reason)
        return reason 
    
    def _format_response(self, data):
        formatter = OUTPUT_FORMATTER[Messages.OPAAS_CLI_TEXT_KEY](content=data) 
        parsed_reason = formatter._format_content()
        return ("%s" % parsed_reason)        

class XMLResponseHandler(BaseResponseHandler):
    pass

   
class ResponseHandler(object):
    # The object which holds HTTP response from REST endpoint 
    def __init__(self, response):
        """
            :type response: requests.Response
            :param response: HTTP response from REST endpoint                
        """            
        self._response = response
        self._utils = Utils()
        self._existing_client_version, self._existing_last_updated_time, self._existing_catalog_build_version = self._utils.get_existing_cli_artifacts_versions()
        self._existing_file_client_version = self._utils.get_existing_file_cli_verion()
        self._job_status_msg = Messages.OPAAS_CLI_JOB_STATUS_ID_MSG
        
    @property
    def response(self):
        return self._response

    def process_response(self, cmd_dict, cmd_name, output_format=None, wait_until_complete=False, service_name=None, additional_response_values=None):
        '''
        Process HTTP response and display output to the user in desired format
        '''      
        if self.response is None:
            raise ResponseNullError()    
        else: 
            response = self.response
            # BUG FIX: 22565495 Fix to read default content type. 
            applicationType = response.headers['Content-Type'] if 'Content-Type' in response.headers else 'text/plain'
            status_code = response.status_code
            
            response_handler = create_response_handler(applicationType)
            
            # check for codes less than 300. requests.codes has a list of error codes
            # that can be used to determine the nature of error. #TODO.
            if status_code >= 300:
                parsed_error = response_handler._handle_response_error(response)
                if status_code == 404:
                    if self._utils.isNotBlank(parsed_error):
                       logger.error(ErrorMessages.OPAAS_CLI_LOGGER_ERROR_MSG, parsed_error)
                       sys.stdout.write(ErrorMessages.OPAAS_CLI_STD_ERR_MSG % parsed_error)
                    else:
                        logger.error(ErrorMessages.OPAAS_CLI_NO_DATA_FOUND)
                        sys.stdout.write('%s\n'%ErrorMessages.OPAAS_CLI_NO_DATA_FOUND)
                else:  
                    logger.error(ErrorMessages.OPAAS_CLI_LOGGER_ERROR_MSG, parsed_error)
                    sys.stdout.write(ErrorMessages.OPAAS_CLI_STD_ERR_MSG % parsed_error)
                
                # checking the cli artifact versions to update the catalog.
                self.checkBuildNumAndUpdate(response)
                
                # BUG FIX: 22538243. Return error exit code. 
                sys.exit(1)
            else:
                output = response_handler._handle_response_output(response)        
                outFormatter = self._utils.getValueFromConfigFile(self._utils.output_format)

                # to route to the proper formatter based on content type.
                if 'json' not in applicationType:
                    outFormatter = 'text'
                                     
                formatter = OUTPUT_FORMATTER[outFormatter](output, cmd_dict, cmd_name, response.headers) if output_format is None else \
                                                            OUTPUT_FORMATTER[output_format](output, cmd_dict, cmd_name, response.headers)
                # display the output.
                stdout_output = formatter._format_content()
                if stdout_output:
                    sys.stdout.write('%s\n' % stdout_output)
                # display job id if exists for monitoring using view-operation-status.
                # if its short output format don't show the job id.
                if (output_format is not None and output_format != self._utils._output_value_short) or \
                    (output_format is None and outFormatter != self._utils._output_value_short):
                    self.display_job_id_for_monitoring_status(response.headers)
                    
                # look for the job Id in the response header
                job_id = self.display_job_id_for_monitoring_status(response.headers, returnJobId=True)
                # if 'wait_until_complete' is true then wait for the operation to be finished
                if wait_until_complete:
                    operation_status_uri = additional_response_values.operation_status_uri
                    # check if job_id, service_name and operation_status_uri is not none
                    if job_id is not None:                    
                        # read the default_uri and identity domain
                        default_uri = self._utils.getValueFromConfigFile(self._utils.default_uri)
                        identity_domain = self._utils.getValueFromConfigFile(self._utils.identity_domain)
                        
                        # populate the header
                        headers = OrderedDict()
                        headers[self._utils.authorization_header_key] = self._utils.getAuthToken()
                        headers[self._utils.identity_domain_header_key] = identity_domain   
                        headers[self._utils.cli_request_key] = 'cli' # Value doesn't matter
                        headers[self._utils.cli_header_version_key] = __version__
                        
                        # Populate the values for identityDomainId and  jobId from the conf file
                        url = default_uri+operation_status_uri.replace('{identityDomainId}', identity_domain).replace('{jobId}',str(job_id))
                        service = OPCService()         
                        sys.stdout.write(Messages.OPAAS_CLI_WAITING_FOR_COMPLETE)
                        # poll every 30 secs until the job is completed
                        while True:
                            # BUG FIX 27075604: adding the "time.sleep" before polling to ensure that the job is created 
                            time.sleep(30)
                            content, max_upload_size = service.get_details("GET", url, headers, None, None, None,self._utils._wc_details_type)                            # check if 'status' exists
                            if isinstance(content, dict) and "status" in content:
                                status = content["status"]
                                if status not in ["NEW","RUNNING"]:
                                    sys.stdout.write(Messages.OPAAS_CLI_OPERATION_COMPLETED % (status))
                                    # Exit with code 1 for scripting purposes
                                    if status not in ["SUCCEED"]:
                                        sys.exit(1)
                                    else:
                                        break
                            else:
                                # status property was not found in operation-status response
                                sys.stdout.write(ErrorMessages.OPAAS_CLI_WAIT_COMMAND_FAILED % (service_name))
                                logger.error(ErrorMessages.OPAAS_CLI_OPERATION_STATUS_RESPONSE_STATUS_MISSING)
                                sys.exit(1)
                    else:
                        logger.debug(ErrorMessages.OPAAS_CLI_CATALOG_JOB_ID_MISSING)
            # checking the cli artifact versions to update the catalog.
            self.checkBuildNumAndUpdate(response)
            
    
    # api to display the job id if it exists.
    def display_job_id_for_monitoring_status(self, headers, returnJobId=False): 
        response_location = headers[self._utils._location] if self._utils._location in headers else None
        if response_location is not None:
            try:
                # match the location header with the regex Job id as of now is numeric eval.
                match = self._utils.get_job_id_from_location_header(response_location)
                if match is None:
                    return
                job_id = match.group('jobid')
                if returnJobId:
                    return job_id
                # display jobId only if it exists
                if job_id:
                    sys.stdout.write(self._job_status_msg%job_id)    
            except Exception as e:
                logger.error(ErrorMessages.OPAAS_CLI_FAIL_JOB_ID, e)
                 
                    
    def checkBuildNumAndUpdate(self, response):
        cli_artifacts_versions = response.headers[self._utils.build_version_key] if self._utils.build_version_key in response.headers else None
        if cli_artifacts_versions is None:
            return
        service = OPCService()
        new_client_version, new_last_updated_time, new_catalog_build_version = self._utils.parse_cli_artifacts_versions(cli_artifacts_versions)
        # update only if the new catalog version is greater than the existing one.
        if self._existing_last_updated_time is None or \
                       self._utils.checkVersionGreaterThan(new_last_updated_time.strip(), self._existing_last_updated_time.strip()):
            
            # False is when the catalog is updated implicit.
            rest_request_status,artifacts_versions_values = service.callRestApiGetServiceTypes(False)
            if rest_request_status:
                self._utils.writeValueToConfigFile(self._utils.build_version_key, \
                        self._utils.concat_cli_artifacts_versions(self._existing_client_version.strip(), \
                                                                        new_last_updated_time.strip(), \
                                                                        new_catalog_build_version))            
        elif self._existing_catalog_build_version is None or \
                not self._utils.checkVersionEquality(self._existing_client_version, self._existing_file_client_version):
            # Maintain catalog_build_version and client_version for debugging purpose.
            self._utils.writeValueToConfigFile(self._utils.build_version_key, \
                self._utils.concat_cli_artifacts_versions(self._existing_client_version.strip(), \
                                                            self._existing_last_updated_time.strip(), \
                                                            new_catalog_build_version)) 
                             
        # display a message only if the new client version is greater than the existing one.
        if self._existing_client_version is not None and \
                       self._utils.checkVersionGreaterThan(new_client_version.strip(), self._existing_client_version.strip()):
            sys.stdout.write('%s: %s\n' % (FormatText.bold(Messages.OPAAS_CLI_WARNING_MSG), Messages.OPAAS_CLI_UPGRADE_WARNING_MSG))


#=== CONSTANTS ================================================================

RESPONSE_HANDLERS = {
    'application/json': JSONResponseHandler,
    'text/plain': TextResponseHandler,
    'application/xml' : XMLResponseHandler,
}

logger = logging.getLogger(__name__)
