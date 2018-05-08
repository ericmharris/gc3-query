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



# GameCreateInfo = collections.namedtuple('GameCreateInfo', 'project_name full_name game_type working_dir')

class SetupMongoDB():

    def __init__(self, ctx: click.core.Context, target_dir: str=None):
        self.user_inputs = self.gather_inputs(ctx=ctx, target_dir=target_dir)


    # def to_package_style(self, text):
    #     if not text:
    #         return text
    #
    #     text = text.strip()
    #     url_txt = ''
    #     for ch in text:
    #         url_txt += ch if ch.isalnum() or ch == '.' else ' '
    #
    #     count = -1
    #     while count != len(url_txt):
    #         count = len(url_txt)
    #         url_txt = url_txt.strip()
    #         url_txt = url_txt.replace('  ', ' ')
    #         url_txt = url_txt.replace(' ', '-')
    #         url_txt = url_txt.replace('--', '-')
    #
    #     return url_txt.lower()




    def gather_inputs(self, ctx: click.core.Context, target_dir: str=None):
        config = cookiecutter.config.get_user_config()
        ctx = config.get('default_context')

        mongodb_bin_dir = Path(click.prompt('Please enter full path to MongoDB bin directory', type=str))
        mongodb_bin = mongodb_bin_dir.joinpath('mongod', click.echo(click.style(f' mongodb_bin={mongodb_bin}', fg='green')))
        _debug(f'mongodb_bin_dir={mongodb_bin_dir}, mongodb_bin={mongodb_bin}')

        full_name = ctx.get('full_name')
        if not full_name:
            full_name = input('What is your full name? ')

        # game_type = None
        # while game_type not in ['hilo', 'pacman', 'pong']:
        #     game_type = input('Game type? [hilo, pacman, pong]? ')


        working_dir = input('Full path where to create the project [must exist]? ')
        while not os.path.exists(working_dir):
            print("Oh, that doesn't exist, try again...")
            working_dir = input('Full path where to create the project [must exist]? ')

        return GameCreateInfo(package_name, full_name, game_type, working_dir)


    def deploy(self, info):
        print("Building game {} of type {}, just a moment ...".format(
            info.project_name, info.game_type), flush=True)

        working_dir = os.path.abspath(os.path.dirname(__file__))
        template = os.path.join(working_dir, 'templates', 'cookiecutter-use-api')

        proj_dir = cookiecutter.main.cookiecutter(
            template,
            no_input=True,
            output_dir=info.working_dir,
            extra_context={
                'project_name': info.project_name,
                'full_name': info.full_name,
                'game_type': info.game_type
            }
        )

        return proj_dir




