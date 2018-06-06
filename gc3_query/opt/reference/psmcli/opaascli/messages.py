# Copyright (c) 2015 Oracle and/or its affiliates. All rights reserved.
# created by sahit.gollapudi

import os
import sys
import json
from collections import OrderedDict


#################################################
######## Description and help Messages ##########
#################################################
class Messages(object):
    # Space is required after the script name.
    OPAAS_CLI_TOP_LEVEL_SCRIPT_NAME = "psm "
    OPAAS_CLI_USAGE = "psm <service> <command> [parameters]"
    OPAAS_CLI_DESCRIPTION = 'A command-line tool to manage Oracle platform services (such as Java Cloud Service or Application Container Cloud Service) on Oracle Cloud Infrastructure and Oracle Cloud Infrastructure Classic.'
    OPAAS_CLI_HELP_DESC = 'Show help'
    # version
    OPAAS_CLI_VERSION_HELP_DESC = 'Show current version of psm client'
    OPAAS_CLI_VERISON_DISPLAY_MSG = 'Oracle PaaS CLI client \nVersion %s'
    # setup
    OPAAS_CLI_SETUP_DESC = 'Configure psm client options'
    # Update
    OPAAS_CLI_UPGRADE_DESC = 'Update psm client to latest version'
    # log-level-description
    OPAAS_CLI_LOG_LEVEL_DESC = 'View or update psm client log level'
    # output format description
    OPAAS_CLI_OUTPUT_FORMAT_HELP_DESC = 'Desired output format. Valid values are %s'
    # wait-until-complete description
    OPAAS_CLI_WAIT_UNTIL_COMPLETE_DESC = "Wait until the command is complete. Valid values are %s. Default is 'false'."
    # Tear down description
    OPAAS_CLI_TEAR_DOWN_DESC = "Remove configured psm client options"

    # Keys for parsing
    OPAAS_CLI_SETUP_KEY = 'setup'
    OPAAS_CLI_UPGRADE_KEY = 'update'
    OPAAS_CLI_LOG_LEVEL = 'log'
    OPAAS_CLI_TEAR_DOWN_KEY = 'cleanup'
    # Used for multiple purposes. Check bfr changing this value.
    OPAAS_CLI_HELP_KEY = 'help'

    OPAAS_CLI_JSON_KEY = 'json'
    OPAAS_CLI_TEXT_KEY = 'text'
    OPAAS_CLI_RETYPE_PWD = 'Retype %s: '

    # Keys for Help display
    OPAAS_CLI_HELP_DESCRIPTION = 'DESCRIPTION'
    OPAAS_CLI_HELP_SYNOPSIS = 'SYNOPSIS'
    OPAAS_CLI_HELP_SERVICES = 'AVAILABLE SERVICES'
    OPAAS_CLI_HELP_COMMANDS = 'AVAILABLE COMMANDS'
    OPAAS_CLI_HELP_PARAMETERS = 'AVAILABLE PARAMETERS'
    OPAAS_CLI_HELP_EXAMPLES = 'EXAMPLES'
    OPAAS_CLI_HELP_PAYLOAD = 'SAMPLE PAYLOAD'


    # for argparse display arguments headers
    OPAAS_CLI_RENAME_POSITIONAL_ARG = 'Available services'
    OPAAS_CLI_RENAME_OPTIONAL_ARG = 'Optional arguments'

    # General Display Messages
    OPAAS_CLI_WARNING_MSG = "WARNING"
    OPAAS_CLI_INFO_MSG = 'INFO'
    #OPAAS_CLI_JOB_STATUS_ID_MSG = 'Job ID : %s. Please use view-operation-status command to view details.\n'
    OPAAS_CLI_JOB_STATUS_ID_MSG = 'Job ID : %s\n'
    OPAAS_CLI_UPGRADE_WARNING_MSG = "A new version of psm client is available. Please run 'psm update' to update to the latest version."
    OPAAS_CLI_SETUP_SUCCESS_MSG = "'psm setup' was successful. Available services are:\n\n"
    OPAAS_CLI_HELP_SAMPLE_PAYLOAD = "Required properties are indicated as \"required\". Replace in the actual payload with real values.\n"
    OPAAS_CLI_WAITING_FOR_COMPLETE = "Waiting for the job to complete... (it cannot be cancelled)\n"
    OPAAS_CLI_OPERATION_COMPLETED = "Command completed with status [%s].\n"

    # configure msgs
    OPAAS_CLI_WARN_OUTPUT_FORMAT_MSG = "\nWarning: Invalid output format. Valid values are %s. Defaulting to 'json'."
    OPAAS_CLI_WARN_LOG_LEVEL_MSG = "Warning: Invalid log level. Valid values are %s\n"
    OPAAS_CLI_WARN_TEARDOWN_FORCE_MSG = "Warning: Invalid force value. Valid values are %s\n"
    OPAAS_CLI_INFO_LOG_LEVEL_UPDATE_MSG = "Successfully updated the log level to '%s'\n"
    OPAAS_CLI_INFO_CURRENT_LOG_LEVEL_MSG = "Current log level is '%s'\n"
    OPAAS_CLI_TEAR_DOWN_PROMT_MSG = "All configuration and data created by 'psm setup' will be removed.\nProceed (y/n)? "
    OPAAS_CLI_TEAR_DOWN_RESPONE_MSG = "Your response ('{0}') was not one of the expected responses: {1}\n"
    OPAAS_CLI_TEAR_DOWN_SUCCESS_MSG = "Cleanup successful"
    OPAAS_CLI_TEAR_DOWN_SUCCESS_DISPLAY = OPAAS_CLI_TEAR_DOWN_SUCCESS_MSG + ". To use the psm client again, configure it using 'psm setup'.\n"
    OPAAS_CLI_OAUTH_CLIID_CLISECRET_MSG = "Use OAuth? [n]: "

    # General Logger Info Msgs
    OPAAS_CLI_CHK_CONN = "Checking connection authorization"
    OPAAS_CLI_DOWNLOAD_CATALOG = "Downloading the catalogs"
    OPAAS_CLI_DOWNLOAD_CATALOG_SUCCESS = "Successfully downloaded catalog"
    OPAAS_CLI_DOWNLOAD_KIT = "Downloading the latest kit"
    OPAAS_CLI_DOWNLOAD_KIT_SUCCESS = "Successfully Downloaded the latest psm client zip"
    OPAAS_CLI_UPGRADE_LOG_SUCCESS = "Successfully updated the psm client"
    OPAAS_CLI_LATEST_VERSION_EXISTS = 'You already have the most up-to-date version of psm client installed on the system'
    OPAAS_CLI_UPGRADE_DOWNLOAD_KIT = "...Downloading the latest psm client distribution - version %s\n"
    OPAAS_CLI_UPGRADE_DOWNLOAD_KIT_UPGRADING = "...Updating psm client from version %s to %s\n"
    OPAAS_CLI_UPGRADE_SUDO_PROMPT = "...If prompted for password, enter sudo password\n"
    OPAAS_CLI_UPGRADE_CLEANING_UP = "...Cleaning up\n"
    OPAAS_CLI_REMOVE_DIR_SUCCESS = "Successfully deleted {0} directory."
    OPAAS_CLI_REMOVE_DIR_FAILURE = "Failed to delete the {0} directory: {1}."

    # Display msgs for custom commands.
    OPAAS_CLI_LONG_CMD_EXEC_INFO_MSG = "This command might take a while to complete...\n"
    OPAAS_CLI_ACCS_PUSH_SIZE_GREATER_THAN_LIMIT_WARNING = "Warning: Local archive size is : %s. For archive sizes greater than %s, uploading the archive to Oracle Storage Cloud and specifying --archive-url parameter is recommended.\n"

    # Deprecated msgs for commands.
    OPAAS_CLI_DEPRECATED = 'deprecated'
    OPAAS_CLI_PARAM_DEPRECATED_INFO = "Warning: parameter '%s' is deprecated"
    OPAAS_CLI_USE_PARAM_IF_DEPRECATED_INFO = "Use parameter '%s' instead."

    # Messages for custom command accs stream logs.
    OPAAS_CLI_RETRIEVE_URL_TOKEN_SUCCESS = "Successfully retrieved the oAuth token and log viewer url."
    OPAAS_CLI_CREATE_CONSUMER_GRP_SUCCESS = "Successfully created the consumer group."
    OPAAS_CLI_SUBCRIBE_CONSUMER_GRP_SUCCESS = "Successfully subscribed to the consumer group to stream the logs."
    OPAAS_CLI_MAX_RETRY_STREAM_LOG_MSG = "accs stream-logs: Reached max count of retries: %s. Exiting."
    OPAAS_CLI_NO_LOGS_TO_STREAM = "No logs to stream.\n"

    # Display msgs for git
    OPAAS_CLI_IS_GIT_REPOSITORY_PUBLIC_PROMPT = "Is git repository public? [n]: "
    OPAAS_CLI_GIT_CREDENTIAL_PROMPT = "Enter credentials for git repository url:"

