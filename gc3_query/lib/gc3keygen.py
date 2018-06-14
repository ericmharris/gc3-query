# -*- coding: utf-8 -*-

"""
#@Filename : gc3keygen
#@Date : [6/14/2018 11:38 AM]
#@Poject: gc3-query
#@AUTHOR : eharris

~~~~~~~~~~~~~~~~

<DESCR SHORT>

<DESCR>
"""

################################################################################
## Standard Library Imports
import sys, os

################################################################################
## Third-Party Imports
import click
from dataclasses import dataclass

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

################################################################################
## Project Imports
from gc3_query import __version__
from gc3_query.lib import *

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
Help message for gc3keygen cli.
""",
)
@click.version_option(__version__, "-v", "--version", message="%(version)s")
@click.option("-d", "--debug", is_flag=True, help="Show additional debug information.")
@click.option("-?", "-h", "--help", is_flag=True, help="Show this message and exit.")
@click.pass_context
def cli(ctx, debug, help):
    # named ctx.parent.gc3_config to other functions in cli group.
    ctx.gc3_config = {}
    click.echo(f"Running cli() with context: {ctx}")
    if debug:
        ctx.gc3_config["logging_level"] = "DEBUG"
    else:
        ctx.gc3_config["logging_level"] = "WARNING"


@cli.command(help="Create SSH keys for new project", short_help="Create SSH keys.", epilog="Create SSH keys.")
@click.option("--region", "-r", help="Region, eg. NAAC, ", default=7117)
@click.option("--force", "-f", help="Force, overwrite files if they exist.", default=False, is_flag=True)
@click.pass_context
def create_project_ssh_keys(ctx: click.core.Context, region: str, project_code: str = False) -> None:
    click.echo(click.style(f"gc3admin.setup_mongodb(): target_dir={mongodb_bin_dir}", fg="green"))
    _warning(f"Test logging for gc3admin.")
    print(f"context: {ctx.parent.gc3_config}")
    sys.exit(0)
