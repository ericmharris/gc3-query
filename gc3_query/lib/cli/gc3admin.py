# -*- coding: utf-8 -*-

"""Module for cli-specific parts of gc3admin.



"""
import sys
import os
import pathlib

import click


from gc3_query import __version__
from gc3_query.lib import *
from gc3_query.lib import BASE_DIR
from gc3_query.lib.logging import get_logging
from gc3_query.lib.gc3admin import *

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
    # named ctx.parent.gc3_config to other functions in cli group.
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



@cli.command(help="Help for util_hello", short_help="Short help for util_hello", epilog="Epilog for util_hello")
@click.option('--mongodb-bin-dir', '-b', help="Directory containing mongodb executables, eg. mongod.exe")
@click.pass_context
def setup_mongodb(ctx: click.core.Context, mongodb_bin_dir: str = None) -> None:
    click.echo(click.style(f'gc3admin.setup_mongodb(): target_dir={mongodb_bin_dir}', fg='green'))
    _warning(f'Test logging for gc3admin.')
    print(f'context: {ctx.parent.gc3_config}')
    setup_mongo_db = SetupMongoDB(ctx=ctx, mongodb_bin_dir=mongodb_bin_dir)






    sys.exit(0)


