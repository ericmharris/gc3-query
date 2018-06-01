# Copyright (c) 2015 Oracle and/or its affiliates. All rights reserved.
# created by sahit.gollapudi


"""scripts.opccli: provides entry point main()."""

import sys
import os
import json
import logging.config
from collections import OrderedDict
from argparse import ArgumentParser
try:
    from .cliparser import OPCServiceCmdExecutor, OPCServiceParser, change_title_of_arguments, CLIVersionAction
    from .configure import SetupParser, OpaasSync, OpaasLogLevel
    from .__init__ import __version__
    from .helpformatter import OPCHelpCommand, OPCCustomHelpFormatter
    from .utils import Utils, LOGGING_CONFIG
    from .messages import Messages, ErrorMessages, LocalizationConstants
except:
    from cliparser import OPCServiceCmdExecutor, OPCServiceParser, change_title_of_arguments, CLIVersionAction
    from configure import SetupParser, OpaasSync, OpaasLogLevel
    from __init__ import __version__
    from helpformatter import OPCHelpCommand, OPCCustomHelpFormatter
    from utils import Utils, LOGGING_CONFIG
    from messages import Messages, ErrorMessages, LocalizationConstants


logger = logging.getLogger(__name__)

def main():
    cli = OPCCreateCLI()
    try:
        cli.main()
    except KeyboardInterrupt:
        logger.error(ErrorMessages.OPAAS_CLI_KEYBOARD_INTERRUPT)
        try:
            sys.exit(1)
        except SystemExit:
            os._exit(1)

class OPCCreateCLI(object):
    """
       The main driver of the psm client. Which builds the parser arguments
       to execute the commands in a systematic way.
    """
    utils = Utils()
    service_list = None
    opcDir =  utils.opc_data_dir
    serviceIndexFile = opcDir + utils.service_index_filename
    service_list_descriptions = OrderedDict()
    setup_description = Messages.OPAAS_CLI_SETUP_DESC
    upgrade_description = Messages.OPAAS_CLI_UPGRADE_DESC
    log_level_description = Messages.OPAAS_CLI_LOG_LEVEL_DESC
    teardown_description = Messages.OPAAS_CLI_TEAR_DOWN_DESC
    #logging.basicConfig(filename=utils.log_file_name, level=logging.INFO)
    logging.config.dictConfig(LOGGING_CONFIG)

    def _create_service_commands(self):
        #TODO: check corner case for the file.
        # create the service list from the service catalog.
        service_list = OrderedDict()
        #check if the catalog exists. other wise only setup will be shown.
        if os.path.exists(self.serviceIndexFile):
            with open(self.serviceIndexFile) as json_file:
                data = json.load(json_file, object_pairs_hook=OrderedDict)
            services = data['services']
            service_list_desc_for_help = services
            # adding the service as the index in lower case. Bug fix: 23333311
            for service, value in services.items():
                # BUG FIX: 27112221. check if the serviceType exists in the ServiceMapping for backward compatibility
                original_service_file_name = service
                if service.lower() in LocalizationConstants.ServiceMapping:
                    service = LocalizationConstants.ServiceMapping[service.lower()]
                    # change the input service type to display service type from service mapping.
                    service_list_desc_for_help = OrderedDict([(service, v) if k == original_service_file_name else (k, v) for k, v in service_list_desc_for_help.items()])
                service_list[service.lower()] = OPCServiceCmdExecutor(service, self.opcDir, value, original_service_file_name=original_service_file_name)
            # add descriptions for help
            self.service_list_descriptions = service_list_desc_for_help

        # add setup command to configure the psm
        service_list[Messages.OPAAS_CLI_SETUP_KEY] = SetupParser(Messages.OPAAS_CLI_SETUP_KEY, self.setup_description)
        # add psm teardown to remove configured psm setup options
        service_list[Messages.OPAAS_CLI_TEAR_DOWN_KEY] = SetupParser(Messages.OPAAS_CLI_TEAR_DOWN_KEY, self.teardown_description)
        # add help command to display the psm help
        service_list[Messages.OPAAS_CLI_HELP_KEY] = OPCCustomHelpFormatter(isServiceOrCommand=True, argumentParserParameter=False)  #HELPTAG
        # add psm upgrade command to upgrade the catalog.
        service_list[Messages.OPAAS_CLI_UPGRADE_KEY] = OpaasSync(Messages.OPAAS_CLI_UPGRADE_KEY, self.upgrade_description)
        # add psm log to change log values.
        service_list[Messages.OPAAS_CLI_LOG_LEVEL] = OpaasLogLevel(Messages.OPAAS_CLI_LOG_LEVEL, self.log_level_description)
        #for help display add setup, help, log level and upgrade.
        self.service_list_descriptions[Messages.OPAAS_CLI_SETUP_KEY] = self.setup_description
        self.service_list_descriptions[Messages.OPAAS_CLI_TEAR_DOWN_KEY] = self.teardown_description
        self.service_list_descriptions[Messages.OPAAS_CLI_UPGRADE_KEY] = self.upgrade_description
        self.service_list_descriptions[Messages.OPAAS_CLI_LOG_LEVEL] = self.log_level_description
        self.service_list_descriptions[Messages.OPAAS_CLI_HELP_KEY] = Messages.OPAAS_CLI_HELP_DESC    #HELPTAG

        return service_list

    def _get_service_list(self):
        if self.service_list is None:
            self.service_list = self._create_service_commands()
        return self.service_list


    def _create_parser(self):
        service_list = self._get_service_list()
        parser = OPCServiceParser(Messages.OPAAS_CLI_DESCRIPTION, service_list, self.service_list_descriptions)
        parser.add_argument('-v', '--version', action = CLIVersionAction, help=Messages.OPAAS_CLI_VERSION_HELP_DESC, version=Messages.OPAAS_CLI_VERISON_DISPLAY_MSG % __version__)
        service_list[Messages.OPAAS_CLI_HELP_KEY].parser = parser #HELPTAG
        change_title_of_arguments(parser, Messages.OPAAS_CLI_RENAME_POSITIONAL_ARG, Messages.OPAAS_CLI_RENAME_OPTIONAL_ARG)
        return parser

    def main(self, args=None):

        if args is None:
            args = sys.argv[1:]

        parser = self._create_parser()
        args_parsed, args_extras = parser.parse_known_args(args)
        service_list = self._get_service_list()

        try:
            # the service is rendered in lower case. For bug fix: 23333311
            return service_list[args_parsed.service.lower()](args_extras, args_parsed)
        except FileNotFoundError as e:
            logger.error(ErrorMessages.OPAAS_CLI_FILE_NOT_FOUND % e)
            sys.stderr.write(ErrorMessages.OPAAS_CLI_CONFIG_CORRUPTED)
            sys.exit(1)
        except Exception as ex:
            logger.error("Exception: %s" % ex)
            sys.stderr.write("%s\n"%ex)
            sys.exit(1)

if __name__ == "__main__":
    main()
