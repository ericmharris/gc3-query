# Copyright (c) 2015 Oracle and/or its affiliates. All rights reserved.
# created by sahit.gollapudi

import configparser as ConfigParser
import io
import json
import keyring
import os
import colorama
import platform
import re
import logging
import time
from datetime import datetime
from collections import OrderedDict
from pkg_resources import parse_version
from builtins import property
try:
    from exceptions import OpaasConfigError
    from messages import LocalizationConstants, ErrorMessages, Messages
    from __init__ import __version__
except:
    from .exceptions import OpaasConfigError
    from .messages import LocalizationConstants, ErrorMessages, Messages
    from .__init__ import __version__


#=== CLASSES ==================================================================

class ReadConfigFile(ConfigParser.RawConfigParser):
    """
    based on ConfigParser from the standard library, modified to parse toml_cfg
    files without sections.
    """

    def read(self, filename):
        text = open(filename).read()
        f = io.StringIO("[%s]\n" % NOSECTION + text)
        self.readfp(f, filename)

    def getoption(self, option):
        'get the value of an option'
        return self.get(NOSECTION, option)


    def getoptionslist(self):
        'get a list of available options'
        return self.options(NOSECTION)


    def hasoption(self, option):
        """
        return True if an option is available, False otherwise.
        (NOTE: do not confuse with the original has_option)
        """
        return self.has_option(NOSECTION, option)

    def write(self, fp):
        """
        overriding the default configparser to fit the need without section.
        Write the items from the default section manually and then remove them
        from the data. They'll be re-added later.
        """
        try:
            default_section_items = self.items(NOSECTION)
            self.remove_section(NOSECTION)

            for (key, value) in default_section_items:
                fp.write("{0} = {1}\n".format(key, value))

            # fp.write("\n")
        except ConfigParser.NoSectionError:
            pass

        ConfigParser.RawConfigParser.write(self, fp)
        self.add_section(NOSECTION)
        for (key, value) in default_section_items:
            self.set(NOSECTION, key, value)



