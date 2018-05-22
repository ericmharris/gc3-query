# Copyright (c) 2015 Oracle and/or its affiliates. All rights reserved.
# created by sahit.gollapudi

import argparse
import json
import logging
import collections as _collections
import copy as _copy
import os as _os
import re as _re
import sys as _sys
import textwrap as _textwrap
from collections import OrderedDict
from argparse import ArgumentError
from argparse import _UNRECOGNIZED_ARGS_ATTR, SUPPRESS
from argparse import _get_action_name
from gettext import gettext as _, ngettext
try:
    from argumenttypes import OPCArgument
    from __init__ import __version__
    from helpformatter import OPCHelpCommand, OPCCustomHelpFormatter
    from configure import SetupParser
    from handlers import RequestParamHandler,AdditionalResponseValues
    from executor import RequestExecutor
    from exceptions import UnknownArgumentError
    from utils import Utils
    from messages import Messages, ErrorMessages, LocalizationConstants
    from customexecutor import CUSTOM_IMPL_MAP
except:
    from .argumenttypes import OPCArgument
    from .__init__ import __version__
    from .helpformatter import OPCHelpCommand, OPCCustomHelpFormatter
    from .configure import SetupParser
    from .handlers import RequestParamHandler,AdditionalResponseValues
    from .executor import RequestExecutor
    from .exceptions import UnknownArgumentError
    from .utils import Utils 
    from .messages import Messages, ErrorMessages, LocalizationConstants
    from .customexecutor import CUSTOM_IMPL_MAP

# Logger
logger = logging.getLogger(__name__)

# a top level api to change the title for all the parsers
def change_title_of_arguments(parser, req_title, opt_title):
    for grp in parser._action_groups:
        if grp.title == 'positional arguments':
            grp.title = req_title
        elif grp.title == 'optional arguments':
            grp.title = opt_title

# a custom boolean type for the parser to parse the boolean values.
def custom_bool_type(v):
  # BUG FIX: 26557045: fixing the boolean parameter to accept
  # true, false. If the value is not in true or false send the 
  # value as is to the API.
  if v.lower() in ('true'):
      return True
  elif v.lower() in ('false'):
      return False
  else:
      return v

def custom_bool_with_validation_type(v):
    if v.lower() == 'true':
        return True
    elif v.lower() == 'false':
        return False
    else:
        raise argparse.ArgumentTypeError("invalid choice: '%s' (choose from 'true', 'false')" % v)
 

# a Case Insensitive list type to check for values in a case 
# sensitive format: Bug fix: 23333311
class CaseInsensitiveList(list):
    # override the __contains__ method for custom rendering.
    def __contains__(self, input):
        for item in self:
            if item.lower() == input.lower():
                return True
        return False

# A custom Action for CLI version. # Bug Fix: 23525276. 
# Honoring the -v/--version argument.
class CLIVersionAction(argparse.Action):

    def __init__(self,
                 option_strings,
                 version=None,
                 dest=argparse.SUPPRESS,
                 default=argparse.SUPPRESS,
                 help="show program's version number and exit"):
        super(CLIVersionAction, self).__init__(
            option_strings=option_strings,
            dest=dest,
            default=default,
            nargs=0,
            help=help)
        self.version = version

    def __call__(self, parser, namespace, values, option_string=None):
        if namespace.service:
            return
        version = self.version
        if version is None:
            version = parser.version
        # JIRA FIX: PSM 15705. The formatter is removing the new line character.
        # hence fixed by directly printing the version message.
        print(version)
        #formatter = parser._get_formatter()
        #formatter.add_text(version)
        #parser._print_message(formatter.format_help(), _sys.stdout)
        parser.exit()
            
