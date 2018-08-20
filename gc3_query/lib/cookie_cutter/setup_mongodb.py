import os
import sys
from pathlib import Path
from typing import Dict, Any

import click
import cookiecutter
import cookiecutter.main
import cookiecutter.config

from gc3_query.lib import gc3_cfg, BASE_DIR_FIX_ME
from gc3_query.lib.gc3admin.gc3admin import _debug
from gc3_query.lib.cookie_cutter import CookieCutterBase

CONTEXT_SETTINGS = dict(
    help_option_names=[
        "-h",
        "--help",
        "-?",
    ],  # help_option_names sets tokens that come after a command that'll trigger help.
    ignore_unknown_options=True,
)

class SetupMongoDB(CookieCutterBase):

    def __init__(self, ctx: click.core.Context, command_line_options: Dict[str, Any] = None):
        super().__init__(ctx, template_name, template_path)
        self.user_inputs = self.gather_inputs(ctx=ctx, command_line_options=self.command_line_options)


#
# class SetupMongoDB(CookieCutterBase):
#
#     def __init__( self, ctx: click.core.Context, mongodb_bin_dir: str = None, listen_port: int = 7117, force: bool = False ):
#         template_name: str = "basic_config"
#         template_path: str = str(BASE_DIR.joinpath(f"opt/templates/cookiecutter/mongodb/{template_name}"))
#         self.mongodb_bin_dir = ( Path(mongodb_bin_dir) if mongodb_bin_dir else Path(r"C:\Program Files\MongoDB\Server\3.6\bin"))
#         self.listen_port = listen_port
#         self.force = force
#         self.user_inputs = self.gather_inputs(ctx=ctx, mongodb_bin_dir=self.mongodb_bin_dir, listen_port=listen_port)
#         # self.proj_dir = self.deploy(user_inputs=self.user_inputs, force=force)
#         self.proj_dir = None
#
#     def gather_inputs(self, ctx: click.core.Context, mongodb_bin_dir: Path, listen_port: int):
#         user_inputs = {}
#         cc_user_config = cookiecutter.config.get_user_config()
#         cc_default_ctx = cc_user_config.get("default_context")
#
#         _debug(f"cc_user_config={cc_user_config}")
#         _debug("cc_default_ctx={cc_default_ctx}")
#
#         # full_name = cc_user_config.get('full_name')
#         # if not full_name:
#         #     full_name = input('What is your full name? ')
#         # game_type = None
#         # while game_type not in ['hilo', 'pacman', 'pong']:
#         #     game_type = input('Game type_name? [hilo, pacman, pong]? ')
#         # working_dir = input('Full file_path where to create the project [must exist]? ')
#         # while not os.file_path.exists(working_dir):
#         #     print("Oh, that doesn't exist, try again...")
#         #     working_dir = input('Full file_path where to create the project [must exist]? ')
#         # return GameCreateInfo(package_name, full_name, game_type, working_dir)
#
#         if not mongodb_bin_dir.exists():
#             mongodb_bin_dir = Path(click.prompt("Please enter full file_path to MongoDB bin directory", type=str))
#         mongod_bin_name = "mongod.exe" if "win" in sys.platform else "mongod"
#         mongod_bin = mongodb_bin_dir.joinpath(mongod_bin_name)
#         _debug(f"mongodb_bin_dir={mongodb_bin_dir}, mongod_bin={mongod_bin}")
#         user_inputs["mongod_bin"] = str(mongod_bin)
#
#         gc3_var_dir = BASE_DIR.joinpath("var")
#         mongodb_setup_dir = gc3_var_dir.joinpath("mongodb")
#         mongodb_data_dir = mongodb_setup_dir.joinpath("data")
#         mongodb_logs_dir = mongodb_setup_dir.joinpath("logs")
#         mongodb_configs_dir = mongodb_setup_dir.joinpath("atoml")
#         mongodb_service_log_file = mongodb_logs_dir.joinpath("mongo-service.log")
#         mongodb_cmd_log_file = mongodb_logs_dir.joinpath("mongo-cmd.log")
#         mongodb_service_config_file = mongodb_configs_dir.joinpath("mongo-service.atoml")
#         mongodb_cmd_config_file = mongodb_configs_dir.joinpath("mongo-cmd.atoml")
#
#         _debug(f"gc3_var_dir={gc3_var_dir}, mongodb_setup_dir={mongodb_setup_dir}")
#         user_inputs["gc3_var_dir"] = str(gc3_var_dir)
#         user_inputs["mongodb_setup_dir"] = str(mongodb_setup_dir)
#         user_inputs["mongodb_data_dir"] = str(mongodb_data_dir)
#         user_inputs["mongodb_logs_dir"] = str(mongodb_logs_dir)
#         user_inputs["mongodb_service_log_file"] = str(mongodb_service_log_file)
#         user_inputs["mongodb_cmd_log_file"] = str(mongodb_cmd_log_file)
#         user_inputs["mongodb_service_config_file"] = str(mongodb_service_config_file)
#         user_inputs["mongodb_cmd_config_file"] = str(mongodb_cmd_config_file)
#         # user_inputs['ASDF'] = str(ASDF)
#
#         user_inputs["mongodb_dir_name"] = "mongodb"
#         user_inputs["mongodb_bin_dir"] = str(mongod_bin)
#         user_inputs["listen_port"] = listen_port
#
#         return user_inputs
#
#     def deploy(self) -> bool:
#         """
#
#         :return:
#
#
#         def cookiecutter(
#             template, checkout=None, no_input=False, extra_context=None,
#             replay=False, overwrite_if_exists=False, output_dir='.',
#             config_file=None, default_config=False, password=None):
#
#             API equivalent to using Cookiecutter at the command line.
#
#             :param template: A directory containing a project template directory,
#                 or a URL to a git repository.
#             :param checkout: The branch, tag or commit ID to checkout after clone.
#             :param no_input: Prompt the user at command line for manual configuration?
#             :param extra_context: A dictionary of context that overrides default
#                 and user configuration.
#             :param: overwrite_if_exists: Overwrite the contents of output directory
#                 if it exists
#             :param output_dir: Where to output the generated project dir into.
#             :param config_file: User configuration file file_path.
#             :param default_config: Use default values rather than a atoml file.
#             :param password: The password to use when extracting the repository.
#     """
#
#         working_dir = os.path.abspath(os.path.dirname(__file__))
#         template = os.path.join(working_dir, "templates", "cookiecutter-use-api")
#         _debug(
#             f"user_inputs={self.user_inputs}, template={SetupMongoDB.template_path}, output_dir={self.user_inputs['mongodb_setup_dir']}"
#         )
#         _debug(f"extra_context={self.user_inputs}")
#         _debug(f"force={self.force}")
#
#         proj_dir = cookiecutter.main.cookiecutter(
#             template=SetupMongoDB.template_path,
#             no_input=True,
#             overwrite_if_exists=self.force,
#             output_dir=self.user_inputs["gc3_var_dir"],
#             extra_context=self.user_inputs,
#         )
#
#         self.proj_dir = proj_dir
#         return True
