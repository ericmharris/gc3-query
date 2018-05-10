# -*- coding: utf-8 -*-

"""Library module for gc3query.



"""
# __all__ = ['UnexpectedThingHappenedException', 'InvalidThingHappenedException']

import sys, os

import click

import collections

import cookiecutter
import cookiecutter.main
import cookiecutter.config


from gc3_query import __version__
from gc3_query.lib import *
from gc3_query.lib import BASE_DIR
from gc3_query.lib.logging import get_logging

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help', '-?'], # help_option_names sets tokens that come after a command that'll trigger help.
                        ignore_unknown_options=True)

class BaseException(Exception):
    """
    Base custom exception
    """

    def __init__(self, msg=None, thing=None, other_thing=None):
        self.msg = msg
        self.thing = thing
        self.other_thing = other_thing

    def __str__(self):
        exception_msg = f"Message: {self.msg}\n"
        if self.thing is not None:
            exception_msg = f"{exception_msg}, other relevant thing\n"
        if self.other_thing is not None:
            other_thing = "\n".join(self.other_thing)
            exception_msg = f"{exception_msg}, other_thing:\n{other_thing}"
        return exception_msg


class UnexpectedThingHappenedException(BaseException):
    """Thrown when an unexpected thing happend . """
    def __init__(self, msg=None, thing=None, other_thing=None, alert_text=None):
        super().__init__(msg, thing, other_thing)
        self.alert_text = alert_text

    def __str__(self):
        return "Alert Text: {}\n{}".format(self.alert_text, super(UnexpectedThingHappenedException, self).__str__())


class InvalidThingHappenedException(BaseException):
    """
    Thrown when an invalid thing happened
    """
    pass



# GameCreateInfo = collections.namedtuple('GameCreateInfo', 'mongodb_dir_name full_name game_type working_dir')

class SetupMongoDB():
    template_name: str = 'basic_config'
    template_path: str = str(BASE_DIR.joinpath(f'opt/templates/cookiecutter/mongodb/{template_name}'))

    def __init__(self, ctx: click.core.Context, mongodb_bin_dir: str = None):
        self.mongodb_bin_dir = Path(mongodb_bin_dir) if mongodb_bin_dir else mongodb_bin_dir
        self.user_inputs = self.gather_inputs(ctx=ctx, mongodb_bin_dir=self.mongodb_bin_dir)
        self.proj_dir = self.deploy(user_inputs=self.user_inputs)


    def gather_inputs(self, ctx: click.core.Context, mongodb_bin_dir: Path=None):
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



        if mongodb_bin_dir is None:
            mongodb_bin_dir = Path(click.prompt('Please enter full path to MongoDB bin directory', type=str))
        mongod_bin_name = 'mongod.exe' if 'win' in sys.platform else 'mongod'
        mongod_bin = mongodb_bin_dir.joinpath(mongod_bin_name)
        _debug(f'mongodb_bin_dir={mongodb_bin_dir}, mongod_bin={mongod_bin}')
        user_inputs['mongod_bin'] = str(mongod_bin)

        gc3_var_dir = BASE_DIR.joinpath('var')
        mongodb_setup_dir = gc3_var_dir.joinpath('mongodb')
        mongodb_data_dir = mongodb_setup_dir.joinpath('data')
        mongodb_logs_dir = mongodb_setup_dir.joinpath('logs')
        mongodb_configs_dir = mongodb_setup_dir.joinpath('configs')
        mongodb_log_file = mongodb_logs_dir.joinpath('mongo-service.log')
        mongodb_config_file = mongodb_configs_dir.joinpath('mongo-service.config')

        _debug(f"gc3_var_dir={gc3_var_dir}, mongodb_setup_dir={mongodb_setup_dir}")
        user_inputs['gc3_var_dir'] = str(gc3_var_dir)
        user_inputs['mongodb_setup_dir'] = str(mongodb_setup_dir)
        user_inputs['mongodb_data_dir'] = str(mongodb_data_dir)
        user_inputs['mongodb_logs_dir'] = str(mongodb_logs_dir)
        user_inputs['mongodb_log_file'] = str(mongodb_log_file)
        user_inputs['mongodb_config_file'] = str(mongodb_config_file)
        # user_inputs['ASDF'] = str(ASDF)

        user_inputs["mongodb_dir_name"] =  "mongodb"
        user_inputs["mongodb_bin_dir"] = str(mongod_bin)
        user_inputs["listen_port"] = 9000

        return user_inputs



    def deploy(self, user_inputs: Dict[str, Any]):
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
        _debug(f"user_inputs={user_inputs}, template={SetupMongoDB.template_path}, output_dir={user_inputs['mongodb_setup_dir']}")
        _debug(f"extra_context={user_inputs}")

        proj_dir = cookiecutter.main.cookiecutter(
            template=SetupMongoDB.template_path,
            no_input=True,
            output_dir=user_inputs['mongodb_setup_dir'],
            extra_context=user_inputs
        )

        return proj_dir