# the psm parser which is the base parser for all the service, command, 
# parameter|options (argument) parsers.    
class OPCParser(argparse.ArgumentParser):
    """ PSM Client parser """
    
    Formatter = OPCHelpCommand  # argparse.RawDescriptionHelpFormatter
    Usage = Messages.OPAAS_CLI_USAGE
    helplist = ['h']
    versionList = ['-v', '--version']
    
    @property 
    def version_parser(self):
        # needs to be implemented by the sub classes. Default is False.
        # this is used to parse the special case of -v and --version handling.
        return False
    
    @property
    def command_list(self):
        # needs to be implemented by the sub classes otherwise it will return None.
        # this is returns a list of services/commands and their descriptions for help.
        return None   
    
    @property
    def parameter_dict(self):
        # ER: 23711216. to support deprecated parameter. This is used to decide 
        # if the parameter is deprecated or not. To be implemented by the sub classes
        # mainly used by OPCArgumentParser
        return None
    
    @property 
    def get_examples(self):
        # needs to be implemented by the sub classes. This returns examples associated with 
        # each command or service if there is one. If no examples, returns None.
        return None
    
    @property 
    def get_payload(self):
        # needs to be implemented by the sub classes. this will return a sample payload 
        # that will be displayed with the examples.
        return None
    
    def parse_known_args(self, args, namespace=None):
        helpvalue = list(set(self.helplist) & set(args)) 
        if helpvalue and len(helpvalue) == 1 and len(args) >= 1:
            loc = args.index(helpvalue[0])            
            args.remove(helpvalue[0])
            args.insert(loc, Messages.OPAAS_CLI_HELP_KEY)  # substituting help if entered 'h'
        
        # Bug Fix: 23525276. Honoring the -v/--version argument.
        if self.version_parser:
            versionExists = list(set(self.versionList) & set(args))
            versionValue = None
            if versionExists and len(versionExists) == 1 and len(args) >= 2:
                versionIndex = args.index(versionExists[0])
                if (versionIndex + 1) < len(args):
                    versionValue = args[versionIndex + 1]
                
        parsed, options = self.custom_parse_known_args(args, namespace)
        
        # Bug Fix: 23525276. Honoring the -v/--version argument.
        if self.version_parser and versionExists and len(versionExists) == 1:
            if versionValue is not None:
                versionValueIndex = options.index(versionValue)
                options.insert(versionValueIndex, versionExists[0])
            else:
                options.append(versionExists[0])
        # print (parsed, options)
        return parsed, options
 
    # BUG FIX: 26561690. Argparse to support deprecated param and ignore 
    # the required parameter if the deprecated param is given.
    # NOTE: Please dont manipulate these methods : 
    #     - custom_parse_known_args(self, args=None, namespace=None)
    #     - _custom_parse_known_args(self, arg_strings, namespace)
    # START : BUG FIX: 26561690
    def custom_parse_known_args(self, args=None, namespace=None):
        if args is None:
            # args default to the system args
            args = _sys.argv[1:]
        else:
            # make sure that args are mutable
            args = list(args)

        # default Namespace built from parser defaults
        if namespace is None:
            namespace = argparse.Namespace()

        # add any action defaults that aren't present
        for action in self._actions:
            if action.dest is not SUPPRESS:
                if not hasattr(namespace, action.dest):
                    if action.default is not SUPPRESS:
                        setattr(namespace, action.dest, action.default)

        # add any parser defaults that aren't present
        for dest in self._defaults:
            if not hasattr(namespace, dest):
                setattr(namespace, dest, self._defaults[dest])

        # parse the arguments and exit if there are any errors
        try:
            namespace, args = self._custom_parse_known_args(args, namespace)
            if hasattr(namespace, _UNRECOGNIZED_ARGS_ATTR):
                args.extend(getattr(namespace, _UNRECOGNIZED_ARGS_ATTR))
                delattr(namespace, _UNRECOGNIZED_ARGS_ATTR)
            return namespace, args
        except ArgumentError:
            err = _sys.exc_info()[1]
            self.error(str(err))

    def _custom_parse_known_args(self, arg_strings, namespace):
        # replace arg strings that are file references
        if self.fromfile_prefix_chars is not None:
            arg_strings = self._read_args_from_files(arg_strings)

        # map all mutually exclusive arguments to the other arguments
        # they can't occur with
        action_conflicts = {}
        for mutex_group in self._mutually_exclusive_groups:
            group_actions = mutex_group._group_actions
            for i, mutex_action in enumerate(mutex_group._group_actions):
                conflicts = action_conflicts.setdefault(mutex_action, [])
                conflicts.extend(group_actions[:i])
                conflicts.extend(group_actions[i + 1:])

        # find all option indices, and determine the arg_string_pattern
        # which has an 'O' if there is an option at an index,
        # an 'A' if there is an argument, or a '-' if there is a '--'
        option_string_indices = {}
        arg_string_pattern_parts = []
        arg_strings_iter = iter(arg_strings)
        for i, arg_string in enumerate(arg_strings_iter):

            # all args after -- are non-options
            if arg_string == '--':
                arg_string_pattern_parts.append('-')
                for arg_string in arg_strings_iter:
                    arg_string_pattern_parts.append('A')

            # otherwise, add the arg to the arg strings
            # and note the index if it was an option
            else:
                option_tuple = self._parse_optional(arg_string)
                if option_tuple is None:
                    pattern = 'A'
                else:
                    option_string_indices[i] = option_tuple
                    pattern = 'O'
                arg_string_pattern_parts.append(pattern)

        # join the pieces together to form the pattern
        arg_strings_pattern = ''.join(arg_string_pattern_parts)

        # converts arg strings to the appropriate and then takes the action
        seen_actions = set()
        seen_non_default_actions = set()

        def take_action(action, argument_strings, option_string=None):
            seen_actions.add(action)
            argument_values = self._get_values(action, argument_strings)

            # error if this argument is not allowed with other previously
            # seen arguments, assuming that actions that use the default
            # value don't really count as "present"
            if argument_values is not action.default:
                seen_non_default_actions.add(action)
                for conflict_action in action_conflicts.get(action, []):
                    if conflict_action in seen_non_default_actions:
                        msg = _('not allowed with argument %s')
                        action_name = _get_action_name(conflict_action)
                        raise ArgumentError(action, msg % action_name)

            # take the action if we didn't receive a SUPPRESS value
            # (e.g. from a default)
            if argument_values is not SUPPRESS:
                action(self, namespace, argument_values, option_string)

        # function to convert arg_strings into an optional action
        def consume_optional(start_index):

            # get the optional identified at this index
            option_tuple = option_string_indices[start_index]
            action, option_string, explicit_arg = option_tuple

            # identify additional optionals in the same arg string
            # (e.g. -xyz is the same as -x -y -z if no args are required)
            match_argument = self._match_argument
            action_tuples = []
            while True:

                # if we found no optional action, skip it
                if action is None:
                    extras.append(arg_strings[start_index])
                    return start_index + 1

                # if there is an explicit argument, try to match the
                # optional's string arguments to only this
                if explicit_arg is not None:
                    arg_count = match_argument(action, 'A')

                    # if the action is a single-dash option and takes no
                    # arguments, try to parse more single-dash options out
                    # of the tail of the option string
                    chars = self.prefix_chars
                    if arg_count == 0 and option_string[1] not in chars:
                        action_tuples.append((action, [], option_string))
                        char = option_string[0]
                        option_string = char + explicit_arg[0]
                        new_explicit_arg = explicit_arg[1:] or None
                        optionals_map = self._option_string_actions
                        if option_string in optionals_map:
                            action = optionals_map[option_string]
                            explicit_arg = new_explicit_arg
                        else:
                            msg = _('ignored explicit argument %r')
                            raise ArgumentError(action, msg % explicit_arg)

                    # if the action expect exactly one argument, we've
                    # successfully matched the option; exit the loop
                    elif arg_count == 1:
                        stop = start_index + 1
                        args = [explicit_arg]
                        action_tuples.append((action, args, option_string))
                        break

                    # error if a double-dash option did not use the
                    # explicit argument
                    else:
                        msg = _('ignored explicit argument %r')
                        raise ArgumentError(action, msg % explicit_arg)

                # if there is no explicit argument, try to match the
                # optional's string arguments with the following strings
                # if successful, exit the loop
                else:
                    start = start_index + 1
                    selected_patterns = arg_strings_pattern[start:]
                    arg_count = match_argument(action, selected_patterns)
                    stop = start + arg_count
                    args = arg_strings[start:stop]
                    action_tuples.append((action, args, option_string))
                    break

            # add the Optional to the list and return the index at which
            # the Optional's string args stopped
            assert action_tuples
            for action, args, option_string in action_tuples:
                take_action(action, args, option_string)
            return stop

        # the list of Positionals left to be parsed; this is modified
        # by consume_positionals()
        positionals = self._get_positional_actions()

        # function to convert arg_strings into positional actions
        def consume_positionals(start_index):
            # match as many Positionals as possible
            match_partial = self._match_arguments_partial
            selected_pattern = arg_strings_pattern[start_index:]
            arg_counts = match_partial(positionals, selected_pattern)

            # slice off the appropriate arg strings for each Positional
            # and add the Positional and its args to the list
            for action, arg_count in zip(positionals, arg_counts):
                args = arg_strings[start_index: start_index + arg_count]
                start_index += arg_count
                take_action(action, args)

            # slice off the Positionals that we just parsed and return the
            # index at which the Positionals' string args stopped
            positionals[:] = positionals[len(arg_counts):]
            return start_index

        # consume Positionals and Optionals alternately, until we have
        # passed the last option string
        extras = []
        start_index = 0
        if option_string_indices:
            max_option_string_index = max(option_string_indices)
        else:
            max_option_string_index = -1
        while start_index <= max_option_string_index:

            # consume any Positionals preceding the next option
            next_option_string_index = min([
                index
                for index in option_string_indices
                if index >= start_index])
            if start_index != next_option_string_index:
                positionals_end_index = consume_positionals(start_index)

                # only try to parse the next optional if we didn't consume
                # the option string during the positionals parsing
                if positionals_end_index > start_index:
                    start_index = positionals_end_index
                    continue
                else:
                    start_index = positionals_end_index

            # if we consumed all the positionals we could and we're not
            # at the index of an option string, there were extra arguments
            if start_index not in option_string_indices:
                strings = arg_strings[start_index:next_option_string_index]
                extras.extend(strings)
                start_index = next_option_string_index

            # consume the next optional and any arguments for it
            start_index = consume_optional(start_index)

        # consume any positionals following the last Optional
        stop_index = consume_positionals(start_index)

        # if we didn't consume all the argument strings, there were extras
        extras.extend(arg_strings[stop_index:])

        # make sure all required actions were present and also convert
        # action defaults which were not given as arguments
        required_actions = []
        for action in self._actions:
            if action not in seen_actions:
                # BUG FIX: 26561690
                # NOTE: action is an object which will contain the details of the parameter
                # check if the seen action is present in the parameter dict 
                # if present check if the superseded by value is the same as 
                # action.dest in the set of listed actions. If its same then bypass
                # adding that action into the required_actions if the action was required.
                deprecatedParam = False
                if self.parameter_dict is not None:
                    for seen_action in seen_actions:
                        if seen_action.dest in self.parameter_dict and "deprecated" in self.parameter_dict[seen_action.dest] \
                                and "supersededBy" in self.parameter_dict[seen_action.dest]:
                            superseded_by_param = self.parameter_dict[seen_action.dest]["supersededBy"]
                            if action.dest == superseded_by_param:
                                deprecatedParam = True
                                break
                            
                if action.required and not deprecatedParam:
                    required_actions.append(_get_action_name(action))
                else:
                    # Convert action default now instead of doing it before
                    # parsing arguments to avoid calling convert functions
                    # twice (which may fail) if the argument was given, but
                    # only if it was defined already in the namespace
                    if (action.default is not None and
                        isinstance(action.default, str) and
                        hasattr(namespace, action.dest) and
                        action.default is getattr(namespace, action.dest)):
                        setattr(namespace, action.dest,
                                self._get_value(action, action.default))

        if required_actions:
            self.error(_('the following arguments are required: %s') %
                       ', '.join(required_actions))

        # make sure all required groups had one option present
        for group in self._mutually_exclusive_groups:
            if group.required:
                for action in group._group_actions:
                    if action in seen_non_default_actions:
                        break

                # if no actions were used, report the error
                else:
                    names = [_get_action_name(action)
                             for action in group._group_actions
                             if action.help is not SUPPRESS]
                    msg = _('one of the arguments %s is required')
                    self.error(msg % ' '.join(names))

        # return the updated namespace and the extra arguments
        return namespace, extras
 
    # END. BUG FIX: 26561690 
 
        
    def format_help(self):
        formatter = self._get_formatter()        
        # the list of descriptions for the commands are passed to the formatter
        formatter.command_list_description = self.command_list           
        # usage
        formatter.add_usage(self.usage, self._actions,
                            self._mutually_exclusive_groups)
        # description
        formatter.add_text(self.description)
        # positionals, optionals and user-defined groups
        for action_group in self._action_groups:
            formatter.start_section(action_group.title)
            formatter.add_text(action_group.description)            
            formatter.add_arguments(action_group._group_actions)
            formatter.end_section()
        # epilog
        formatter.add_text(self.epilog)
        # determine help from format above
        return formatter.format_help()      
    
