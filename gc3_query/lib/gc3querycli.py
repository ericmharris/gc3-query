# -*- coding: utf-8 -*-

"""Module for cli-specific parts of gc3query.



"""

import click

from gc3_query import __version__
from gc3_query.lib import *
from gc3_query.lib.logging import Logging, get_logging
from gc3_query.lib.gc3querylib import *

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help', '-?'], # help_option_names sets tokens that come after a command that'll trigger help.
                        ignore_unknown_options=True)




@click.group(invoke_without_command=False, context_settings=CONTEXT_SETTINGS, help="""
Help message for gc3_query cli.
""")
@click.version_option(__version__, '-v', '--version', message='%(version)s')
@click.option('-d', '--debug', is_flag=True, help='Show additional debug information.')
@click.option('-?', '-h', '--help', is_flag=True, help='Show this message and exit.')
@click.pass_context
def cli(ctx, debug, help):
    click.echo(f'Running cli() with context: {ctx}')
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARN)


@cli.command(help="Help for util_hello", short_help="Short help for util_hello", epilog="Epilog for util_hello")
@click.option('--opt', '-o', help="Help for opt")
@click.pass_context
def test_gc3_query_command(ctx: click.core.Context, opt: str) -> None:
    click.echo(click.style(f'gc3query.test_gc3_query_command(): {opt}', fg='green'))
    _info(f'Test logging for gc3_query.')
    print(f'context: {ctx}')
    sys.exit(0)
