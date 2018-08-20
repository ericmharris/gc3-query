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
import json
import subprocess
from pprint import pprint, pformat
from distutils.spawn import find_executable


################################################################################
## Third-Party Imports
from dataclasses import dataclass
import click
# from prettyprinter import prettyprinter, pprint

################################################################################
## Project Imports
from gc3_query.lib import gc3_cfg
from gc3_query import BASE_DIR
from gc3_query.lib import *
from gc3_query.lib.gc3logging import get_logging
from gc3_query.lib.atoml.atoml_config import ATomlConfig
from gc3_query.lib import gc3_cfg
from gc3_query.lib.base_collections import OrderedDictAttrBase

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


@cli.command(help="Print TOML to stdout", short_help="ATOML CLI", epilog="ATOML CLI")
@click.pass_context
def print(ctx: click.core.Context) -> None:
    if not ctx.obj.quiet:
        click.echo(click.style(f"atoml.print(): verbose={ctx.obj.verbose}, quiet={ctx.obj.quiet}", fg="green"))
    gc3_cfg = ctx.obj.gc3_cfg
    pprint(gc3_cfg._serializable)
    sys.exit(0)


@cli.command(help="Export TOML to var/config_data.py", short_help="ATOML export ", epilog="export ATOML ")
@click.option("--editor", "-e", help="Open exported file using the first hit found in user.windows_editors/or linux_editors",
              default=False, is_flag=True)
@click.pass_context
def export(ctx: click.core.Context, editor: bool = False) -> None:
    gc3_cfg = ctx.obj.gc3_cfg
    output_file = BASE_DIR.joinpath('var/config/config_data.py')
    with output_file.open('w') as fd:
        fd.write(pformat(gc3_cfg._serializable))
    click.echo(click.style(f"Config data written to {output_file}", fg="green"))
    if editor:
        found_editor = False
        if sys.platform.startswith('win'):
            editors = gc3_cfg.user.windows_editors
        else:
            editors = gc3_cfg.user.linux_editors
        editors_found = [find_executable(e) for e in editors]
        _debug(f"editors={editors}, editors_found={editors_found}")
        for editor in editors_found:
            if editor:
                args = f"{editor} {output_file}".split()
                click.echo(click.style(f"Opening: {editor} {output_file}", fg="green"))
                # subprocess.run(args=args, check=False)
                subprocess.Popen(args=args)
                break
    sys.exit(0)



if __name__=='__main__':
    cli()