# the below three sub classes of the main opcparser that will 
# be used for services, commands and parameters    
class OPCServiceParser(OPCParser):
    # the parser which builds the initial <service> command list
    Formatter = OPCHelpCommand  # argparse.RawTextHelpFormatter    
    def __init__ (self, description, service_commands, service_list_descriptions):
        super().__init__(formatter_class=self.Formatter,
            conflict_handler='resolve',
            description=description,
            usage=self.Usage,
            add_help=False)  # add_help=False
        # _command_list will be used by the help formatter to display the description
        # for the available services.
        self._command_list = service_list_descriptions
        self._version_parser = True  
        self._build_arguments(service_commands)
    
    @property
    def version_parser(self):
        return self._version_parser
        
    @property
    def command_list(self):
        return self._command_list
    
    @command_list.setter
    def command_list(self, value):
        self._command_list = value
        
    def _build_arguments(self, service_commands):        
        # Place to add any other commands
        self.add_argument("service", choices=CaseInsensitiveList(list(service_commands.keys())))


class OPCCommandParser(OPCParser):
    Formatter = OPCHelpCommand  # argparse.RawTextHelpFormatter    
    
    def __init__(self, command_list, service_desc, service_name):
        """
            :type command_list: dict
            :param command_list: holds the list of commands and  commandexecutor for a particular service
            
            :type service_desc: str
            :param servcie_desc: the description of the service
            
            :type servcie_name: str
            :param servcie_name: the name of the service for which the command parser is built.
        """
        Usage = Messages.OPAAS_CLI_TOP_LEVEL_SCRIPT_NAME + service_name + " <command> [parameters]"
        super().__init__(
            formatter_class=self.Formatter,
            conflict_handler='resolve',
            usage=Usage,
            description=service_desc,
            add_help=False)
        self._build(command_list)
        self._service_name = service_name
        # use this to pass the description list to the help formatter.
        self._service_commands_description = None
        # use this to pass the example if exist to the help formatter.
        self._example_for_service = None

    @property
    def command_list(self):
        return self._service_commands_description
    
    @command_list.setter 
    def command_list(self, value):
        self._service_commands_description = value 
    
    @property
    def get_examples(self):
        return self._example_for_service
    
    @get_examples.setter
    def get_examples(self, value):
        self._example_for_service = value
        
    def _build(self, command_list):
        self.add_argument('command', choices=list(command_list.keys()))
    

