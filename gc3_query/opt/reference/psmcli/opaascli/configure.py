# Copyright (c) 2015 Oracle and/or its affiliates. All rights reserved.
# created by sahit.gollapudi


import sys
import os
from argparse import ArgumentParser
import base64
import getpass 
import keyring
import requests
import pip 
import subprocess
import logging 
import json 
from requests.auth import _basic_auth_str
from collections import OrderedDict
try:
    from opcservice import OPCService
    from utils import Utils, FormatText, LOGGING_CONFIG, get_log_level
    from exceptions import UnknownArgumentError, OpaasDownloadFileError
    from messages import Messages, ErrorMessages
except:
    from .opcservice import OPCService
    from .utils import Utils, FormatText, LOGGING_CONFIG, get_log_level
    from .exceptions import UnknownArgumentError, OpaasDownloadFileError
    from .messages import Messages, ErrorMessages

# BUG FIX: 27920176 (pip 10.0.1 fix where the internal dir structure of pip was changed)
SUCCESS = 0
ERROR = 1
UNKNOWN_ERROR = 2
VIRTUALENV_NOT_FOUND = 3
PREVIOUS_BUILD_DIR_ERROR = 4
NO_MATCHES_FOUND = 23

# Logger
logger = logging.getLogger(__name__)

class Configure(object):    
    """
       It is called on 'psm setup' to configure the credentials
    """

    def __init__(self):        
        self.utils = Utils()
        # check to maintain this list from the utils.
        self.setupList = self.utils.getsetuplist 
        self.setupTable = {}

        self.opcDir = self.utils.opcDir
        self.subOpcDir = self.utils.subOpcDir

        self.confFileName = self.utils.conf_file_name 
        self.dataFileName = self.utils.data_file_name     
        self._service = OPCService()
        
        self.MAX_RETRIES = 2
        
        self.isOauth = False
        self.isSetupProfileBased = False
        
    def configureCredentials(self):
        # prompt the user with credentials
        user, passwd = self.login()                
        # get the input for the other setup values.
        self._prompt_setup_values()        
        # continue setup for OAuth
        self._prompt_setup_oauth()
        # continue to execute setup
        return self.execute_setup(user=user, passwd=passwd)        
                        
    def execute_setup(self, user=None, passwd=None):
        access_token = None
        # Get the current log level. if doesnt exist default the log level to Info 
        self.setupTable[self.utils.log_level] = get_log_level()
        
        # replace the Identity URL with the identity domain.
        if self.isOauth:
            self.setupTable[self.utils._oauth_idcs_url] = self.setupTable[self.utils._oauth_idcs_url].format(self.setupTable[self.utils.identity_domain])
        
        # create the directory for .opaas if it does not exists
        if not os.path.exists(self.opcDir):
            os.makedirs(self.opcDir)
        for dirname in self.subOpcDir:
            os.makedirs(self.opcDir + "/" + dirname, exist_ok=True)
                
        # validate the user credentials
        urlHostName = self.setupTable[self.utils.default_uri]
        identityDomain = self.setupTable[self.utils.identity_domain]
        if self.isOauth:
            access_token, expires_in = self._service.get_oauth_access_token(self.setupTable, user, passwd, False)
            access_token = "Bearer " + access_token
            self.setupTable[self.utils.access_token_expiry] = self.utils.get_token_expiration_time(expires_in)
        validationResult, user, passwd = self.getValidationCode(user, passwd, identityDomain, urlHostName, access_token)  
        
        # to get the value of the client_version if setup is run multiple times
        client_version = self.utils.get_existing_cli_version()
        
        # if validation is successful then write conf file. else return
        if validationResult:
            # if successful add the token to the keyring
            token = None
            if self.isOauth:
                token = access_token
            else:
                token = self.createToken(user, passwd) 
            # get the list of service catalogs
            # True is when the setup is run explicitly
            rest_request_status,cli_artifacts_versions = self._service.callRestApiGetServiceTypes(True,token,self.setupTable)
            
            if rest_request_status:
                if client_version is not None:
                    new_client_version, new_last_updated_time, catalog_build_version = self.utils.parse_cli_artifacts_versions(cli_artifacts_versions)
                    cli_artifacts_versions = self.utils.concat_cli_artifacts_versions(client_version, \
                                                                            new_last_updated_time, \
                                                                            catalog_build_version)
                self.setupTable[self.utils.build_version_key] = cli_artifacts_versions
                # add the token to the keyring
                keyring.set_password(self.utils.cli_keyring_name, user, token)
                # add the passwd to the keyring if its OAUTH. This is used
                # for refreshing OAuth token after expiring.
                if self.isOauth:
                    keyring.set_password(self.utils.cli_keyring_name, self.utils._cli_user_passwd, passwd) 
                # add the user to the config file: open with append mode or write new mode.
                mode = 'w' if os.path.exists(self.confFileName) else 'a'
                with open(self.confFileName, mode) as f:
                    f.write("%s=%s\n" % (self.utils.username, user))
                    for key, value in self.setupTable.items():
                       f.write("%s=%s\n" % (key, value))                
                f.close()
            else:
                # debug msg
                logger.debug(ErrorMessages.OPAAS_CLI_CONFIG_DOWNLOAD_CATALOG_ERROR)
                sys.exit(1) 
            
        else:
            sys.exit(1)        
    
    def _prompt_setup_values(self):
        # setup for identity domain, region and output format
        for inputKey in self.setupList:
            input_prompt = lambda: (input(inputKey + ": "))
            inpStr = input_prompt()
            if inputKey == self.utils._identity_domain_lbl:
                # get the identityDomain value.
                inpStr = self.getIdentityDomain(inpStr)
                inputKey = self.utils.identity_domain
            elif inputKey == self.utils._outputFormat_lbl:
                # checking for default outputformat
                if not inpStr:
                    inpStr = self.utils.default_output_value
                else:
                    while inpStr not in self.utils.get_output_format_values:
                        if not inpStr:
                            inpStr = self.utils.default_output_value
                            break
                        else:
                            print(ErrorMessages.OPAAS_CLI_OUTPUT_FORMAT_ERROR_MSG % (self.utils.getStringFromList(self.utils.get_output_format_values), \
                                                                                     self.utils._outputFormat_lbl))
                            inpStr = input_prompt()
                inputKey = self.utils.output_format
            elif inputKey == self.utils.region:
                # construct the default uri.
                inputKey = self.utils.default_uri
                while True:
                    inpStr = self.getRegion(inpStr)
                    if inpStr is None:
                        print(ErrorMessages.OPAAS_CLI_REGION_ERR_DISPLAY % (self.utils.get_region_values, self.utils.region))
                    else:
                        break             
                        
            self.setupTable[inputKey] = inpStr         
     
    def _prompt_setup_oauth(self):
        # prompt for clientId and Client Secret
        oauthInpStr = None
        oauthinp_prompt = lambda: input(Messages.OPAAS_CLI_OAUTH_CLIID_CLISECRET_MSG)
        oauthInpStr = oauthinp_prompt()
        if not oauthInpStr:
            oauthInpStr = self.utils._response_no
        else:
            while oauthInpStr not in self.utils._response_list:
                if not oauthInpStr:
                    oauthInpStr = self.utils._response_no
                    break
                else:
                    sys.stdout.write(Messages.OPAAS_CLI_TEAR_DOWN_RESPONE_MSG.format(oauthInpStr, \
                                        self.utils.getStringFromList(self.utils._response_list)))
                    oauthInpStr = oauthinp_prompt()
                    
        if oauthInpStr.lower() == self.utils._response_yes:
            for ipKey in self.utils.setup_oauth_details:
                ip_prompt = lambda: (input(ipKey + ": "))
                ipStr = ip_prompt()
                if ipKey == self.utils._oauth_idcs_url_lbl:
                    ipStr = self.getIdentityURL(ipStr)
                else:
                    while not ipStr:
                        sys.stdout.write(ErrorMessages.OPAAS_CLI_FIELD_EMPTY_ERROR_DISPLAY % ipKey)
                        ipStr = ip_prompt()
                    self.setupTable[self.utils._oauth_details[ipKey]] = ipStr 
                self.isOauth = True        
        
    def login(self, get_identity_domain=False):
        # prompts the user to enter the credentials.
        userPrompt = lambda: (input("%s: " % self.utils.username_lbl))
        user = userPrompt()
        # username cannot be empty. 
        while not user:
            print(ErrorMessages.OPAAS_CLI_FIELD_EMPTY_ERROR_DISPLAY % self.utils.username_lbl)  # user = getpass.getuser()
            user = userPrompt()
        pprompt = lambda: (getpass.getpass('%s: ' % self.utils._pwd_lbl), getpass.getpass(Messages.OPAAS_CLI_RETYPE_PWD % self.utils._pwd_lbl))
        passwd, passwd2 = pprompt()
        # Passwords cannot be empty and passwords should match all the time.
        while passwd != passwd2 or not passwd:
            if not passwd or not passwd2:
                print(ErrorMessages.OPAAS_CLI_FIELD_EMPTY_ERROR_DISPLAY % self.utils._pwd_lbl)
            else:
                print(ErrorMessages.OPAAS_CLI_PWD_MATCH_ERROR_DISPLAY)
            passwd, passwd2 = pprompt()   
        # Get identity Domain if required.
        if get_identity_domain:
            identity_domain = self.getIdentityDomain(None) 
            return user, passwd, identity_domain
        return user, passwd 

    # Get SM URL from 'Region [us]' input value entered in psm setup.
    def getRegion(self, inpStr=None):
        # Invoke cmd prompt for Region if input is None
        if inpStr is None:
            inpStr = input(self.utils.region + ": ")
        
        if not inpStr:
            # the default will be US.
            inpStr = self.utils.get_public_domain_url('us')
        else:
            inpStr = self.utils.get_public_domain_url(inpStr)
        
        self.setupTable[self.utils.default_uri] = inpStr
        
        return inpStr   
    
    # Get Identity URL to retrieve the access token for OAuth 
    def getIdentityURL(self, inpStr=None):     
        if not inpStr: 
            # the default will be production url for US.
            inpStr = self.utils.get_public_identity_domain_url()
        
        self.setupTable[self.utils.oauth_idcs_url] = inpStr 
        
        return inpStr
        
    # Get IdentityDomain
    def getIdentityDomain(self, inpStr=None):
        input_prompt = lambda: (input(self.utils._identity_domain_lbl + ": "))
        # invoke cmd input prompt if inpStr is None.
        if inpStr is None:
            inpStr = input_prompt()
        
        # identity domain cannot be empty.
        while not inpStr:
            print(ErrorMessages.OPAAS_CLI_FIELD_EMPTY_ERROR_DISPLAY % self.utils._identity_domain_lbl)
            inpStr = input_prompt()
        
        # update the main table, that actually stores the values in the conf file.
        self.setupTable[self.utils.identity_domain] = inpStr
        
        return inpStr
    
    def checkCredentials(self, user, passwd, identityDomain, urlHostName, access_token):
        token = None
        # check if its OAUTH
        if self.isOauth and access_token is not None:
            token = access_token
        else:
            # if not, use basic auth
            if user and passwd:
                token = self.createToken(user, passwd)
            
        # return true if validation successful 
        return self._service.checkCredentials(token, identityDomain, urlHostName)  
    
    def getValidationCode(self, user, passwd, identityDomain, urlHostName, access_token, counter=0):
        # check for valid credentials at this point.
        validationCode = self.checkCredentials(user, passwd, identityDomain, urlHostName, access_token)
        if validationCode == True:
            return True, user, passwd
        else: 
            if validationCode == 400:
                # bad request error
                self._display_error(ErrorMessages.OPAAS_CLI_DEFAULT_URI_ERROR_DISPLAY)
            elif validationCode in (404, 111):
                # invalid URL
                self._display_error(ErrorMessages.OPAAS_CLI_GENERIC_SETUP_VALUES_ERR_DISPLAY)
            elif validationCode == 502:
                # invalid host or host not resolvable
                self._display_error(ErrorMessages.OPAAS_CLI_DNS_ERROR_DISPLAY % (urlHostName, self.utils.region))
            elif validationCode == 401:
                # authorization error. Quit after max retry attempts
                if counter < self.MAX_RETRIES and not self.isSetupProfileBased:
                    counter += 1
                    print(ErrorMessages.OPAAS_CLI_UNAME_PWD_ERR_DISPLAY)
                    user, passwd, identityDomain = self.login(get_identity_domain=True)
                    return self.getValidationCode(user, passwd, identityDomain, urlHostName, access_token, counter=counter)
                    #return True, user, passwd 
                else:
                    self._display_error(ErrorMessages.OPAAS_CLI_GENERIC_ERR_DISPLAY)
            elif validationCode == 403:
                # Identity domain error
                self._display_error(ErrorMessages.OPAAS_CLI_INVALID_IDENTITY_DOMAIN_ERR_DISPLAY % (identityDomain, self.utils._identity_domain_lbl))
            elif validationCode == False:
                self._display_error(ErrorMessages.OPAAS_CLI_GENERIC_ERR_DISPLAY) 
            elif validationCode >= 300:
                self._display_error(ErrorMessages.OPAAS_CLI_GENERIC_ERR_DISPLAY)
            
            # return false                
            return False, user, passwd
   
    def _display_error(self, msg):
        print('\n--------------------------------------------------------------------------------') 
        print(msg)
        logger.error(msg)
        print('--------------------------------------------------------------------------------') 


    def createToken(self, username, password):
        """
            this is used to create the http basic auth token. for the rest calls.
        """
        basicAuthToken = _basic_auth_str(username, password)
        return basicAuthToken

    def undo_configureCredentials(self, force=False):
        """
            Removes the conf and data files.
        """
        inpStr = None
        if not force:
            # if force is False, then show the interactive msg.
            while True:
                inpStr = input(Messages.OPAAS_CLI_TEAR_DOWN_PROMT_MSG)
                if inpStr.lower() in self.utils._response_list:
                    break
                else:
                    sys.stdout.write(Messages.OPAAS_CLI_TEAR_DOWN_RESPONE_MSG.format(inpStr, \
                                                                    self.utils.getStringFromList(self.utils._response_list)))
        else:
            inpStr = self.utils._response_yes
            
        if inpStr.lower() == self.utils._response_yes:
            try:
                user = self.utils.getValueFromConfigFile(self.utils.username)
                keyring.delete_password(self.utils.cli_keyring_name, user)
            except Exception as e:
                logger.error(ErrorMessages.OPAAS_CLI_TEAR_DOWN_CRED_ERROR.format(e))
            
            # remove the config directories:
            for dirname in self.subOpcDir:
                if dirname != self.utils.opc_log_dir_name:
                    self.utils.remove_config_dirs(self.opcDir + os.sep + dirname)

            sys.stdout.write(Messages.OPAAS_CLI_TEAR_DOWN_SUCCESS_DISPLAY)
            logger.info(Messages.OPAAS_CLI_TEAR_DOWN_SUCCESS_MSG)

        return 

    def execute_profile_based_setup(self, profile_file_name):
        if os.path.exists(profile_file_name):
            try:
                with open(profile_file_name) as json_file:
                    data = json.load(json_file, object_pairs_hook=OrderedDict)
                
                if not all(key in data for key in [self.utils.username, self.utils.password, self.utils.identity_domain]):
                    sys.stdout.write(ErrorMessages.OPAAS_CLI_PROFILE_BASED_MISSING_VALUES_ERR_DISPLAY % (self.utils.username, self.utils.password, self.utils.identity_domain))
                    return
                
                # read the required setup values.
                username = data[self.utils.username]
                password = data[self.utils.password]
                self.setupTable[self.utils.identity_domain] = data[self.utils.identity_domain]
                
                # get the defaultURI
                region = self.utils.get_public_domain_url('us')
                # check if the payload has the region.
                if self.utils._profile_based_region in data:
                    region = self.utils.get_public_domain_url(data[self.utils._profile_based_region])
                    # check for validity of the region
                    if region is None:
                        print(ErrorMessages.OPAAS_CLI_REGION_ERR_DISPLAY % (self.utils.get_region_values, self.utils._profile_based_region))
                        return
                # store the defaultURI into the setupTable.
                self.setupTable[self.utils.default_uri] = region
                
                # get the default outputformat.
                output_format = self.utils.default_output_value
                # check if the payload has the output format.
                if self.utils.output_format in data:
                    # check for validity of output format value.
                    if data[self.utils.output_format] not in self.utils.get_output_format_values:
                        print(ErrorMessages.OPAAS_CLI_OUTPUT_FORMAT_ERROR_MSG % (self.utils.getStringFromList(self.utils.get_output_format_values), \
                                                                                     self.utils.output_format))
                        return
                    output_format = data[self.utils.output_format] 
                self.setupTable[self.utils.output_format] = output_format 
                
                if 'oAuth' in data:
                    oauth_details = data['oAuth']
                    # check if client Id and client secret are present.
                    if not all(key in oauth_details for key in [self.utils.oauth_client_id, self.utils.oauth_client_secret]):
                        sys.stdout.write(ErrorMessages.OPAAS_CLI_PROFILE_BASED_MISSING_VALUES_OAUTH_ERR_DISPLAY % \
                                            (self.utils.oauth_client_id, self.utils.oauth_client_secret))
                        return
                    
                    # Read the clientId and Client secret into setupTable.
                    self.setupTable[self.utils.oauth_client_id] = oauth_details[self.utils.oauth_client_id]
                    self.setupTable[self.utils.oauth_client_secret] = oauth_details[self.utils.oauth_client_secret]
                    
                    # check access token server if its in the payload.
                    # get the default value.
                    access_token_server = self.utils.get_public_identity_domain_url()
                    if self.utils.oauth_idcs_url in oauth_details:
                        if self.utils.isNotBlank(oauth_details[self.utils.oauth_idcs_url]):
                            access_token_server = oauth_details[self.utils.oauth_idcs_url]
                        else:
                            sys.stdout.write(ErrorMessages.OPAAS_CLI_PROFILE_BASED_INVALID_ACCESS_TOKEN_ERR_DISPLAY)
                            return
                    self.setupTable[self.utils.oauth_idcs_url] = access_token_server
                    
                    self.isOauth = True
                    
                # execute the setup.  
                self.isSetupProfileBased = True
                return self.execute_setup(user=username, passwd=password)
            
            except ValueError as e:
                sys.stdout.write(ErrorMessages.OPAAS_CLI_PROFILE_BASED_INVALID_PAYLOAD_ERR_DISPLAY % e)
                sys.exit(1)
        else:
            sys.stdout.write(ErrorMessages.OPAAS_CLI_PROFILE_BASED_FILE_NOT_FOUND_ERR_DISPLAY.format(msg=profile_file_name))
            sys.exit(1)
                