class Utils(object):
    # a general class to get toml_cfg values and general utility apis.

    DATA_TYPES = {
            str: 'string',
            float: 'float',
            int: 'integer',
            'bool': 'boolean',
            'custom_bool': 'boolean',
            json.loads:'json',
            'FileType(\'r\')':'file',
            'list': '(list) (space separated)',
    }

    def __init__(self):
        self._readConfigFile = ReadConfigFile()
        usrHome = os.path.expanduser('~')

        # values for build no.
        self._build_version_key = 'X-PSM-CLI-ARTIFACT-VERSIONS'
        self._cli_request_key = 'X-PSM-CLI-REQUEST'
        self._cli_header_version_key = 'X-PSM-CLI-VERSION'
        self._version_split_token = '::'

        # identityDmain request header param name
        self._identity_domain_header_key = 'X-ID-TENANT-NAME'
        self._authorization_header_key = 'Authorization'

        # header values:
        self._location = 'Location'
        # accs push max upload size header
        self._max_archive_upload_size = 'MaximumArchiveSize-MB'

        # setup values
        self.opcDir = usrHome + "/.psm"
        self.opc_data_dir_name = 'data'
        self.opc_log_dir_name = 'log'
        self.opc_conf_dir_name = 'conf'
        self.subOpcDir = [self.opc_conf_dir_name, self.opc_data_dir_name, self.opc_log_dir_name]
        self._cli_keyring_name = 'psm-cli'
        self._cli_user_passwd = 'psm-api-passwd'

        ## values for output format
        self._output_value_json = 'json'
        self._output_value_short = 'short'
        self._output_value_html = 'html'

        # Labels
        self._username_lbl = 'Username'
        self._pwd_lbl = 'Password'
        self._identity_domain_lbl = 'Identity domain'
        self._display_region_lbl = 'Region [us]'
        self._outputFormat_lbl = 'Output format [{0}]'.format(self.default_output_value)

        # values stored in conf.
        self._username = 'username'
        self._passwd = 'password'
        self._identityDomain = 'identityDomain'
        self._default_uri = 'defaultURI'
        self._outputFormat = 'outputFormat'
        self._log_level = 'logLevel'

        self._setupList = [self._identity_domain_lbl, self._display_region_lbl , self._outputFormat_lbl]
        self._confFile = "/" + self.opc_conf_dir_name + "/setup.conf"
        self._dataFile = "/" + self.opc_data_dir_name + "/catalog.json"
        self._logFile = "/psmcli.log"

        # common values for output format for setup.
        self._json_object = '[JSON Object]'
        self._get_output_format_values = [self._output_value_short, self._output_value_json, self._output_value_html]
        self._get_wait_until_complete_values = ['true', 'false']
        self._get_region_values =  self.getStringFromList(list(LocalizationConstants.RegionMapping.keys()))
        self._default_log_level = INFO
        self._get_available_log_levels = [DEBUG.lower(), INFO.lower(), WARNING.lower(), ERROR.lower(), CRITICAL.lower()]

        # values for cliparser
        self._opc_data_dir = self.opcDir + "/" + self.opc_data_dir_name
        self._service_index_filename = "/service-index.json"
        self._opc_log_dir = self.opcDir + "/" + self.opc_log_dir_name
        self._output_format_override = 'outputFormat'
        self._wait_until_complete = 'waitUntilComplete'
        self._wc_details_type = 'wc'

        # values for custom command output
        self._specific_commands = ['services', 'apps']

        # values for undo setup
        self._response_yes = 'y'
        self._response_no = 'n'
        self._response_list = [self._response_yes, self._response_no]

        # values for git public repository prompt
        self._git_public_repo_response_yes = 'y'
        self._git_public_repo_response_no = 'n'
        self._git_public_repo_response_list = [self._git_public_repo_response_yes, self._git_public_repo_response_no]

        # determine the platform
        self._system = platform.system()

        # values to store the downloaded client zip
        self._tmp_storage_linux = "/tmp/psmcli.zip"
        self._tmp_storage_win = "C:/temp/psmcli.zip"   # the / is being used here, as python will convert it.
        self._tmp = "C:/temp" if self.isWindows() else "/tmp"

        # arguments for the set-log-level
        self._log_level_parameter = ['--level', '-l']
        self._convert_camel_case = re.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')

        # arguments for teardown force.
        self._teardown_params = ['-f', '--force']
        self._teardown_force_param_values = ['true', 'false']

        # arguments for setup. toml_cfg payload
        self._config_payload_params = ['-c', '--toml_cfg-payload']
        self._profile_based_region = 'region'

        # storage cloud endpoint
        self._cloud_storage_endpoint = '/paas/service/apaas/api/v1.1/apps/{' + self._identityDomain + '}/storagedetails'

        # configur outh details
        self._oauth_client_id = "clientId"
        self._oauth_client_secret = "clientSecret"
        self._oauth_idcs_url = "accessTokenServer"
        self._oauth_access_token_expiry = "tokenExpiry"
        self._oauth_client_id_lbl = "Client ID"
        self._oauth_client_secret_lbl = "Client Secret"
        self._oauth_idcs_url_lbl = "Access Token Server [default]"
        self._oauth_details_type = "access_token"
        self._oauth_details = {
                self._oauth_client_id_lbl : self._oauth_client_id,
                self._oauth_client_secret_lbl : self._oauth_client_secret,
                self._oauth_idcs_url_lbl : self._oauth_idcs_url
            }
        self.setup_oauth_details = [self._oauth_client_id_lbl, self._oauth_client_secret_lbl, self._oauth_idcs_url_lbl]

        self._accs_stream_log_details_type = "view-logs"


    @property
    def get_available_log_levels(self):
        return self._get_available_log_levels

    @property
    def default_log_level(self):
        return self._default_log_level

    @property
    def output_format_override(self):
        return self._output_format_override

    @property
    def wait_until_complete(self):
        return self._wait_until_complete

    @property
    def tmp_storage_win(self):
        return self._tmp_storage_win

    @property
    def tmp_storage_linux(self):
        return self._tmp_storage_linux

    @property
    def service_index_filename(self):
        return self._service_index_filename

    @property
    def opc_data_dir(self):
        return self._opc_data_dir

    @property
    def opc_log_dir(self):
        return self._opc_log_dir

    @property
    def default_output_value(self):
        return self._output_value_short

    @property
    def get_output_format_values(self):
        return self._get_output_format_values

    @property
    def get_wait_until_complete_values(self):
        return self._get_wait_until_complete_values

    @property
    def get_region_values(self):
        return self._get_region_values

    @property
    def conf_file_name(self):
        # concatenate to give the full path as a string.
        return self.opcDir + self._confFile

    @property
    def data_file_name(self):
        # concatenate to give the full path as a string.
        return self.opcDir + self._dataFile

    @property
    def log_file_name(self):
        # concatenate to give the full path as a string.
        return self.opc_log_dir + self._logFile

    @property
    def conf_file(self):
        return self._confFile

    @property
    def data_file(self):
        return self._dataFile

    @property
    def log_file(self):
        return self._logFile

    @property
    def getsetuplist(self):
        return self._setupList

    @property
    def log_level(self):
        return self._log_level

    @property
    def log_level_argument(self):
        return self._log_level_parameter

    @property
    def teardown_params(self):
        return self._teardown_params

    @property
    def teardown_force_param_values(self):
        return self._teardown_force_param_values

    @property
    def config_payload_params(self):
        return self._config_payload_params

    @property
    def output_format(self):
        return self._outputFormat

    @property
    def identity_domain(self):
        return self._identityDomain

    @property
    def cli_keyring_name(self):
        return self._cli_keyring_name

    @property
    def username_lbl(self):
        return self._username_lbl

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._passwd

    @property
    def default_uri(self):
        return self._default_uri

    @property
    def region(self):
        return self._display_region_lbl

    @property
    def oauth_client_id(self):
        return self._oauth_client_id

    @property
    def oauth_client_secret(self):
        return self._oauth_client_secret

    @property
    def oauth_idcs_url(self):
        return self._oauth_idcs_url

    @property
    def cli_request_key(self):
        return self._cli_request_key

    @property
    def cli_header_version_key(self):
        return self._cli_header_version_key

    @property
    def identity_domain_header_key(self):
        return self._identity_domain_header_key

    @property
    def authorization_header_key(self):
        return self._authorization_header_key

    @property
    def build_version_key(self):
        return self._build_version_key

    @property
    def specific_commands(self):
        return self._specific_commands

    @property
    def oauth_details_type(self):
        return self._oauth_details_type

    @property
    def access_token_expiry(self):
        return self._oauth_access_token_expiry

    def get_public_identity_domain_url(self):
        # replace {0} with identity domain
        return "https://{0}.identity.oraclecloud.com/oauth/v1/token"

    def getStringFromList(self, list_values):
        return '[%s]'%(', '.join(list_values))

    def readConfigFile(self):
        # import configreader
        cp = self._readConfigFile
        if os.path.exists(self.conf_file_name):
            cp.read(self.conf_file_name)
            return cp;
        else:
            return None

    def getValueFromConfigFile(self, value):
        # reads the value from the toml_cfg value for specified key.
        cp = self.readConfigFile()
        if cp and value.lower() in cp.getoptionslist() and cp.getoption(value.lower()) is not None and cp.getoption(value.lower()):
            return cp.getoption(value.lower())
        else:
            logger.debug(ErrorMessages.OPAAS_CLI_CONFIG_FILE_READ_ERROR % value)
            raise OpaasConfigError

    def getValueConfigFileOrReturnsNone(self, value):
        # reads the value from the toml_cfg value for specified key.
        cp = self.readConfigFile()
        if cp and value.lower() in cp.getoptionslist():
            return cp.getoption(value.lower())
        else:
            return None

    def writeValueToConfigFile(self, key, value):
        # write the value to the toml_cfg file. either adds a value
        # if not present or overrides the current value.
        cp = self.readConfigFile()
        cp.set(NOSECTION, key, value)
        with open(self.conf_file_name, 'w') as configfile:
              cp.write(configfile)

    def writeTestValue(self, value):
        self.writeValueToConfigFile(self.log_level, value)

    def getAuthToken(self):
        # return the auth token that is stored in the keyring.
        user = self.getValueFromConfigFile(self.username)
        token = keyring.get_password(self.cli_keyring_name, user)
        if token is None:
            # raise toml_cfg error when there is no token
            raise OpaasConfigError
        return token

    def getUserPasswd(self):
        # return the user passwd for the psm api
        pwd = keyring.get_password(self.cli_keyring_name, self._cli_user_passwd)
        if pwd is None:
            raise OpaasConfigError
        return pwd

    def removeFilesFromDir(self, dir, filetype):
        # removes all the files in the directory based on the filetype.
        filelist = [ f for f in os.listdir(dir) if f.endswith(filetype) ]
        for f in filelist:
            os.remove(dir + "/" + f)

    def remove_config_dirs(self, dir_name):
        # remove all the toml_cfg dirs while doing psm undo setup
        try:
            for root, dirs, files in os.walk(dir_name, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.removedirs(dir_name)
            logger.info(Messages.OPAAS_CLI_REMOVE_DIR_SUCCESS.format(dir_name))
        except Exception as e:
            logger.info(Messages.OPAAS_CLI_REMOVE_DIR_FAILURE.format(dir_name, e))

    def isWindows(self):
        return self._system.lower() in ['windows', 'win32', 'win64']

    def isLinux(self):
        return self._system.lower() in ['linux', 'linux2']

    # OS X
    def isMac(self):
        return self._system.lower() in ['darwin']

    def get_existing_cli_artifacts_versions(self):
         existing_cli_version, last_updated_time, ctlg_version = self.parse_cli_artifacts_versions(self.getValueFromConfigFile(self.build_version_key))
         # Always return the installed client version for the existing_cli_version
         return __version__, last_updated_time, ctlg_version

    # this parses the build version key which has the
    # client version::last_updated_time::catalog_build_version
    # returns client_version, last_updated_time, catalog_build_version
    def parse_cli_artifacts_versions(self, build_version):
        build_version_split = build_version.split(self._version_split_token)
        client_version = build_version_split[0]
        last_updated_time = build_version_split[1]
        # Send None, if the catalog_build_version doesnt exists for prior versions before 1.1.9
        catalog_build_version = build_version_split[2] if len(build_version_split) == 3 else None
        return client_version, last_updated_time, catalog_build_version

    # concats the client version, and last update time
    # with the default split_token.
    # NOTE: order of the concat needs to be maintained.
    def concat_cli_artifacts_versions(self, client_version, last_updated_time, catalog_build_version):
        if catalog_build_version is not None:
            return self._version_split_token.join([client_version, last_updated_time, catalog_build_version.strip()])
        else:
            # This is for backward compatiblity of the CLI with a previous version of SM.
            return self._version_split_token.join([client_version, last_updated_time])


    def checkVersionEquality(self, existing_version, new_version):
        return parse_version(existing_version) == parse_version(new_version)

    # The order matters. check if version one is greater than two.
    def checkVersionGreaterThan(self, version_one, version_two):
        return parse_version(version_one) > parse_version(version_two)

    # to get the value of the client_version
    def get_existing_cli_version(self):
        return __version__

    # Get existing cli version from conf file
    def get_existing_file_cli_verion(self):
        existing_artifacts_versions = self.getValueConfigFileOrReturnsNone(self.build_version_key)
        if existing_artifacts_versions is None:
            return None
        else:
            client_version = existing_artifacts_versions.split(self._version_split_token)
            return client_version[0]

    # updates only catalog and last updated time if setup is run again.
    def checkCatalogTokensAndUpdate(self, existing_client_version, cli_artifacts_versions):
        if existing_client_version is None:
            self.writeValueToConfigFile(self.build_version_key, cli_artifacts_versions)
        else:
            new_client_version, new_last_updated_time, catalog_build_version = self.parse_cli_artifacts_versions(cli_artifacts_versions)
            self.writeValueToConfigFile(self.build_version_key, \
                                        self.concat_cli_artifacts_versions(existing_client_version, \
                                                                            new_last_updated_time, \
                                                                            catalog_build_version))

    # return response headers removing the authorization token.
    def get_response_header_with_no_auth(self, headers):

        if headers is not None:
            dict_header = OrderedDict(headers)
            for param in ['cloud_auth_token', 'Authorization', 'cloud_pwd']:
                if param in dict_header:
                    del dict_header[param]
            return dict_header
        # if nothing to delete return the default.
        return headers

    # return the Job Id match from the Location header
    def get_job_id_from_location_header(self, response_location):
         return re.match(r"(?P<joburl>.*/(job|opStatus)/)(?P<jobid>.[0-9]+)", response_location)

    # Get SM URL from region
    def get_public_domain_url(self, region_name):
        # if the region name doesnt exists in the mapping dict,
        # return the value entered.
        if region_name in LocalizationConstants.RegionMapping:
            # replace the public url with the region.
            public_url = LocalizationConstants.Default_URI.replace('region', LocalizationConstants.RegionMapping[region_name])
            return public_url
        else:
            # If region is not found in the RegionMapping,
            # check if the region SM URL starting with http|https.
            if re.search(r'^(http|https)://.*', region_name) is not None:
                return region_name
            else:
                # Invalid region entered.
                return None

    # convert the camelcase to lowercase seperated by '-'
    def convertCamelCase(self, value):
         return self._convert_camel_case.sub(r'-\1', value).lower()

    # change the value of the password if exists for logging purpose.
    def changeValueOfPwd(self, data):
        if bool(data):
            data_dict = data
            try:
                data_dict = self.changeValueOfPwdRecurrsive(json.loads(data))
            except:
                pass
            return data_dict
        else:
            return data

    def changeValueOfPwdRecurrsive(self, data_dict):
        for key, value in data_dict.items():
            if isinstance(value, dict):
                self.changeValueOfPwdRecurrsive(value)
            elif isinstance(value, list):
                for list_item in value:
                    self.changeValueOfPwdRecurrsive(list_item)
            elif any(value in key.lower() for value in ['pwd', 'password', 'passwd', 'cred']):
                data_dict[key] = "*******"

        return data_dict

    # this is to parse the value from the catalog for boolean values
    # which will return json standard output.
    def parseValueForBoolean(self, value):
        if value.lower() == 'false':
            return False
        elif value.lower() == 'true':
            return True

        return value

    # to check if given var is empty or not
    def isNotBlank(self, value):
        if value and value.strip():
            # value is not empty
            return True

        return False

    # convert string to json.
    def convertInputToJson(self, value):
        return_value = value
        try:
            data_dict = json.loads(value)
            if isinstance(data_dict, dict):
                return_value = data_dict
        except:
            pass

        return return_value

    # check for free size on disk
    def check_free_size_on_disk(target_dir, expected_size):
        '''
            Check for free space on the disk before download
        '''
        import pythonUtils.disk as disk
        import socket
        if not disk.verify_disk_free_space(target_dir, long(expected_size), socket.gethostname()):
            return False
        else:
            return True

    def get_human_readable_size(self, size, suffix='B'):
        for unit in ['','K','M','G','T','P','E','Z']:
            if abs(size) < 1024.0:
                return "%.0f %s%s" % (size, unit, suffix)
            size /= 1024.0
        return "%.0f %s%s" % (size, 'Y', suffix)

    def convert_size_to_bytes(self, size, suffix='M'):
        if suffix == 'M':
            return size *1024 * 1024

        return size

    def get_token_expiration_time(self, expires_in):
        currentDateTime = datetime.now()
        currentDateTimeStamp = time.mktime(currentDateTime.timetuple())
        # Add default expiry of 90 secs less than one hour.
        currentDateTimeStamp = currentDateTimeStamp + 3510
        if expires_in is not None:
            try:
                # subtracting 90 seconds for efficient REST API calls.
                expires_in = expires_in - (90 if expires_in > 180 else 0)
                currentDateTimeStamp = time.mktime(currentDateTime.timetuple())
                currentDateTimeStamp = currentDateTimeStamp + expires_in
            except:
                logger.info(ErrorMessages.OPAAS_CLI_TOKEN_EXPIRY_UPDATE_ERR)

        return currentDateTimeStamp

    def isAccessTokenExpired(self):
        token_expiry = self.getValueConfigFileOrReturnsNone(self.access_token_expiry)
        if token_expiry is not None:
            currentDateTime = datetime.now()
            currentTimeStamp = time.mktime(currentDateTime.timetuple())
            if currentTimeStamp > float(token_expiry):
                return True
        return False

    def persistTokenAndExpiryTime(self, access_token, expires_in):
        if access_token is not None:
            # Add Bearer to the access Token
            access_token = "Bearer " + access_token
            keyring.set_password(self.cli_keyring_name, self.getValueFromConfigFile(self.username), access_token)
            expiry_time = self.get_token_expiration_time(expires_in)
            self.writeValueToConfigFile(self.access_token_expiry, expiry_time)

class TerminalStyler(object):
    # A terminal color mechanism which has different options of colorizing the
    # text in the terminal. Using colorama to enable this. At present we need
    # only bold.

    def __init__(self):
        colorama.init(autoreset=True)

    def format_bold(self, msg):
        return (colorama.Style.BRIGHT + msg + colorama.Style.RESET_ALL)

    def format_green(self, msg):
        return (colorama.Fore.GREEN + msg + colorama.Style.RESET_ALL)

    def format_blue(self, msg):
        return (colorama.Fore.BLUE + msg + colorama.Style.RESET_ALL)

    def format_black(self, msg):
        return (colorama.Fore.BLACK + msg + colorama.Style.RESET_ALL)

    def format_red(self, msg):
        return (colorama.Fore.RED + msg + colorama.Style.RESET_ALL)


class FormatText(object):

    #====== FORMAT =======#
    HEADER = '\033[95m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[04m'

    #====== COLORS =======#
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    ORANGE = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    LIGHTGREY = '\033[37m'
    DARKGREY = '\033[90m'
    LIGHTRED = '\033[91m'
    LIGHTGREEN = '\033[92m'
    YELLOW = '\033[93m'
    LIGHTBLUE = '\033[94m'
    PINK = '\033[95m'
    LIGHTCYAN = '\033[96m'

    STYLER = TerminalStyler()

    def disable():
        HEADER = ''
        WARNING = ''
        FAIL = ''
        ENDC = ''

    @classmethod
    def formatgreen(cls, msg):
        # return (cls.GREEN + msg + cls.ENDC)
        return cls.STYLER.format_green(msg)

    @classmethod
    def formatblue(cls, msg):
        return cls.STYLER.format_blue(msg)

    @classmethod
    def formatblack(cls, msg):
        return cls.STYLER.format_black(msg)

    @classmethod
    def formatred(cls, msg):
        return cls.STYLER.format_red(msg)

    @classmethod
    def bold(cls, msg):
        return cls.STYLER.format_bold(msg)


#=== MODULE METHODS ================================================================

def get_log_filename():
    utils = Utils()
    if not os.path.exists(utils.opcDir):
        os.makedirs(utils.opcDir)
    if not os.path.exists(utils.opc_log_dir):
        os.makedirs(utils.opc_log_dir)

    return utils.log_file_name

def get_log_level():
    utils = Utils()
    cp = utils.readConfigFile()
    if cp and utils.log_level.lower() in cp.getoptionslist():
        # return the log leve in upper case for configuration.
        return cp.getoption(utils.log_level.lower()).upper()
    else:
        return INFO


#=== CONSTANTS ================================================================

logger = logging.getLogger(__name__)

#LOG LEVEL CONSTANTS
INFO = 'INFO'
DEBUG = 'DEBUG'
ERROR = 'ERROR'
CRITICAL = 'CRITICAL'
WARNING = 'WARNING'

# section name for options without section:
NOSECTION = 'NOSECTION'

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(module)s: %(message)s',
            'datefmt': '%b %d %H:%M:%S'
        },
    },
    'handlers': {
        'default': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': get_log_filename(),
            'maxBytes': 10485760,
            'backupCount': 10,
            'encoding': 'utf8'
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': get_log_level(),
            'propagate': True
        }
    }
}
