import os
import sys
from pathlib import Path
from typing import Dict, Any

import click
import cookiecutter
import cookiecutter.main
import cookiecutter.config

from gc3_query.lib import BASE_DIR
from gc3_query.lib.gc3admin.gc3admin import _debug

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help', '-?'], # help_option_names sets tokens that come after a command that'll trigger help.
                        ignore_unknown_options=True)



class SetupHomeKitty():
    """


[http://www.9bis.net/kitty/?page=Command-line%20options]
-classname: to define a specific class name for the window
-cmd: to define a startup auto-command
-convert-dir: convert registry settings to savemode=dir mode
-convert-reg: backup session settings from savemode=dir mode to registry
-edit: edit the settings of a session
-fileassoc: associate .ktx files with KiTTY
-folder: directly open a specific folder (for savemode=dir mode only)
-fullscreen: start directly in full screen mode
-keygen: start the integrated ssh key generator
-kload: load a .ktx file (that contains session settings)
-launcher: start the session launcher
-log: create a log file
-loginscript: load a login script file
-nobgimage: to disable background image feature
-noctrltab: disable CTRL+TAB feature
-nofiles: disable the creation of default ini file if it does not exist
-noicon: disable icons support
-noshortcuts: disable all shortcuts
-notrans: disable Transparency support
-nozmodem: disable ZModem support
-pass: set a password
-putty: disable with one option all KiTTY new features
-runagent: start the integrated SSH agent
-send-to-tray: start a session directly in the system tray (useful for SSH tunnels)
-sendcmd: to send a command to all windows with the same class name
-sshhandler: create protocols associations (telnet://, ssh://) for internet explorer
-title: set a window title
-version: only open the about box
-xpos: to set the initial X position
-ypos: to set the initial Y position




    [emharris@win10x64-emharris:master .kitty]# cp kitty.ini C:\ProgramData\chocolatey\lib\kitty\tools
	[emharris@win10x64-emharris:master .kitty]# ls
	kitty.ini
    [emharris@win10x64-emharris:master .kitty]# kitty.exe -convert-dir
    """
    template_name: str = 'basic_config'
    template_path: str = str(BASE_DIR.joinpath(f'opt/templates/cookiecutter/kitty/{template_name}'))

    def __init__(self, ctx: click.core.Context, kitty_bin_dir: str = None, listen_port: int=7117, force: bool=False):
        self.kitty_bin_dir = Path(kitty_bin_dir) if kitty_bin_dir else kitty_bin_dir
        self.listen_port = listen_port
        self.force = force
        self.user_inputs = self.gather_inputs(ctx=ctx, kitty_bin_dir=self.kitty_bin_dir, listen_port=listen_port)
        self.proj_dir = self.deploy(user_inputs=self.user_inputs, force=force)


    def gather_inputs(self, ctx: click.core.Context, kitty_bin_dir: Path, listen_port:int):
        user_inputs = {}
        cc_user_config = cookiecutter.config.get_user_config()
        cc_default_ctx = cc_user_config.get('default_context')

        _debug(f"cc_user_config={cc_user_config}")
        _debug("cc_default_ctx={cc_default_ctx}")


        # full_name = cc_user_config.get('full_name')
        # if not full_name:
        #     full_name = input('What is your full name? ')
        # game_type = None
        # while game_type not in ['hilo', 'pacman', 'pong']:
        #     game_type = input('Game type? [hilo, pacman, pong]? ')
        # working_dir = input('Full path where to create the project [must exist]? ')
        # while not os.path.exists(working_dir):
        #     print("Oh, that doesn't exist, try again...")
        #     working_dir = input('Full path where to create the project [must exist]? ')
        # return GameCreateInfo(package_name, full_name, game_type, working_dir)



        if kitty_bin_dir is None:
            kitty_bin_dir = Path(click.prompt('Please enter full path to Kitty bin directory', type=str))
        mongod_bin_name = 'mongod.exe' if 'win' in sys.platform else 'mongod'
        mongod_bin = kitty_bin_dir.joinpath(mongod_bin_name)
        _debug(f'kitty_bin_dir={kitty_bin_dir}, mongod_bin={mongod_bin}')
        user_inputs['mongod_bin'] = str(mongod_bin)

        gc3_var_dir = BASE_DIR.joinpath('var')
        kitty_setup_dir = gc3_var_dir.joinpath('kitty')
        kitty_data_dir = kitty_setup_dir.joinpath('data')
        kitty_logs_dir = kitty_setup_dir.joinpath('logs')
        kitty_configs_dir = kitty_setup_dir.joinpath('config')
        kitty_service_log_file = kitty_logs_dir.joinpath('mongo-service.log')
        kitty_cmd_log_file = kitty_logs_dir.joinpath('mongo-cmd.log')
        kitty_service_config_file = kitty_configs_dir.joinpath('mongo-service.config')
        kitty_cmd_config_file = kitty_configs_dir.joinpath('mongo-cmd.config')

        _debug(f"gc3_var_dir={gc3_var_dir}, kitty_setup_dir={kitty_setup_dir}")
        user_inputs['gc3_var_dir'] = str(gc3_var_dir)
        user_inputs['kitty_setup_dir'] = str(kitty_setup_dir)
        user_inputs['kitty_data_dir'] = str(kitty_data_dir)
        user_inputs['kitty_logs_dir'] = str(kitty_logs_dir)
        user_inputs['kitty_service_log_file'] = str(kitty_service_log_file)
        user_inputs['kitty_cmd_log_file'] = str(kitty_cmd_log_file)
        user_inputs['kitty_service_config_file'] = str(kitty_service_config_file)
        user_inputs['kitty_cmd_config_file'] = str(kitty_cmd_config_file)
        # user_inputs['ASDF'] = str(ASDF)

        user_inputs["kitty_dir_name"] =  "kitty"
        user_inputs["kitty_bin_dir"] = str(mongod_bin)
        user_inputs["listen_port"] = listen_port

        return user_inputs



    def deploy(self, user_inputs: Dict[str, Any], force: bool):
        """

        :param user_inputs:
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
            :param config_file: User configuration file path.
            :param default_config: Use default values rather than a config file.
            :param password: The password to use when extracting the repository.
    """



        working_dir = os.path.abspath(os.path.dirname(__file__))
        template = os.path.join(working_dir, 'templates', 'cookiecutter-use-api')
        _debug(
            f"user_inputs={user_inputs}, template={SetupHomeKitty.template_path}, output_dir={user_inputs['kitty_setup_dir']}")
        _debug(f"extra_context={user_inputs}")
        _debug(f"force={force}")

        proj_dir = cookiecutter.main.cookiecutter(
            template=SetupHomeKitty.template_path,
            no_input=True,
            overwrite_if_exists=force,
            output_dir=user_inputs['gc3_var_dir'],
            extra_context=user_inputs
        )

        return proj_dir
