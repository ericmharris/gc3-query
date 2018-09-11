# -*- coding: utf-8 -*-

"""
#@Filename : gc3export
#@Date : [8/11/2018 12:56 PM]
#@Poject: gc3-query
#@AUTHOR : emharris

~~~~~~~~~~~~~~~~

<DESCR SHORT>

<DESCR>
"""

################################################################################
## Standard Library Imports
import sys
from pprint import pprint

################################################################################
## Third-Party Imports
import click

################################################################################
## Project Imports
from gc3_query.lib.base_collections import OrderedDictAttrBase
from gc3_query.lib import gc3_cfg

from gc3_query.lib import get_logging
_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

CONTEXT_SETTINGS = dict(
    help_option_names=[
        "-h",
        "--help",
        "-?",
    ],  # help_option_names sets tokens that come after a command that'll trigger help.
    ignore_unknown_options=True,
)


@click.group(
    invoke_without_command=False,
    context_settings=CONTEXT_SETTINGS,
    help="""Help message for atoml cli.""", )
@click.version_option('0.1.0', "--version", message="%(version)s")
@click.option("-d", "--debug", is_flag=True, help="Show additional debug information.")
@click.option("--quiet", "-q", help="Print only serialized data", default=False, is_flag=True)
@click.option("--verbose", "-v", help="Be chatty", default=False, is_flag=True)
# @click.option("-?", "-h", "--help", is_flag=True, help="Show this message and exit.")
@click.pass_context
def cli(ctx, debug:bool = False, quiet:bool = False, verbose: bool = False):
    # named ctx.parent.gc3_cfg to other functions in cli group.
    # ctx.gc3_config = {}
    ctx.obj = OrderedDictAttrBase()
    ctx.obj['debug'] = debug
    ctx.obj['verbose'] = verbose
    ctx.obj['quiet'] = quiet
    ctx.obj['gc3_cfg'] = gc3_cfg
    if not quiet:
        click.echo(f"Running atoml.cli() with context: {ctx}")
    if debug:
        ctx.obj['logging_level'] = "debug"
        ctx.obj["gc3_cfg"]["logging"]["logging_level"] = "debug"
    else:
        ctx.obj['logging_level'] = "warning"
        ctx.obj["gc3_cfg"]["logging"]["logging_level"] = "warning"


@cli.command(help="Export to MongoDb", short_help="Export to MongoDb", epilog="MongoDb")
@click.pass_context
def mongodb(ctx: click.core.Context) -> None:
    if not ctx.obj.quiet:
        click.echo(click.style(f"atoml.print(): verbose={ctx.obj.verbose}, quiet={ctx.obj.quiet}", fg="green"))
    gc3_cfg = ctx.obj.gc3_cfg
    pprint(gc3_cfg._serializable)
    sys.exit(0)


@cli.command(help="Export to Excel", short_help="Export to Excel", epilog="Excel")
@click.pass_context
def excel(ctx: click.core.Context) -> None:
    if not ctx.obj.quiet:
        click.echo(click.style(f"atoml.print(): verbose={ctx.obj.verbose}, quiet={ctx.obj.quiet}", fg="green"))
    gc3_cfg = ctx.obj.gc3_cfg
    pprint(gc3_cfg._serializable)
    sys.exit(0)


@cli.command(help="Export to PolicyScanner", short_help="Export to PolicyScanner", epilog="PolicyScanner")
@click.pass_context
def policy_scanner(ctx: click.core.Context) -> None:
    if not ctx.obj.quiet:
        click.echo(click.style(f"atoml.print(): verbose={ctx.obj.verbose}, quiet={ctx.obj.quiet}", fg="green"))
    gc3_cfg = ctx.obj.gc3_cfg
    pprint(gc3_cfg._serializable)
    sys.exit(0)

if __name__=='__main__':
    cli()