class OPCArgumentParser(OPCParser):       
    def __init__(self, argument_list, cmd_dict, service_name, cmd_name, cmd_list=None, additional_response_values=None):
        """
           :type argument_list: dict
           :param argument_list: the argumenttypes to be added to the argument parser.
           
           :type cmd_dict: dict
           :param cmd_dict: holds the description for the specified command
           
           :type service_name: str
           :param service_name: the service name that is in scope.  
           
           :type cmd_name: str
           :param cmd_name: the cmd name that is in scope         
        """
        self.utils = Utils()
        # command_list is an optional subcommand_list.  If it's passed
        # in, then we'll update the argparse to parse a 'subcommand' argument
        # and populate the choices field with the command list keys.
        command_structure = Messages.OPAAS_CLI_TOP_LEVEL_SCRIPT_NAME + service_name + " " + cmd_name 
        # the if, is to add the parameters in the usage if it exsits in the catalog dict.
        usage = command_structure + (" [parameters]" if 'parameters' in cmd_dict else '')
        super().__init__(
            formatter_class=self.Formatter,
            usage=usage,
            description=cmd_dict['description'],
            conflict_handler='resolve',
            add_help=False)
        # register the custom type for parsing the boolean values.
        self.register('type','bool', custom_bool_type)
        self.register('type', 'custom_bool', custom_bool_with_validation_type)
        # add the example and payload if present for a particular command.
        self._example_for_command = cmd_dict['example'] if 'example' in cmd_dict else None
        self._payload_for_example = cmd_dict['samplePayload'] if 'samplePayload' in cmd_dict else None        
        # TBD: if this cmd_list is needed.
        if cmd_list is None:
            cmd_list = {}
        self._command_structure = command_structure
        self._param_dict = cmd_dict['parameters'] if 'parameters' in cmd_dict else None
        self._command_dict = cmd_dict
        self._additional_response_values = additional_response_values
        self._build(argument_list, cmd_list)

    @property
    def parameter_dict(self):
        return self._param_dict
    
    @property
    def get_examples(self):
        return self._example_for_command
    
    @get_examples.setter
    def get_examples(self, value):
        self._example_for_command = value
    
    @property 
    def get_payload(self):
        return self._payload_for_example
    
    @get_payload.setter 
    def get_payload(self, value):
        self._payload_for_example = value 
    
    def _build(self, argument_list, cmd_list=None):
        for parameter_name in argument_list:
            optionArgument = argument_list[parameter_name]
            # self will this class parser
            optionArgument.add_arg_to_parser(self)
        
        # add default output format overriding at cmd level for every command:
        self.add_argument('-of','--output-format', type=str, dest=self.utils.output_format_override, metavar='',\
                           action='store', \
                           help=Messages.OPAAS_CLI_OUTPUT_FORMAT_HELP_DESC % self.utils.getStringFromList(self.utils.get_output_format_values) , \
                           choices = self.utils.get_output_format_values )
        
        # check if it's a NON-GET command, if yes then add "wait-until-complete" argument 
        if self._command_dict["method"] != "GET" and self._additional_response_values.operation_status_uri is not None \
                            and self._additional_response_values.operation_status_uri:
            # add default 'wait-until-complete' for every command:
            self.add_argument('-wc','--wait-until-complete', type='custom_bool', dest=self.utils.wait_until_complete, metavar='',\
                           action='store', \
                           help=Messages.OPAAS_CLI_WAIT_UNTIL_COMPLETE_DESC % self.utils.getStringFromList(self.utils.get_wait_until_complete_values) ) 

    def parse_known_args(self, args, namespace=None):
        if len(args) == 1 and args[0] == Messages.OPAAS_CLI_HELP_KEY:
            parsed_args = argparse.Namespace()
            parsed_args.help = Messages.OPAAS_CLI_HELP_KEY
            return parsed_args, []
        else:
            return super().parse_known_args(
                    args, namespace)
    

