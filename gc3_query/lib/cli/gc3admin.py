# -*- coding: utf-8 -*-

"""Module for cli-specific parts of gc3admin.



"""
import sys
import os

import collections

import click

import cookiecutter
import cookiecutter.main
import cookiecutter.config


from gc3_query import __version__
from gc3_query.lib import *
from gc3_query.lib import BASE_DIR
from gc3_query.lib.logging import get_logging
from gc3_query.lib.gc3adminlib import *

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help', '-?'], # help_option_names sets tokens that come after a command that'll trigger help.
                        ignore_unknown_options=True)




@click.group(invoke_without_command=False, context_settings=CONTEXT_SETTINGS, help="""
Help message for gc3query cli.
""")
@click.version_option(__version__, '-v', '--version', message='%(version)s')
@click.option('-d', '--debug', is_flag=True, help='Show additional debug information.')
@click.option('-?', '-h', '--help', is_flag=True, help='Show this message and exit.')
@click.pass_context
def cli(ctx, debug, help):
    ctx.gc3_config = {}
    click.echo(f'Running cli() with context: {ctx}')
    if debug:
        ctx.gc3_config['logging_level'] = 'DEBUG'
    else:
        ctx.gc3_config['logging_level'] = 'WARNING'


# @cli.command(help="Help for util_hello", short_help="Short help for util_hello", epilog="Epilog for util_hello")
# @click.option('--opt', '-o', help="Help for opt")
# @click.pass_context
# def test_gc3query_command(ctx: click.core.Context, opt: str) -> None:
#     click.echo(click.style(f'gc3admin.test_gc3query_command(): {opt}', fg='green'))
#     _info(f'Test logging for gc3query.')
#     print(f'context: {ctx}')
#     sys.exit(0)


def to_package_style(text):
    if not text:
        return text

    text = text.strip()
    url_txt = ''
    for ch in text:
        url_txt += ch if ch.isalnum() or ch == '.' else ' '

    count = -1
    while count != len(url_txt):
        count = len(url_txt)
        url_txt = url_txt.strip()
        url_txt = url_txt.replace('  ', ' ')
        url_txt = url_txt.replace(' ', '-')
        url_txt = url_txt.replace('--', '-')

    return url_txt.lower()



GameCreateInfo = collections.namedtuple('GameCreateInfo', 'project_name full_name game_type working_dir')

def gather_inputs():
    config = cookiecutter.config.get_user_config()
    ctx = config.get('default_context')

    full_name = ctx.get('full_name')
    if not full_name:
        full_name = input('What is your full name? ')

    game_type = None
    while game_type not in ['hilo', 'pacman', 'pong']:
        game_type = input('Game type? [hilo, pacman, pong]? ')

    package_name = input("What do you call your game? ")
    package_name = to_package_style(package_name)

    working_dir = input('Full path where to create the project [must exist]? ')
    while not os.path.exists(working_dir):
        print("Oh, that doesn't exist, try again...")
        working_dir = input('Full path where to create the project [must exist]? ')

    return GameCreateInfo(package_name, full_name, game_type, working_dir)


def build_game(info):
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





@cli.command(help="Help for util_hello", short_help="Short help for util_hello", epilog="Epilog for util_hello")
@click.option('--target-dir', '-d', help="Help for taget dir")
@click.pass_context
def setup_mongodb(ctx: click.core.Context, target_dir: str=None) -> None:
    if not target_dir:
        target_dir = BASE_DIR
    click.echo(click.style(f'gc3admin.setup_mongodb(): target_dir={target_dir}', fg='green'))
    _info(f'Test logging for gc3admin.')
    print(f'context: {ctx}')
    sys.exit(0)


