# Copyright (c) 2015 Oracle and/or its affiliates. All rights reserved.
# created by sahit.gollapudi

import argparse
import sys
import os
import re as _re
import json
import textwrap
from collections import OrderedDict

import datetime
from distutils.core import Command
from distutils.errors import DistutilsOptionError

try:
    from utils import Utils, FormatText
    from messages import Messages, LocalizationConstants
except:
    from .utils import Utils, FormatText
    from .messages import Messages, LocalizationConstants

#=== CLASSES ==================================================================

class OPCHelpCommand(argparse.HelpFormatter):
    # Overriding the HelpFormatter to customize the help choices that get displayed.
    # The inner class Section Formatter is also overridden inorder to display the 
    # action choices (list of commands, services) in a sorted order. 
    # Not a good practice to do this. But will be in place until the implementation 
    # of the Linux man page for help is completed.
    
    def __init__(self,
                 prog,
                 indent_increment=2,
                 max_help_position=24,
                 width=None):
        
        super().__init__(prog, indent_increment=2, max_help_position=24,
                         width=None)

        self._root_section = self._SectionFormatter(self, None)
        self._current_section = self._root_section
        
        self._command_list_description = None
        # ER: 23711216
        self._parameter_dict = None   
        self._utils = Utils() 
        # custom help indent for options description
        self._help_indent_option = 7
        self._help_overrided_width_text_length = 78
          
    class _SectionFormatter(argparse.HelpFormatter._Section):
        # overriding the default _Section class of the HelpFormatter
        
        def __init__(self, formatter, parent, heading=None):
            self.formatter = formatter
            self.parent = parent
            self.heading = heading
            self.items = []

        def format_help(self):
            # format the indented section
            if self.parent is not None:
                self.formatter._indent()
            join = self.formatter._join_parts
            for func, args in self.items:
                func(*args)
            item_help = join([func(*args) for func, args in self.items])
            if self.parent is not None:
                self.formatter._dedent()

            # return nothing if the section was empty
            if not item_help:
                return ''

            # add the heading if the section was non-empty
            if self.heading is not argparse.SUPPRESS and self.heading is not None:
                current_indent = self.formatter._current_indent
                heading = '%*s%s:\n' % (current_indent, '', self.heading)
            else:
                heading = ''
            
            if heading.strip() == 'Available commands:' or heading.strip() == 'Available services:':
                command_list = self.formatter.command_list_description if self.formatter.command_list_description is not None else None
                sortedlist = item_help if command_list is None else self.format_dict_description(command_list)               
                return join(['\n', heading, sortedlist, '\n']) 
              
            # join the section-initial newline, the heading and the help
            return join(['\n', heading, item_help, '\n'])
        
        def format_dict_description(self, command_list_description):
            # this is to format the command list with description that 
            # gets displayed on print_help of the parser.
            result = []
            if command_list_description and len(command_list_description) >= 1 :
                result = []
                maxlen = len(max(command_list_description, key=len))
                max_linux_description = 78
                for name, description in command_list_description.items():
                    format_name = self.format_cmd_name_help(name, maxlen)
                    if len(description) > max_linux_description:
                        format_description = textwrap.shorten(description, max_linux_description, placeholder='...')
                    else: 
                        format_description = description 
                    # append the name and the description to the result.
                    result.append("%s%s" % (format_name, format_description))
                # return the result with the adding the new line character.
                return '\n'.join(result) 
            # returns an empty list.
            return result 
        
        def format_cmd_name_help(self, name, maxlen):
            max_space_len_cmd_name_leading = 2
            max_space_len_cmd_name_trailing = 5
            # adds indent with space in the begining of the name.'>' means adds the spaces at the beginning 
            fill_value_name_leading = max_space_len_cmd_name_leading + len(name)   
            format_name = '{message: >{fill}}'.format(message=name, fill=fill_value_name_leading)
            # add trailing spaces for the command name.'<' means adds spaces at the end.
            fill_value_name_trailing = max_space_len_cmd_name_leading + maxlen + max_space_len_cmd_name_trailing
            format_name = '{message: <{fill}}'.format(message=format_name, fill=fill_value_name_trailing)      
            return format_name      
            
    def start_section(self, heading):
        self._indent()
        section = self._SectionFormatter(self, self._current_section, heading)
        self._add_item(section.format_help, [])
        self._current_section = section
     
    @property 
    def command_list_description(self):
        return self._command_list_description
        
    @command_list_description.setter
    def command_list_description(self, value):
        self._command_list_description = value  
     
    # overriding this method to parse newline with 'no fill'    
    def _split_lines(self, text, width):
        return text.splitlines()
      
    @property
    def param_dict(self):
        return self._parameter_dict
    
    @param_dict.setter 
    def param_dict(self, value):
        self._parameter_dict = value
    
    @staticmethod
    def format_options(parser):
        formatter = parser._get_formatter()
        # ER: 23711216. added this param_dict to show the deprecated values in help
        formatter.param_dict = parser.parameter_dict 

        # positionals, optionals and user-defined groups
        for action_group in parser._action_groups:
            if action_group.title != 'Available commands' and action_group.title != 'Available services':
                formatter.start_section(None)
                formatter.add_text(None)
                formatter.add_arguments(action_group._group_actions)
                formatter.end_section()

        # epilog
        formatter.add_text(parser.epilog)

        # determine help from format above
        return formatter.format_help()
    
    @staticmethod
    def get_format_actions(parser, action):
        # this is explicitly to get the list of actions (optional arguments)
        formatter = parser._get_formatter()
        return formatter._format_action_invocation(action)
    
    # overriding this method.
    def _format_action_invocation(self, action):
        if not action.option_strings:
            metavar, = self._metavar_formatter(action, action.dest)(1)
            return metavar
        else:
            parts = []
            # if the Optional doesn't take a value, format is:
            #    -s, --long
            if action.nargs == 0:
                parts.extend([action_str for action_str in action.option_strings])

            # if the Optional takes a value, format is:
            #    -s ARGS, --long ARGS
            else:
                default = action.dest.upper()
                args_string = self._format_args(action, default)
                for option_string in action.option_strings:
                    parts.append('%s%s' % (option_string, args_string))
       
            return ', '.join(parts)    
    
    def _format_paramater_help_display_list(self, action_header, deprecated='', indent_spacing=2):
        # changing the action header display.
        result = ''
        if ',' in action_header:
            values = action_header.split(',')
            action_display_header = []
            for header in values:
                split_list = header.replace(' [ ...]', '')
                action_display_header.append(split_list)
            result = ','.join(action_display_header)
        else:
            action_header_display = action_header.replace(' [ ...]', '')
            # new action_header with the option name.
            result = action_header_display
        
        return self._format_parameter(deprecated, indent_spacing, result)
    
    # overriding this method for custom help formatting
    def _format_action(self, action):
        # determine the required width and the entry label
        help_position = min(self._action_max_length + 2,
                            self._max_help_position)
        help_width = max(self._width - help_position, 11)
        action_width = help_position - self._current_indent - 2
        action_header = self._format_action_invocation(action)
        deprecated = ''
          
        # no help; start on same line and add a final newline
        if not action.help:
            tup = self._current_indent, '', action_header
            action_header = '%*s%s' % tup

        # short action name; start on the same line and pad two spaces
        elif len(action_header) <= action_width:
            tup = self._current_indent, '', action_header
            action_header = '%*s%s  ' % tup  # '%*s%-*s  ' % tup
            indent_first = 0

        # long action name; start on the next line
        else:
            tup = self._current_indent, '', action_header
            action_header = '%*s%s' % tup
            indent_first = help_position
               
        # ER: 23711216. To display (deprecated) in the help if the parameter is marked deprecated 
        if self.param_dict and self.param_dict is not None:
            deprecated = Messages.OPAAS_CLI_DEPRECATED if action.dest in self.param_dict and 'deprecated' in self.param_dict[action.dest] \
                                         and self.param_dict[action.dest]['deprecated'] else ''

        # indent_spacing for adding the type of the argument
        indent_spacing = 2
        # collect the pieces of the action help
        parts = self._format_parameter(deprecated, indent_spacing, action_header)
            
        # Add the datatype to the options as <optionname>  (datatype) (|deprecated).
        if action.type:
            # action.type.__name__ will give the name of the class for eg: 'str'            
            try:
                data_type = Utils.DATA_TYPES.get(action.type)
                if data_type is None:
                    if 'FileType' in str(action.type):
                        data_type = Utils.DATA_TYPES.get(str(action.type))
            except:
                # initialise to an empty string
                data_type = '' 
            parts.append('%*s%s%*s%s\n' % (indent_spacing, '', '(%s)' % data_type, 
                                           indent_spacing, '', '(%s)' % deprecated if deprecated and len(deprecated) > 1 else ''))
        
        # to check if this is a list as it has nargs='+'    
        elif '[ ...]' in action_header:
            parts = self._format_paramater_help_display_list(action_header, deprecated)
            # add the data type to the action_header
            data_type = Utils.DATA_TYPES.get('list')
            parts.append('%*s%s%*s%s\n' % (indent_spacing, '', '%s' % data_type,
                                           indent_spacing, '', '(%s)' % deprecated if deprecated and len(deprecated) > 1 else ''))
        
        else:
            # adding a newline if the the header doesn't end with one       
            if not action_header.endswith('\n'):
                parts.append('\n')
            
        # if there was help for the action, add lines of help text
        if action.help:
            help_text = self._expand_help(action)
            # _split_lines is overrided. Look method for explanation.            
            help_lines = self._split_lines(help_text, self._help_overrided_width_text_length)
            # parts.append('%*s%s\n' % (self._help_indent_option, '', help_lines[0].strip()))
            for line in help_lines:
                if len(line) > self._help_overrided_width_text_length:
                    wrappedText = textwrap.wrap(line, self._help_overrided_width_text_length)
                    for text in wrappedText:
                        parts.append('%*s%s\n' % (self._help_indent_option, '', text.strip()))
                else:
                    parts.append('%*s%s\n' % (self._help_indent_option, '', line.strip()))
            # add a new line for space seperation between options.
            parts.append('\n')

        # or add a newline if the description doesn't end with one
        elif not action_header.endswith('\n'):
            parts.append('\n')

        # if there are any sub-actions, add their help as well
        for subaction in self._iter_indented_subactions(action):
            parts.append(self._format_action(subaction))

        # return a single string
        return self._join_parts(parts)
    
    def _strike_text(self, text):
        # used to indicate that a param is deprecated
        result = ''
        for c in text:
            result = result + '\u0336' + c 
        return result
    
    def _format_parameter(self, deprecated, indent_spacing, action_header):
        if deprecated and len(deprecated) > 1 and not self._utils.isWindows():
            return ['%*s%s%*s' % (indent_spacing, '', 
                                   FormatText.bold(self._strike_text(action_header.strip())), indent_spacing, '')]
        else: 
            return [FormatText.bold(action_header)]