class OPCServiceCmdExecutor (object):
    """ the class to hold the <service> commands """
    
    def __init__ (self, service_cmd_name, opcdir, service_description, original_service_file_name=None):
        """
           :type service_cmd_name: str
           :param service_cmd_name: the name of the service that is keyed in.
           
           :type opcdir: str
           :param opcdir: this is the base directory from where the service json resides
           
           :type service_description: str
           :param service_description: the description that goes for each command parser.
        """
        # the service_cmd_name is the name that the CLI user types 
        # after the base psm command. for eg: psm jcs / psm setup
        self._name = service_cmd_name
        self._original_service_file_name = original_service_file_name
        self._servicepath = opcdir 
        self._service_commands = None
        # to be passed to the OPCCommandparser for parser description
        self._service_description = service_description
        # this is used to display the description for each command 
        self._service_commands_description = OrderedDict()
        # this is to store the example for the service leve help.
        self._service_example = None
        # ths is to store the payload for the example if exists for help.
        self._service_example_payload = None
        self._additional_response_values = AdditionalResponseValues()
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
    
    @property     
    def service_commands_description(self):
        return self._service_commands_description
    
    @service_commands_description.setter 
    def service_commands_description(self, value):
        self._service_commands_description = value 
    
    @property
    def service_example(self):
        return self._service_example
    
    @service_example.setter
    def service_example(self, value):
        self._service_example = value
    
    @property 
    def get_service_description(self):
        return self._service_description
    
    @property
    def service_commands(self):
        # build the service commands from <service>.json
        if self._service_commands is None:
            self._service_commands = self._build_service_cmd_list()            
        return self._service_commands
    
    def _build_service_cmd_list(self):
        # builds the list of commands associated with a particular
        # service. for eg: if the service is 'jcs', it builds all the
        # commands for jcs.
        service_commands = OrderedDict()        
        with open(self._servicepath + "/" + self._original_service_file_name + ".json") as jf:
            data = json.load(jf, object_pairs_hook=OrderedDict)        
        commands = data[self._original_service_file_name]['commands']   
        self.service_example = data[self._original_service_file_name]['example'] if 'example' in data[self._original_service_file_name] else None
        
        # Add Custom Command to the service catalog. From ER:27411048
        if self._original_service_file_name in LocalizationConstants.AddCustomCommandToCatalog:
            for command_name, service_command_help_file_name in LocalizationConstants.AddCustomCommandToCatalog[self._original_service_file_name].items():
                path_service_command_help_file_name = _os.path.join(_os.path.dirname(__file__), service_command_help_file_name)
                with open(path_service_command_help_file_name) as af:
                    command_help_data = json.load(af, object_pairs_hook=OrderedDict)
                commands[command_name] = command_help_data[command_name]
                 
        # check if 'operation-status' is present in the commands
        # if yes, then populate the operation_status_uri
        if 'operation-status' in commands:
            self._additional_response_values.operation_status_uri = commands['operation-status'].get('uri',{})    
       
        # for each command in the specified service build the command executor 
        # which builds the parser for the parameters (options) associated with
        # that command. Passing the value, the rest of the dict for reference to 
        # opccommandexecutor.
        for command, value in commands.items():
            # check our any service with custom command implementation
            if self._original_service_file_name in LocalizationConstants.CustomCommandForService and \
                            command in LocalizationConstants.CustomCommandForService[self._original_service_file_name]:
                command_help_file_name = LocalizationConstants.CustomCommandForService[self._original_service_file_name][command]
                help_dir = _os.path.dirname(__file__)
                path_to_command_help_file = _os.path.join(help_dir, command_help_file_name)
                with open(path_to_command_help_file) as f:
                    help_data = json.load(f, object_pairs_hook=OrderedDict)
                for k,v in help_data.items():
                    value['parameters'][k] = v 
                    
            service_commands[command] = OPCCommandExecutor(self.name, command, value,self._additional_response_values, original_service_type_name=self._original_service_file_name)         
            # build the description for each command to be displayed on help
            self.service_commands_description[command] = value['description']
        # add help
        service_commands[Messages.OPAAS_CLI_HELP_KEY] = OPCCustomHelpFormatter(isServiceOrCommand=False, argumentParserParameter=False, service_type_name=self._original_service_file_name )  # HELPTAG
        self.service_commands_description[Messages.OPAAS_CLI_HELP_KEY] = Messages.OPAAS_CLI_HELP_DESC  # HELPTAG
        return service_commands
    
    def __call__(self, args_extras, args_parsed):
        # to create the OPCCommand Parser by calling the create command
        # parser which is used to check the arguments for the service 
        # and then invoke the OPC Command Executor which builds the 
        # OPCArgumentParser.
        # print ("OPCServiceCommandExecutor call function")
        parser = self._create_command_parser()
        service_commands = self.service_commands 
        try:
            cmd_args_parsed, command_args_extras = parser.parse_known_args(args_extras)
            return service_commands[cmd_args_parsed.command](command_args_extras, cmd_args_parsed, service_commands)
        except argparse.ArgumentError:
            parser.print_help()                
    
    def _create_command_parser(self):
        # creates the OPCCommandParser for the list of services
        service_commands = self.service_commands  
        parser = OPCCommandParser(service_commands, self.get_service_description, self.name)
        # pass the service_command description to the parser for help formatter to use.
        parser.command_list = self.service_commands_description
        # pass the service level example to the parser for help formatter to use.
        parser.get_examples = self.service_example
        service_commands[Messages.OPAAS_CLI_HELP_KEY].parser = parser  # HELPTAG
        change_title_of_arguments(parser, 'Available commands', 'Optional arguments') 
        return parser

