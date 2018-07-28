# -*- coding: utf-8 -*-

"""
#@Filename : cookie_cutter_base
#@Date : [7/27/2018 1:09 PM]
#@Poject: gc3-query
#@AUTHOR : emharris

~~~~~~~~~~~~~~~~

<DESCR SHORT>

<DESCR>
"""

################################################################################
## Standard Library Imports
import sys, os
import abc

################################################################################
## Third-Party Imports
from dataclasses import dataclass
import click
import cookiecutter

################################################################################
## Project Imports
from gc3_query.lib import *

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


class CookieCutterBase:

    def __init__(self, ctx: click.core.Context, template_name: str, template_path: Path, command_line_options: Dict[str, Any] = None):
        self.ctx = ctx
        self.template_name = template_name
        self.template_path = template_path
        self.command_line_options = command_line_options
        self.user_inputs = self.gather_inputs(ctx=ctx, mongodb_bin_dir=self.mongodb_bin_dir, listen_port=listen_port)

    @abc.abstractmethod
    def gather_inputs(self, ctx: click.core.Context, command_line_options: Dict[str, Any] = None) -> Dict[str,Any]:
        """

        :param ctx:
        :param command_line_options:
        :return:
        """
        user_inputs = {}
        cc_user_config = cookiecutter.config.get_user_config()
        cc_default_ctx = cc_user_config.get("default_context")

        _debug(f"cc_user_config={cc_user_config}")
        _debug("cc_default_ctx={cc_default_ctx}")

        # full_name = cc_user_config.get('full_name')
        # if not full_name:
        #     full_name = input('What is your full name? ')
        # game_type = None
        # while game_type not in ['hilo', 'pacman', 'pong']:
        #     game_type = input('Game type_name? [hilo, pacman, pong]? ')
        # working_dir = input('Full file_path where to create the project [must exist]? ')
        # while not os.file_path.exists(working_dir):
        #     print("Oh, that doesn't exist, try again...")
        #     working_dir = input('Full file_path where to create the project [must exist]? ')
        # return GameCreateInfo(package_name, full_name, game_type, working_dir)
        return user_inputs

    def deploy(self) -> bool:
        """

        :return:


        def cookiecutter(
            template, checkout=None, no_input=False, extra_context=None,
            replay=False, overwrite_if_exists=False, output_dir='.',
            config_file=None, default_config=False, password=None):

            API equivalent to using Cookiecutter at the command line.

            :param template: A directory containing a project template directory,
                or a URL to a git repository.
            :param checkout: The branch, tag or commit ID to checkout after clone.
            :param no_input: Prompt the user at command line for manual configuration?
            :param extra_context: A dictionary of context that overrides default
                and user configuration.
            :param: overwrite_if_exists: Overwrite the contents of output directory
                if it exists
            :param output_dir: Where to output the generated project dir into.
            :param config_file: User configuration file file_path.
            :param default_config: Use default values rather than a atoml_cfg file.
            :param password: The password to use when extracting the repository.
    """

        working_dir = os.path.abspath(os.path.dirname(__file__))
        template = os.path.join(working_dir, "templates", "cookiecutter-use-api")
        _debug(
            f"user_inputs={self.user_inputs}, template={SetupMongoDB.template_path}, output_dir={self.user_inputs['mongodb_setup_dir']}"
        )
        _debug(f"extra_context={self.user_inputs}")
        _debug(f"force={self.force}")

        proj_dir = cookiecutter.main.cookiecutter(
            template=SetupMongoDB.template_path,
            no_input=True,
            overwrite_if_exists=self.force,
            output_dir=self.user_inputs["gc3_var_dir"],
            extra_context=self.user_inputs,
        )

        self.proj_dir = proj_dir
        return True
