# -*- coding: utf-8 -*-

"""
#@Filename : atoml
#@Date : [6/17/2018 8:46 AM]
#@Poject: gc3-query
#@AUTHOR : eharris

~~~~~~~~~~~~~~~~

<DESCR SHORT>

<DESCR>
"""

################################################################################
## Standard Library Imports
import sys, os
# from pprint import pprint

################################################################################
## Third-Party Imports
from dataclasses import dataclass
import click
from prettyprinter import prettyprinter, pprint

################################################################################
## Project Imports
from gc3_query import GC3_QUERY_HOME
from gc3_query.lib import *
from gc3_query.lib.gc3logging import get_logging
from gc3_query.lib.atoml.atoml_config import ATomlConfig
from gc3_query.lib import gc3_cfg

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
    help="""
Help message for atoml cli.
""",
)
@click.version_option('0.1.0', "-v", "--version", message="%(version)s")
@click.option("-d", "--debug", is_flag=True, help="Show additional debug information.")
@click.option("-?", "-h", "--help", is_flag=True, help="Show this message and exit.")
@click.pass_context
def cli(ctx, debug, help):
    # named ctx.parent.gc3_cfg to other functions in cli group.
    # ctx.gc3_config = {}
    ctx.gc3_cfg = gc3_cfg
    click.echo(f"Running atoml.cli() with context: {ctx}, ctx.gc3_cfg={gc3_cfg}")
    if debug:
        ctx.gc3_cfg["logging"]["logging_level"] = "debug"
    else:
        ctx.gc3_cfg["logging"]["logging_level"] = "warning"


@cli.command(help="Annotated TOML CLI", short_help="ATOML CLI", epilog="ATOML CLI")
@click.option("--verbose", "-v", help="Be chatty", default=False, is_flag=True)
@click.pass_context
def print(ctx: click.core.Context, verbose: bool = False) -> None:
    click.echo(click.style(f"atoml.print(): verbose={verbose}", fg="green"))
    gc3_cfg = ctx.parent.gc3_cfg
    pprint(gc3_cfg)
    sys.exit(0)




if __name__=='__main__':
    cli()