class SetupParser(object):
    """
    The setup parser which handles the setup functions and teardown functions
    """
    def __init__(self, service_name, service_description):
        self.service_name = service_name
        self.service_description = service_description
        self._configure = Configure()
        self._utils = Utils()
    
    def __call__(self, args_extras, args_parsed):
        if Messages.OPAAS_CLI_HELP_KEY in args_extras:
            if self.service_name == Messages.OPAAS_CLI_TEAR_DOWN_KEY:
                self._display_teardown_help()
            else:
                self._display_setup_help()        
        elif args_extras:
            # additional check for teardown if they have specified force parameter.
            if len(args_extras) == 2 and args_extras[0] in self._utils.teardown_params and self.service_name == Messages.OPAAS_CLI_TEAR_DOWN_KEY:
                force_value = args_extras[1]
                if force_value.lower() not in self._utils.teardown_force_param_values:
                    sys.stdout.write(Messages.OPAAS_CLI_WARN_TEARDOWN_FORCE_MSG % self._utils.teardown_force_param_values)
                else:
                    force_value = True if force_value.lower() == 'true' else False
                    self._configure.undo_configureCredentials(force=force_value)                    
            elif len(args_extras) == 2 and args_extras[0] in self._utils.config_payload_params and self.service_name == Messages.OPAAS_CLI_SETUP_KEY:
                config_param_value = args_extras[1]
                self._configure.execute_profile_based_setup(config_param_value)
            else:
                # display the argparse error if the argument alone is specified without value.
                if len(args_extras) == 1 and (args_extras[0] in self._utils.teardown_params or args_extras[0] in self._utils.config_payload_params):
                    sys.stdout.write(ErrorMessages.OPAAS_CLI_SETUP_GENERIC_MISSING_PARAMS_ERR_DISPLAY % (self.service_name, args_extras[0]))
                    return
                raise UnknownArgumentError(arguments=' '.join(args_extras), cmd_struct=Messages.OPAAS_CLI_TOP_LEVEL_SCRIPT_NAME + self.service_name)
        else:
            if self.service_name == Messages.OPAAS_CLI_TEAR_DOWN_KEY:
                self._configure.undo_configureCredentials()    
            else:
                self._configure.configureCredentials()
    
    def _display_setup_help(self):
        script_dir = os.path.dirname(__file__)
        fileName = "setuphelp.txt"
        rel_path = os.path.join(script_dir, fileName)
        if os.path.exists(rel_path):
            with open(rel_path, "r") as f:
                print(f.read())
        else: 
            logger.error(ErrorMessages.OPAAS_CLI_SETUP_HELP_ERROR)
            print(ErrorMessages.OPAAS_CLI_SETUP_GENERIC_DISPLAY)
    
    def _display_teardown_help(self):
        script_dir = os.path.dirname(__file__)
        fileName = "teardownhelp.txt"
        rel_path = os.path.join(script_dir, fileName)
        if os.path.exists(rel_path):
            with open(rel_path, "r") as f:
                print(f.read())
        else: 
            logger.error(ErrorMessages.OPAAS_CLI_TEARDOWN_HELP_ERROR)
   