#################################################
############### Error Messages ##################
#################################################
class ErrorMessages(object):
    # generic Error display msg
    OPAAS_CLI_LOGGER_ERROR_MSG = 'Error: %s'
    OPAAS_CLI_STD_ERR_MSG = 'Error: %s\n'

    OPAAS_CLI_KEYBOARD_INTERRUPT = "Initiated KeyBoardInterrupt"

    # Logger msgs.
    OPAAS_CLI_NO_DATA_FOUND = 'No data found'
    OPAAS_CLI_FILE_NOT_FOUND = 'File Not Found Error: %s'
    OPAAS_CLI_CONNECTION_ERROR = "Connection Error: %s"
    OPAAS_CLI_TIMEOUT_ERROR = "Timeout: %s"
    OPAAS_CLI_INVALID_URL_ERROR = "Invalid URL: %s"
    OPAAS_CLI_REQUESTS_ERROR = "Request Exception: %s"
    OPAAS_CLI_DOWNLOAD_KIT_ERROR = "Error while downloading the kit. with response code: %s"
    OPAAS_CLI_UPGRADE_UNKNOWN_ARGS_ERROR = "%s unknown arguments for psm update."
    OPAAS_CLI_UPGRADE_LOG_ERROR = "Exception while updating the psm client. KeyBoardInterrupt/CommandError"
    OPAAS_CLI_UPGRADE_LOG_UNKOWN_ERROR = "Unknown error while updating the psm client."
    OPAAS_CLI_UPGRADE_LOG_BUILD_ERROR = "Previous build dir error."
    OPAAS_CLI_UPGRADE_PIP_RETRY_ERROR = "Could not update psmcli using pip3: %s. Retrying update using pip"
    OPAAS_CLI_UPGRADE_PIP_ERROR = "Exception while updating using pip: %s"
    OPAAS_CLI_NO_VERSION_FOUND_ERROR ='No client and catalog version found in the response.'
    OPAAS_CLI_UPGRADE_GENERIC_ERROR = "Response code: %s while trying to update the cli."
    OPAAS_CLI_UPGRADE_DOWNLOAD_KIT_LOCATION_ERROR = "The downloaded file location file_path is None."
    OPAAS_CLI_LOG_LEVEL_ERROR = "Please check the help by running 'psm log h'.\n"
    OPAAS_CLI_CONFIG_FILE_READ_ERROR = "Error while reading value from atoml_cfg file: %s"
    OPAAS_CLI_TEAR_DOWN_CRED_ERROR = "Error while removing credentials: {0}"
    OPAAS_CLI_CONFIG_DOWNLOAD_CATALOG_ERROR = "Failed to execute psm setup while trying to download catalogs"
    OPASS_CLI_VERSION_NOT_FOUND_ERROR = "CLI header key missing in the response header"
    OPASS_CLI_TOKEN_NOT_FOUND_ERROR = "Unable to retrieve the token."

    OPAAS_CLI_CHK_CONN_FAIL_ERROR = "Check connection failed with status code: %s"
    OPAAS_CLI_BAD_RESPONSE_ZIPFILE = "Bad Response: catalog zip file corrupted"
    OPAAS_CLI_TOKEN_EXPIRY_UPDATE_ERR = "Error in updating the access token expiry. Using Default token expiry value."

    # Configure Error Msgs
    OPAAS_CLI_PWD_MATCH_ERROR_DISPLAY = 'Passwords do not match. Try again.'
    OPAAS_CLI_FIELD_EMPTY_ERROR_DISPLAY = "'%s' can not be empty."
    OPAAS_CLI_DEFAULT_URI_ERROR_DISPLAY = "Please re-configure the default Uri, by running 'psm setup'."
    OPAAS_CLI_INVALID_IDENTITY_DOMAIN_ERR_DISPLAY = "No valid account or subscription for domain %s. Please re-run 'psm setup' and provide valid value for '%s'."
    OPAAS_CLI_OUTPUT_FORMAT_ERROR_MSG = "Invalid output format. Valid values are %s. Please re-enter valid value for '%s'."
    OPAAS_CLI_DNS_ERROR_DISPLAY = "DNS host name resolution failed for %s. Please re-run 'psm setup' and provide fully qualified host name for '%s'."
    OPAAS_CLI_UNAME_PWD_ERR_DISPLAY = "Username, Password and/or Identity domain are incorrect. Please re-enter."
    OPAAS_CLI_REGION_ERR_DISPLAY = "Invalid region. Valid values are %s. Please re-enter valid value for '%s'."
    OPAAS_CLI_GENERIC_SETUP_ERR_DISPLAY = "Please check values and re-run 'psm setup'."
    OPAAS_CLI_GENERIC_ERR_DISPLAY = "Setup failed. " + OPAAS_CLI_GENERIC_SETUP_ERR_DISPLAY
    OPAAS_CLI_GENERIC_SETUP_VALUES_ERR_DISPLAY = "Failed to establish connection. " + OPAAS_CLI_GENERIC_SETUP_ERR_DISPLAY
    OPAAS_CLI_UPGRADE_HELP_ERROR = 'Update help does not exist.'
    OPAAS_CLI_UPGRADE_GENERIC_DISPLAY = "Please run 'psm update' to update to the latest psm client distribution."
    OPAAS_CLI_SETUP_HELP_ERROR = 'Setup help does not exist.'
    OPAAS_CLI_SETUP_GENERIC_DISPLAY = "Please run 'psm setup' to configure psm client."
    OPAAS_CLI_TEARDOWN_HELP_ERROR = 'Cleanup help does not exist.'
    OPAAS_CLI_LOG_LEVEL_HELP_ERROR = 'Log help does not exist.'
    OPAAS_CLI_LOG_LEVEL_GENERIC_DISPLAY = "Please run 'psm log --level <level>' to update the log level.\n"
    OPAAS_CLI_UPGRADE_PIP_NOT_FOUND_ERROR = 'sudo: pip: command not found\n'
    OPAAS_CLI_UPGRADE_DNS_ERROR_DISPLAY = "DNS host name resolution failed for defaultURI '%s'. Please provide fully qualified host name and re-run 'psm setup'.\n"
    OPAAS_CLI_UPGRADE_FAILED_ERR_DISPLAY = 'Update failed.\n'
    OPAAS_CLI_SETUP_VERSION_ERR_DISPLAY = "Setup failed. " + OPAAS_CLI_SETUP_GENERIC_DISPLAY
    OPAAS_CLI_SETUP_GENERIC_MISSING_PARAMS_ERR_DISPLAY = "usage: psm %s [parameters]\npsm: error: argument %s: expected one argument\n"
    OPAAS_CLI_PROFILE_BASED_INVALID_PAYLOAD_ERR_DISPLAY = "Error: please provide valid payload. %s.\n"
    OPAAS_CLI_PROFILE_BASED_INVALID_ACCESS_TOKEN_ERR_DISPLAY = "Error: accessTokenServer cannot be empty. Please specify a value.\n"
    OPAAS_CLI_PROFILE_BASED_MISSING_VALUES_ERR_DISPLAY = "Error: missing one or more of the required values in the payload: %s, %s, %s\n"
    OPAAS_CLI_PROFILE_BASED_MISSING_VALUES_OAUTH_ERR_DISPLAY = "Error: missing one or more of the required values in the payload: %s, %s\n"
    OPAAS_CLI_PROFILE_BASED_FILE_NOT_FOUND_ERR_DISPLAY = "usage: psm setup [parameters]\npsm: error: argument -c/--atoml_cfg-payload: can't open '{msg}': [Errno 2] No such file or directory: '{msg}'\n"


    # Display error messages
    OPAAS_CLI_FAIL_JOB_ID = "Failed to get the Job ID: %s"
    OPAAS_CLI_CONNECTION_ERROR_DISPLAY = "Failed to connect to the server. %s"
    OPAAS_CLI_TIMEOUT_ERROR_DISPLAY = "Request timed out. %s"
    OPAAS_CLI_INVALID_URL_ERROR_DISPLAY = "Malformed URL. %s"
    OPAAS_CLI_CONFIG_CORRUPTED = "psm client configuration corrupted. Please re-run 'psm setup'.\n"
    OPAAS_CLI_STATUS_CODE_ERROR_DISPLAY = 'Status: %s Problem with the request. Exiting.\n'
    OPAAS_CLI_BAD_RESPONSE_ZIPFILE_DISPLAY = "psm setup failed while trying to download the catalog.\n"
    OPAAS_CLI_DOWNLOAD_KIT_CORRUPTED_DISPLAY = "Downloaded file corrupted. Exiting the psm update.\n"
    OPAAS_CLI_SHORT_OUTPUT_PARSING_ERROR_DISPLAY = "Exception while trying to format output for short format: {}"
    OPAAS_CLI_WAIT_COMMAND_FAILED = "Command failed, try 'psm %s operation-status -j {jobId}' for details\n"
    OPAAS_CLI_OPERATION_STATUS_RESPONSE_STATUS_MISSING = "Missing 'status' property in operation-status response"
    OPAAS_CLI_CATALOG_JOB_ID_MISSING = "Job Id does not exist in the response"
    OPAAS_CLI_WC_JOB_POLLING_ERROR = "Unable to get job status. Please use 'psm <service> operation-status -j <jobId>' to get the status."

    # Custom Command Error Msgs
    OPAAS_CLI_SPECIFY_ONE_ARGUMENT_ERROR = "specify only one of these parameters {}"
    OPAAS_CLI_NO_SUCH_FILE_EXISTS_ERROR = "argument {0}: can't open '{1}': No such file or directory: '{1}'"
    OPAAS_CLI_MAX_LIMIT_ERROR = "argument {0}: the max limit to upload the application is {1}: Failed to upload application '{2}'"
    OPAAS_CLI_ACCS_STREAM_LOG_ERROR = "Unable to stream logs. Please try again later."
    OPAAS_CLI_STREAM_LOGS_ERROR = "Error while trying to get logs. Status code: {0}: {1}."
    OPAAS_CLI_PARSING_TOPIC_PATTERN_ERROR = "Unable to get the topic pattern from the log viewer url."
    OPAAS_CLI_UNABLE_TO_CREATE_CONSUMER_GRP_ERROR = "Unable to create consumer group."
    OPAAS_CLI_NO_ACCESS_TOKEN_LOG_VIEWER_URL_ERROR = "Unable to retrieve access token and log viewer url."
    OPAAS_CLI_SUBSCRIPTION_FAILED_ERROR = "Failed to subscribe to the consumer group."