class OPCCommandExecutor(object):
    """ this is to call and build the options for the commands if any
        Build the ArgParser and invokes the Request builder to call
        Rest End points.
    """
    def __init__(self, service_name, cmd_name, cmd_dict, additional_response_values=None, original_service_type_name=None):
        """
            :type service_name: str
            :param service_name: the name of the <service>
 
            :type cmd_name: str
            :param cmd_name: the name of the <command>
            
            :type cmd_dict: dict
            :param cmd_dict: holds the dict values for a given command
            
            :type additional_response_values: object
            :param additional_response_values: object containing additional response values
        """
        self._cmd_name = cmd_name
        self._service_name = service_name
        # TODO: TBD if this command_list will be used later or not
        self._command_list = None
        self._argument_list = None 
        self._arg_parameter_list = None
        # the dict for command from the json 
        self._cmd_dict = cmd_dict
        self._additional_response_values = additional_response_values
        self._original_service_type_name = original_service_type_name

        
    @property
    def cmd_name(self):
        return self._cmd_name
    
    @cmd_name.setter
    def cmd_name(self, value):
        self._cmd_name = value 
        
    @property
    def service_name(self):
        return self._service_name
    
    @service_name.setter
    def service_name(self, value):
        self._service_name = value
    
    @property 
    def command_list(self):
        return self._command_list
    
    @command_list.setter
    def command_list(self, value):
        self._command_list = value
        
    @property 
    def cmd_list_dict(self):
        return self._cmd_dict
    
    @cmd_list_dict.setter
    def cmd_list_dict(self, value):
        self._cmd_dict = value 
    
    @property 
    def arg_parameter_list(self):
        return self.arg_parameter_list
    
    @arg_parameter_list.setter 
    def arg_parameter_list(self, value):
        self._arg_parameter_list = value 
        
    @property 
    def original_service_type(self):
        return self._original_service_type_name

    @property
    def argument_list(self):
        if self._argument_list is None:
            self._argument_list = self._build_argument_list()
        return self._argument_list
    
    def _build_argument_list(self): 
        # build the list of arguments based on the command name
        # cmd_list = self._command_list[self.cmd_name]
        cmd_list_dict = self.cmd_list_dict
        argument_list = cmd_list_dict['parameters'] if 'parameters' in cmd_list_dict else None
        return argument_list
    
    def __call__(self, args_extras, args_parsed, command_list):
        # TODO: TBD if this command_list will be used later or not.
        self.command_list = command_list
        parser = self._create_argument_parser()   
        options_args_parsed, options_args_extras = parser.parse_known_args(args_extras) 
        
        # the parameter ArgParser is processed differently for Help:
        if Messages.OPAAS_CLI_HELP_KEY in options_args_parsed:
            if options_args_parsed.help == Messages.OPAAS_CLI_HELP_KEY:
                parameter_help = self._create_help(parser)
                return parameter_help(options_args_extras, options_args_parsed)
        
        if options_args_extras:
            logger.error("Unknown Argument: %s"% ' '.join(options_args_extras)) 
            raise UnknownArgumentError(arguments = ' '.join(options_args_extras), cmd_struct=parser._command_structure)
        else:
            # parse the values entered in the cmd line and build the requests
            # and format the response that gets displayed to the user.
            options_for_request_builder = RequestParamHandler(self.service_name,
                                                self.cmd_name,
                                                options_args_parsed,
                                                self._arg_parameter_list,
                                                self._cmd_dict,
                                                self.argument_list,
                                                self._additional_response_values)
            
            # Build HTTP request --> Call REST endpoint --> Process response --> Display output
            if (self.service_name in LocalizationConstants.CustomCommandForService and \
                            self.cmd_name in LocalizationConstants.CustomCommandForService[self.service_name]) or \
                (self.service_name in LocalizationConstants.AddCustomCommandToCatalog and \
                            self.cmd_name in LocalizationConstants.AddCustomCommandToCatalog[self.service_name]):
                CUSTOM_IMPL_MAP[self.service_name][self.cmd_name](options_for_request_builder, parser.usage, parser.prog).pre_execute_request()
            else:
                RequestExecutor(options_for_request_builder).execute_request() 
    
    def _create_help(self, parser):
        # the custom help formatter is created with a flag to indicate that 
        # it is for parameter to display the help for parameters.
        parameter_help = OPCCustomHelpFormatter(isServiceOrCommand=False, argumentParserParameter=True, service_type_name=self.original_service_type)
        # add the parser for formatting the help
        parameter_help.parser = parser
        return parameter_help
    
    def _create_argument_parser(self):
        # creates the parser for the optional arguments associated with
        # the specified <command>
        # the command_list: TBD if needed.
        command_list = self.command_list
        self._arg_parameter_list = self._build_parameter_list()
        parser = OPCArgumentParser(self._arg_parameter_list, self.cmd_list_dict, self.service_name, self.cmd_name, None, self._additional_response_values) 
        change_title_of_arguments(parser, 'Required parameters', 'Optional parameters') 
        return parser
        
    def _build_parameter_list(self):
        # this is the create a list of OPCArgument object from the argument_list
        arg_parameter_list = OrderedDict()
        argument_list = self.argument_list
        if argument_list is not None:
            for parameter, value in argument_list.items():
                # Dont add the hiddenconstant parameter to the argparse. 
                # this is processed internally in handlers.
                if 'hiddenConstant' not in value:
                    # keep the arg_name and dest name the same. Look __init__ in OPCArgument for details
                    alias_name = value['alias'] if 'alias' in value else None
                    choices_list = value['choices'] if 'choices' in value else None
                    arg_parameter_list[parameter] = OPCArgument(parameter, value['type'], value['description'],
                         parameter, value['required'], 'store', alias_name, choices_list) 
        return arg_parameter_list    