class OPCCustomHelpFormatter(object):
    # a custom help formatter to display the help 
    def __init__(self, isServiceOrCommand=False, argumentParserParameter=False, service_type_name=None):
        """
            :type argumentParserParameter:bool
            :param argumentParserParameter: differentiate to format the parameter help with conditions
            
            :type isServiceOrCommand:bool
            :param isServiceOrCommand: defaults to indicate its command level, else its service level
        """
        self._parser = None
        self._isArgumentParser = argumentParserParameter
        self._isServiceOrCommand = isServiceOrCommand
        self._leading_description_space = 7
        self._leading_space_header = 2
        self._max_description_length = 78
        self._original_service_type_name = service_type_name
        
    @property
    def parser(self):
        return self._parser
    
    @parser.setter 
    def parser(self, value):
        self._parser = value
    
    def __call__(self, args_extras, args_parsed, placeholder=None):
        self.display_help()
        
    def display_help(self):
        sys.stdout.write (self._print_help())
    
    # to remove the [ ...] when displaying help
    def _format_argument_display_list(self, argmt_string):
        if '[ ...]' in argmt_string:
            args_replace = argmt_string.replace(' [ ...]', '')
            return args_replace.strip()
        else:
            return argmt_string
    
    # format the payload json for example
    def _format_json_payload(self, payload):
        data = payload
        try:
            data_dict = json.loads(payload, object_pairs_hook=OrderedDict)
            data = json.dumps(data_dict, indent=4, separators=(',',':'))
            return data
        except:
            pass
        
        return payload            
    
    def _print_help(self):
        ret = []

        # display the description.
        description = self._parser.description
        if description:
            description = self.format_help_text(description.strip(), True)
            ret.append('\n' + FormatText.bold(Messages.OPAAS_CLI_HELP_DESCRIPTION) + '\n%s\n' % description)
        
        # to display the usage as the synopsis and add the required parameters
        # or arguments if any exists for parameter help.
        if isinstance(self._parser, argparse.ArgumentParser):
            synopsis = self._parser.format_usage().split(':', 1)[1]
            # strip the usage: to remove the white space and add custom indent.
            synopsis = '%s\n' % self.format_cmd_name_help(synopsis.strip())
            if self._isArgumentParser:
                synopsis_req_parameters = []
                for action in self._parser._actions:
                    param_name = self._format_argument_display_list(self._parser.formatter_class.get_format_actions(self._parser, action))
                    if action.required:
                        synopsis_req_parameters.append(self.format_cmd_name_help('%s <value>\n' % param_name, self._leading_description_space))
                    else:
                        synopsis_req_parameters.append(self.format_cmd_name_help('[%s <value>]\n' % param_name, self._leading_description_space))
                synopsis = synopsis + ''.join(synopsis_req_parameters)
        else:
            synopsis = None  # self._parser.usage
        
        if synopsis:
            # synopsis = synopsis.replace('%s ' % appname, '')
            ret.append(FormatText.bold(Messages.OPAAS_CLI_HELP_SYNOPSIS) + '\n%s\n' % synopsis)    
        
        # to display the service or commands.
        commands = self.format_dict_description(self._parser.command_list)
        if commands:
            if self._isServiceOrCommand:
                ret.append(FormatText.bold(Messages.OPAAS_CLI_HELP_SERVICES) + '\n%s\n\n' % commands)
            else:
                ret.append(FormatText.bold(Messages.OPAAS_CLI_HELP_COMMANDS) + '\n%s\n\n' % commands)
        
        # to display the optional arguments or parameters
        options = self._parser.formatter_class.format_options(self._parser)
        if options:
            ret.append(FormatText.bold(Messages.OPAAS_CLI_HELP_PARAMETERS) + '\n%s\n' % options)   
            
        # to display the examples for command/service if exists.
        examples = self._parser.get_examples
        if examples:
            # BUG FIX: 27112221. replace the service type with the service mapping for backward compatibility
            if self._original_service_type_name is not None and self._original_service_type_name.lower() in LocalizationConstants.ServiceMapping:
                examples = examples.replace(self._original_service_type_name, LocalizationConstants.ServiceMapping[self._original_service_type_name.lower()])
            ret.append(FormatText.bold(Messages.OPAAS_CLI_HELP_EXAMPLES) + '\n%s\n' % self.format_help_text(examples))   
            payload = self._parser.get_payload
            if payload:
                ret.append(FormatText.bold(Messages.OPAAS_CLI_HELP_PAYLOAD) + '\n%s%s\n\n' \
                           % (Messages.OPAAS_CLI_HELP_SAMPLE_PAYLOAD, self._format_json_payload(payload)))
        
        # return the whole help text.
        return ''.join(ret)
    
    # format the text for example and description to indent to 2.
    # if formatting for description, the description param is
    # set to True.
    def format_help_text(self, text, description=False):
        text_split = text.splitlines()
        format_ret = []
        for ex in text_split:
            if description and len(ex) > self._max_description_length:
                # executed only for description.
                wrappedText = textwrap.wrap(ex, self._max_description_length)
                for text in wrappedText:
                    format_ret.append('%*s%s\n' % (self._leading_space_header, '', text.strip()))                
            else:
                format_ret.append('%*s%s\n' % (self._leading_space_header, '', ex.strip()))
        return ''.join(format_ret)
        
    def format_dict_description(self, command_list_description):
        # this is to format the command list with description that 
        # gets displayed on print_help of the parser.
        result = []
        if command_list_description and len(command_list_description) >= 1 :
            result = []
            maxlen = len(max(command_list_description, key=len))
            for name, description in command_list_description.items():
                format_name = self.format_cmd_name_help(name, bulletHeader=True)
                if len(description) > self._max_description_length:
                    format_description = textwrap.shorten(description, self._max_description_length, placeholder='...')
                else: 
                    format_description = description 
                fill_value_description_leading = len(format_description) + self._leading_description_space
                format_description = '{message: >{fill}}'.format(message=format_description, fill=fill_value_description_leading)
                # append the name and the description to the result.
                result.append("%s\n%s" % (format_name, format_description))
            # return the result with the adding the new line character.
            return '\n'.join(result) 
        # returns an empty list.
        return result 
    
    def format_cmd_name_help(self, name, leading_space=2, bulletHeader=False):
        if bulletHeader:
            name = "o %s" % name
        max_space_len_cmd_name_leading = leading_space
        # adds indent with space in the begining of the name.'>' means adds the spaces at the beginning 
        fill_value_name_leading = max_space_len_cmd_name_leading + len(name)   
        format_name = '{message: >{fill}}'.format(message=name, fill=fill_value_name_leading)
        return format_name      