#################################################
############### Catalog Constants ###############
#################################################
class CatalogConstants(object):

    OUTPUT_FILTER = 'outputFilter'
    OFFSET = 'offset'
    SHOW_TABLE = 'showTable'
    INCLUDE_PROPERTIES = 'includeProperties'
    INCLUDE_PROP_NAME = 'name'
    INCLUDE_PROP_DISP_NAME = 'displayName'

#################################################################################
####################### CONSTANTS for Localization ##############################
#################################################################################
def get_supported_url_and_regions():
    default_uri = None
    regions_mapping = None
    script_dir = os.path.dirname(__file__)
    fileName = "supported-regions.json"
    rel_path = os.path.join(script_dir, fileName)
    try:
        with open(rel_path) as json_file:
            data = json.load(json_file, object_pairs_hook=OrderedDict)
        default_uri = data['defaultURI']
        regions_mapping = data['regions']
    except Exception as e:
        # this is a fallback if for any reason the above file is tampered or removed.
        default_uri = 'https://psm.region.oraclecloud.com'
        regions_mapping = {
                           'us':'us',
                           'emea':'europe',
                           'aucom':'aucom'
                           }

    return default_uri, regions_mapping

class LocalizationConstants(object):
    # the oracle psm cloud pub url, # default mapping to the selected region.
    Default_URI, RegionMapping = get_supported_url_and_regions()

    # Service types
    ACCS_SERVICE_TYPE = 'accs'

    # commands
    ACCS_PUSH = 'push'
    ACCS_VIEW_LOGS = 'view-logs'

    # Custom command execution.
    CustomCommandForService = {
                               ACCS_SERVICE_TYPE : {
                                         ACCS_PUSH : 'help/psm_accs_push_help.json'
                                         }
                               }

    # Add Custom Commands to the Service Catalog:
    AddCustomCommandToCatalog = {
                                    ACCS_SERVICE_TYPE : {
                                            ACCS_VIEW_LOGS : 'help/psm_accs_stream_log_help.json'
                                        }
                                }

    # BUG FIX: 27112221. Backward compatibility for service Types in CLI.
    ServiceMapping = {
                                'jaas' : 'jcs',
                                'dbaas' : 'dbcs'
        }
