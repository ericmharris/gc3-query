# Copyright (c) 2015 Oracle and/or its affiliates. All rights reserved.
# created by sahit.gollapudi
import json
import argparse
try:
    from .utils import Utils
except:
    from utils import Utils

class OPCArgument(object):
    #TODO: FILE, JSON  type_name needs to be revistied
    DATA_TYPES = {
                'string': str,
                'timestamp': str,
                'list': 'list',
                'array': 'list',
                'float': float,
                'integer': int,
                'long': int,
                'boolean': 'bool',
                'double': float,
                'json':str,
                'file':argparse.FileType('r')
            }

    def __init__(self, argument_name, type, description,
                 dest, is_arg_required, action, alias_name=None, choices_list=None):
        """
            :type_name argument_name: str
            :param argument_name: the optional argument name for the command

            :type_name type:str
            :param type: the data type_name for the argument

            :type_name description: str
            :param description: the text that gets displayed for the help

            :type_name dest: str
            :param dest: the keyword that holds the arg value entered

            :type_name is_arg_required: boolean
            :param is_arg_required: to specify if the optional argument is required or not

            :type_name action: str
            :param action: to specify the action for that argument.

            :type_name alias_name: str
            :param alias_name: to specify the short name for the argument.

            :type_name choices_list: str
            :param choices_list: comma separated values.
        """
        self._arg_name = argument_name
        self._type = self.gettype(type)
        self._required = is_arg_required
        # the dest is used to store the value of the argument.
        self._dest = dest
        self._description = description
        self._action = action
        self._alias_name = alias_name
        self._choices_list = choices_list
        self._utils = Utils()

    @property
    def arg_name(self):
        return self._arg_name

    @property
    def description(self):
        return self._description

    @property
    def required(self):
        return self._required

    @property
    def type(self):
        return self._type

    @property
    def dest_name(self):
        return self._dest

    @property
    def action(self):
        return self._action

    @property
    def alias_name(self):
        return self._alias_name

    @property
    def choices_list(self):
        if self._choices_list is not None:
            choices_values = self._choices_list.split(',')
            return [word.strip() for word in choices_values]
        return self._choices_list

    @property
    def argument_option_name(self):
        converted_param_name = self.arg_name
        try:
            converted_param_name = self._utils.convertCamelCase(self.arg_name)
        except:
            pass

        return "--" + converted_param_name

    @property
    def argument_option_alias_name(self):
        if self.alias_name:
            return "-" + self.alias_name
        else:
            return None

    def add_arg_to_parser(self, parser):

        cmdargs = {}
        arg_cli_name = self.argument_option_name
        arg_cli_alias_name = self.argument_option_alias_name

        # this is differentiate between required and optional arguments.
        if self.required:
            cmdargs['required'] = self.required
            #arg_cli_name = self.arg_name
        if self.dest_name is not None:
            cmdargs['dest'] = self.dest_name
        # this is to not print the destination values in the help display which are uppercased.
        cmdargs['metavar'] = ''
        if self.action is not None:
            cmdargs['action'] = self.action
        if self.description is not None:
            cmdargs['help'] = self.description
        if self.type is not None:
            if self.type == 'list':
                cmdargs['nargs'] = '+'
            else:
                cmdargs['type_name'] = self.type
        if self.choices_list is not None:
            cmdargs['choices'] = self.choices_list

        if arg_cli_alias_name:
            parser.add_argument(arg_cli_alias_name, arg_cli_name, **cmdargs)
        else:
            parser.add_argument(arg_cli_name, **cmdargs)

    def gettype(self, type):
        return self.DATA_TYPES.get(type.lower())