class OpaasSync(object):
    """
    This upgrades to the latest client on psm upgrade. 
    """
    def __init__(self, service_name, service_description):
        self.service_name = service_name
        self.service_description = service_description
        self._opcservice = OPCService()
        self._utils = Utils()
    
    def __call__(self, args_extras, args_parsed):
        if Messages.OPAAS_CLI_HELP_KEY in args_extras:
            self._display_help()
        elif args_extras:
            logger.error(ErrorMessages.OPAAS_CLI_UPGRADE_UNKNOWN_ARGS_ERROR, ' '.join(args_extras))
            raise UnknownArgumentError(arguments=' '.join(args_extras), cmd_struct=Messages.OPAAS_CLI_TOP_LEVEL_SCRIPT_NAME + Messages.OPAAS_CLI_UPGRADE_KEY)
        else:
            # check the version and determine whether to upgrade or not.
            self._check_version_and_upgrade()
            
    def _display_help(self):
        script_dir = os.path.dirname(__file__)
        fileName = "upgradehelp.txt"
        rel_path = os.path.join(script_dir, fileName)
        if os.path.exists(rel_path):
            with open(rel_path, "r") as f:
                print(f.read())
        else: 
            logger.error(ErrorMessages.OPAAS_CLI_UPGRADE_HELP_ERROR)
            print(ErrorMessages.OPAAS_CLI_UPGRADE_GENERIC_DISPLAY)
    
    def _install(self, package):
        # call the pip main to run the install for the upgrade command.
        return_code = pip.main(['install', '-U', package])
        
        if return_code == SUCCESS:
            logging.config.dictConfig(LOGGING_CONFIG)
            logger.info(Messages.OPAAS_CLI_UPGRADE_LOG_SUCCESS)
            return True
        elif return_code == ERROR:
            logger.error(ErrorMessages.OPAAS_CLI_UPGRADE_LOG_ERROR)
            return False
        elif return_code == UNKNOWN_ERROR:
            logger.error(ErrorMessages.OPAAS_CLI_UPGRADE_LOG_UNKOWN_ERROR)
            return False
        elif return_code == PREVIOUS_BUILD_DIR_ERROR:
            logger.error(ErrorMessages.OPAAS_CLI_UPGRADE_LOG_BUILD_ERROR)
            return False

    def _install_root(self, package):
        logger.info(Messages.OPAAS_CLI_UPGRADE_SUDO_PROMPT)
        sys.stdout.write(Messages.OPAAS_CLI_UPGRADE_SUDO_PROMPT)        
        success = True
        sudo_opts = '-HE' if self._utils.isMac() else '-H'
        p = subprocess.Popen(['sudo', sudo_opts, 'pip3', 'install', '-U', package], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        # seperate check for command not found for pip, install with pip3
        # 1 is to determine its always true.
        err_cmd_not_found_code = 1
        if err:
            err_cmd_not_found_code = self._check_err_msg(err)
        
        # check for error_code. if 2, then re-run the upgrade with pip3.
        if err_cmd_not_found_code == 2:
            # rerun the upgrade using pip3.
            p2 = subprocess.Popen(['sudo', sudo_opts, 'pip', 'install', '-U', package], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p2.communicate()            
            # check for err and success msgs. if error code is 1, then its true implicitly
            if err:
                err_code = self._check_err_msg(err, upgrade_using_pip3=False)
                if err_code == 3 or err_code == 2:
                    success = False
      
        # check for other exceptions if failed.    
        elif err_cmd_not_found_code == 3:
            success = False   
        
        # if no exception display the output for the upgrade using pip.
        if out:
            output = out.splitlines()
            for msg in output:
                sys.stdout.write('%s\n' % msg.decode('ascii'))

        if success:
            logging.config.dictConfig(LOGGING_CONFIG)
            logger.info(Messages.OPAAS_CLI_UPGRADE_LOG_SUCCESS)
        return success
    
    def _check_err_msg(self, err, upgrade_using_pip3=True):
        # success codes - 1 : success. 2 : pip command not found. 3 : Other exceptions
        success = 1;
        errMsg = err.splitlines()
        for msg in errMsg:
            decode_msg = msg.decode('ascii')
            # to figure out if there was any exception while upgrade.
            #if 'Exception:' in decode_msg or 'Exception' in decode_msg or 'Traceback' in decode_msg:
            if 'command not found' in decode_msg:
                if upgrade_using_pip3:
                    logger.error(ErrorMessages.OPAAS_CLI_UPGRADE_PIP_RETRY_ERROR % decode_msg)
                    success = 2
                    break
                else:
                    logger.error(ErrorMessages.OPAAS_CLI_UPGRADE_PIP_NOT_FOUND_ERROR)
                    sys.stderr.write(ErrorMessages.OPAAS_CLI_UPGRADE_PIP_NOT_FOUND_ERROR)
            if any(error_msg in decode_msg.lower() for error_msg in ['exception:', 'exception', 'traceback', 'command not found', \
                                                                     'invalid password', 'incorrect password']): 
                logger.error(ErrorMessages.OPAAS_CLI_UPGRADE_PIP_ERROR % decode_msg)
                success=3
            sys.stderr.write('%s\n' % decode_msg)
        return success                    
    
    def _check_version_and_upgrade(self):
        # update the cli_artifacts_version in the conf.
        defaultUri = self._utils.getValueFromConfigFile(self._utils.default_uri)
        # check if the access token is expired
        refresh_token = self._utils.isAccessTokenExpired() 
        # if token is expired, refresh the access token
        if refresh_token:
            access_token, expires_in = self._opcservice.get_oauth_access_token(refresh_token=refresh_token)
            self._utils.persistTokenAndExpiryTime(access_token, expires_in)
        
        cli_artifacts_version = self._opcservice.checkCredentials(self._utils.getAuthToken(), self._utils.getValueFromConfigFile(self._utils.identity_domain), \
                                                                  defaultUri, return_cli_artifacts_upgrade=True)
        
        if cli_artifacts_version is not None and self._utils._version_split_token in str(cli_artifacts_version):
            existing_client_version, existing_last_updated_time, existing_catalog_build_version = self._utils.get_existing_cli_artifacts_versions()
            new_client_version, new_last_updated_time, catalog_build_version = self._utils.parse_cli_artifacts_versions(cli_artifacts_version)
              
            # check if the client versions are the same, if same there is no need to upgrade.
            if (new_client_version is not None and existing_last_updated_time is not None) and \
                              (self._utils.checkVersionEquality(existing_client_version, new_client_version) or \
                              self._utils.checkVersionGreaterThan(existing_client_version, new_client_version)):
                logger.info(Messages.OPAAS_CLI_LATEST_VERSION_EXISTS)
                sys.stdout.write('%s: %s\n' % (FormatText.bold(Messages.OPAAS_CLI_INFO_MSG), Messages.OPAAS_CLI_LATEST_VERSION_EXISTS))
                return
            
            # upgrade to the latest.
            success = self._upgrade_to_latest(existing_client_version, new_client_version)
        
            # write the value to the conf
            if success:
                self._utils.writeValueToConfigFile(self._utils.build_version_key, \
                    self._utils.concat_cli_artifacts_versions(new_client_version.strip(), \
                                                               existing_last_updated_time.strip(), \
                                                               existing_catalog_build_version))
            else:
                sys.exit(1)
        else:
            if cli_artifacts_version is None:
                logger.error(ErrorMessages.OPAAS_CLI_NO_VERSION_FOUND_ERROR)
            elif cli_artifacts_version == 502:
                # invalid host or host not resolvable
                logger.error(ErrorMessages.OPAAS_CLI_UPGRADE_DNS_ERROR_DISPLAY % defaultUri)
                sys.stderr.write(ErrorMessages.OPAAS_CLI_UPGRADE_DNS_ERROR_DISPLAY % defaultUri)
            else:
                logger.error(ErrorMessages.OPAAS_CLI_UPGRADE_GENERIC_ERROR % (cli_artifacts_version))
            
            logger.info(ErrorMessages.OPAAS_CLI_UPGRADE_FAILED_ERR_DISPLAY)    
            sys.stdout.write(ErrorMessages.OPAAS_CLI_UPGRADE_FAILED_ERR_DISPLAY)    
            sys.exit(1)    
                
    
    def _upgrade_to_latest(self, existing_client_version, new_client_version):
        logger.info(Messages.OPAAS_CLI_UPGRADE_DOWNLOAD_KIT % new_client_version)
        sys.stdout.write(Messages.OPAAS_CLI_UPGRADE_DOWNLOAD_KIT % new_client_version)
        tmp_file_loc = self._opcservice.callRestApiToDownloadClient()
        if tmp_file_loc is None:
            logger.error(ErrorMessages.OPAAS_CLI_UPGRADE_DOWNLOAD_KIT_LOCATION_ERROR)
            raise OpaasDownloadFileError()
        try:
            logger.info(Messages.OPAAS_CLI_UPGRADE_DOWNLOAD_KIT_UPGRADING % (existing_client_version, new_client_version))            
            sys.stdout.write(Messages.OPAAS_CLI_UPGRADE_DOWNLOAD_KIT_UPGRADING % (existing_client_version, new_client_version))
            
            # upgrade the clientkit.    
            if self._utils.isWindows():
                return self._install(tmp_file_loc)
            else:
               return self._install_root(tmp_file_loc)  
           
            return False      
        finally:
            # remove the downloaded kit
            if os.path.exists(tmp_file_loc):
                os.remove(tmp_file_loc)
                logger.info(Messages.OPAAS_CLI_UPGRADE_CLEANING_UP)
                sys.stdout.write(Messages.OPAAS_CLI_UPGRADE_CLEANING_UP)


class OpaasLogLevel(object):
    """
    Logging level for PSM cli.
    """
    def __init__(self, service_name, service_description):
        self.service_name = service_name
        self.service_description = service_description
        self._utils = Utils()
    
    def __call__(self, args_extras, args_parsed):
        if Messages.OPAAS_CLI_HELP_KEY in args_extras:
            self._display_help()
        else:
            current_level = self._utils.getValueFromConfigFile(self._utils.log_level).lower()        
            if len(args_extras) == 0:
                sys.stdout.write(Messages.OPAAS_CLI_INFO_CURRENT_LOG_LEVEL_MSG % current_level)        
            elif len(args_extras) == 2 and args_extras[0] in self._utils.log_level_argument:
                   level = args_extras[1]
                   if level not in self._utils.get_available_log_levels:
                        sys.stdout.write(Messages.OPAAS_CLI_WARN_LOG_LEVEL_MSG % self._utils.get_available_log_levels)
                   else:
                       if  current_level != level.lower():
                           self._utils.writeValueToConfigFile(self._utils.log_level, level)
                           logger.info(Messages.OPAAS_CLI_INFO_LOG_LEVEL_UPDATE_MSG % level)
                           sys.stdout.write(Messages.OPAAS_CLI_INFO_LOG_LEVEL_UPDATE_MSG % level)
            else:
                raise UnknownArgumentError(arguments=' '.join(args_extras), cmd_struct=Messages.OPAAS_CLI_TOP_LEVEL_SCRIPT_NAME + self.service_name)
   
    def _display_help(self):
        script_dir = os.path.dirname(__file__)
        fileName = "loghelp.txt"
        rel_path = os.path.join(script_dir, fileName)
        if os.path.exists(rel_path):
            with open(rel_path, "r") as f:
                print(f.read())
        else: 
            logger.error(ErrorMessages.OPAAS_CLI_LOG_LEVEL_HELP_ERROR)
            sys.stdout.write(ErrorMessages.OPAAS_CLI_LOG_LEVEL_GENERIC_DISPLAY)     
    
