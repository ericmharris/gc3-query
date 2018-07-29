# -*- coding: utf-8 -*-

"""
#@Filename : gc3admin
#@Date : [7/27/2018 9:06 AM]
#@Poject: gc3-query
#@AUTHOR : emharris

~~~~~~~~~~~~~~~~

<DESCR SHORT>

<DESCR>
"""

################################################################################
## Standard Library Imports
import sys

################################################################################
## Third-Party Imports
import click

################################################################################
## Project Imports
from gc3_query import __version__
from gc3_query.lib import *
from gc3_query.lib.cookie_cutter.setup_mongodb import SetupMongoDB

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


CONTEXT_SETTINGS = dict(
    help_option_names=[
        "-h",
        "--help",
        "-?",
    ],  # help_option_names sets tokens that come after a command that'll trigger help.
    ignore_unknown_options=True,
)


@click.group( invoke_without_command=False, context_settings=CONTEXT_SETTINGS, help=""" Help message for gc3keygen cli. """, )
@click.version_option(__version__, "-v", "--version", message="%(version)s")
@click.option("-d", "--debug", is_flag=True, help="Show additional debug information.")
@click.option("-?", "-h", "--help", is_flag=True, help="Show this message and exit.")
@click.pass_context
def cli(ctx, debug, help):
    # named ctx.parent.gc3cfg to other functions in cli group.
    ctx.gc3_config = {}
    click.echo(f"Running cli() with context: {ctx}")
    if debug:
        ctx.gc3_config["logging_level"] = "DEBUG"
    else:
        ctx.gc3_config["logging_level"] = "WARNING"


@cli.command(help="Setup MongoDB.", short_help="Setup MongoDB.", epilog="Setup Mongo")
@click.option( "--mongodb-bin-dir", "-b",
    # prompt="Please enter full file_path to MongoDB bin directory",
    help="Directory containing mongodb executables, eg. mongod.exe", )
@click.option("--listen-port", "-p", help="TCP port mongod should listen on.", default=7117)
@click.option("--force", "-f", help="Force, overwrite files if they exist.", default=False, is_flag=True)
@click.pass_context
def setup_mongodb( ctx: click.core.Context, mongodb_bin_dir: str = None, listen_port: int = 7117, force: bool = False ) -> None:
    click.echo(click.style(f"gc3admin.setup_mongodb(): target_dir={mongodb_bin_dir}", fg="green"))
    _warning(f"Test logging for gc3admin.")
    print(f"context: {ctx.parent.gc3_config}")
    setup_mongo_db = SetupMongoDB(ctx=ctx, mongodb_bin_dir=mongodb_bin_dir, listen_port=listen_port, force=force)
    ret_code = setup_mongo_db.deploy()
    if ret_code:
        click.echo(click.style(f"""MongoDB configuration succeeded 
        config_dir={setup_mongo_db.user_inputs['mongodb_setup_dir']} 
        using MongoDB={setup_mongo_db.user_inputs['mongod_bin']}""", fg="green"))
        sys.exit(0)
    else:
        click.echo(click.style(f"""MongoDB configuration FAILED!
        config_dir={setup_mongo_db.user_inputs['mongodb_setup_dir']} 
        using MongoDB={setup_mongo_db.user_inputs['mongod_bin']}""", fg="red"))
        sys.exit(1)





@cli.command(help="Manage credentials in OS keystore", short_help="Keystore.", epilog="Manage keystore")
@click.option( "--password",
               "-p",
               prompt="Please enter full file_path to MongoDB bin directory",
               help="Directory containing mongodb executables, eg. mongod.exe", )
@click.option("--listen-port", "-p", help="TCP port mongod should listen on.", default=7117)
@click.option("--force", "-f", help="Force, overwrite files if they exist.", default=False, is_flag=True)
@click.pass_context
def set_domain_passwords( ctx: click.core.Context, mongodb_bin_dir: str = None, listen_port: int = 7117, force: bool = False ) -> None:
    click.echo(click.style(f"gc3admin.setup_mongodb(): target_dir={mongodb_bin_dir}", fg="green"))
    _warning(f"Test logging for gc3admin.")
    print(f"context: {ctx.parent.gc3_config}")
    setup_mongo_db = SetupMongoDB(ctx=ctx, mongodb_bin_dir=mongodb_bin_dir, listen_port=listen_port, force=force)
    ret_code = setup_mongo_db.deploy()
    if ret_code:
        click.echo(click.style(f"""MongoDB configuration succeeded 
        config_dir={setup_mongo_db.user_inputs['mongodb_setup_dir']} 
        using MongoDB={setup_mongo_db.user_inputs['mongod_bin']}""", fg="green"))
        sys.exit(0)
    else:
        click.echo(click.style(f"""MongoDB configuration FAILED!
        config_dir={setup_mongo_db.user_inputs['mongodb_setup_dir']} 
        using MongoDB={setup_mongo_db.user_inputs['mongod_bin']}""", fg="red"))
        sys.exit(1)









if __name__=='__main__':
    cli()
