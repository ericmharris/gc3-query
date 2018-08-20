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
from gc3_query.lib import gc3_cfg
from gc3_query.lib.base_collections import OrderedDictAttrBase
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


# @click.group( invoke_without_command=False, context_settings=CONTEXT_SETTINGS, help=""" Help message for gc3keygen cli. """, )
# @click.version_option(__version__, "-v", "--version", message="%(version)s")
# @click.option("-d", "--debug", is_flag=True, help="Show additional debug information.")
# @click.option("-?", "-h", "--help", is_flag=True, help="Show this message and exit.")
# @click.pass_context
# def cli(ctx, debug, help):
#     # named ctx.parent.gc3cfg to other functions in cli group.
#     ctx.gc3_config = {}
#     click.echo(f"Running cli() with context: {ctx}")
#     if debug:
#         ctx.gc3_config["logging_level"] = "DEBUG"
#     else:
#         ctx.gc3_config["logging_level"] = "WARNING"



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
    command_line_options = dict(mongodb_bin_dir=mongodb_bin_dir,
                                listen_port=listen_port,
                                force=force )
    setup_mongo_db = SetupMongoDB(ctx=ctx, command_line_options=command_line_options)
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





@cli.command(help="Manage password for IDM domain", short_help="Keystore.", epilog="Manage keystore")
@click.option("--domain-name", "-d", help="IDM Domain name")
@click.option( "--password", "-p", prompt="Password for IDM Domain: ", help="Password for IDM Domain" )
@click.pass_context
def set_domain_passwords( ctx: click.core.Context, domain_name: str, password: str) -> None:
    # click.echo(click.style(f"atoml.print(): verbose={ctx.obj.verbose}, quiet={ctx.obj.quiet}", fg="green"))
    password = password.strip()
    click.echo(click.style(f"Setting IDM password, domain_name={domain_name}", fg="blue"))
    idm_credential = gc3_cfg.set_credential(idm_domain_name=domain_name, password=password)
    click.echo(click.style(f"IDM password for domain_name={idm_credential.idm_domain_name} set to: '{idm_credential.password}'", fg="green"))
    sys.exit(0)









if __name__=='__main__':
    cli()
