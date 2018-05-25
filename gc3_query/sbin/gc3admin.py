# -*- coding: utf-8 -*-

import sys
import click

from gc3_query import __version__
from gc3_query.lib.gc3admin.gc3admin import *
from gc3_query.lib.gc3admin.setup_mongodb import SetupMongoDB
from gc3_query.lib.gc3admin.setup_home_kitty import SetupHomeKitty

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
Help message for gc3query cli.
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


# @cli.command(help="Help for util_hello", short_help="Short help for util_hello", epilog="Epilog for util_hello")
# @click.option('--opt', '-o', help="Help for opt")
# @click.pass_context
# def test_gc3query_command(ctx: click.core.Context, opt: str) -> None:
#     click.echo(click.style(f'gc3admin.test_gc3query_command(): {opt}', fg='green'))
#     _info(f'Test logging for gc3query.')
#     print(f'context: {ctx}')
#     sys.exit(0)


@cli.command(help="Setup MongoDB.", short_help="Setup MongoDB.", epilog="Setup Mongo")
@click.option(
    "--mongodb-bin-dir",
    "-b",
    # prompt="Please enter full path to MongoDB bin directory",
    help="Directory containing mongodb executables, eg. mongod.exe",
)
@click.option("--listen-port", "-p", help="TCP port mongod should listen on.", default=7117)
@click.option("--force", "-f", help="Force, overwrite files if they exist.", default=False, is_flag=True)
@click.pass_context
def setup_mongodb(
    ctx: click.core.Context, mongodb_bin_dir: str = None, listen_port: int = 7117, force: bool = False
) -> None:
    click.echo(click.style(f"gc3admin.setup_mongodb(): target_dir={mongodb_bin_dir}", fg="green"))
    _warning(f"Test logging for gc3admin.")
    print(f"context: {ctx.parent.gc3_config}")
    setup_mongo_db = SetupMongoDB(ctx=ctx, mongodb_bin_dir=mongodb_bin_dir, listen_port=listen_port, force=force)
    sys.exit(0)


@cli.command(help="Setup Kitty.", short_help="Setup Kitty.", epilog="Setup Mongo")
@click.option(
    "--kitty-bin-dir",
    "-b",
    prompt="Please enter full path to Kitty bin directory",
    help="Directory containing kitty executables, eg. kittyd.exe",
)
@click.option("--listen-port", "-p", help="TCP port kittyd should listen on.", default=7117)
@click.option("--force", "-f", help="Force, overwrite files if they exist.", default=False, is_flag=True)
@click.pass_context
def setup_kitty(
    ctx: click.core.Context, kitty_bin_dir: str = None, listen_port: int = 7117, force: bool = False
) -> None:
    click.echo(click.style(f"gc3admin.setup_kitty(): target_dir={kitty_bin_dir}", fg="green"))
    _warning(f"Test logging for gc3admin.")
    print(f"context: {ctx.parent.gc3_config}")
    setup_kitty_db = SetupHomeKitty(ctx=ctx, kitty_bin_dir=kitty_bin_dir, listen_port=listen_port, force=force)

    sys.exit(0)




@cli.command(help="Setup Cookiecutter.", short_help="Setup Cookiecutter.", epilog="Setup Mongo")
@click.option(
    "--cookiecutter-bin-dir",
    "-b",
    prompt="Please enter full path to Cookiecutter bin directory",
    help="Directory containing cookiecutter executables, eg. cookiecutterd.exe",
)
@click.option("--listen-port", "-p", help="TCP port cookiecutterd should listen on.", default=7117)
@click.option("--force", "-f", help="Force, overwrite files if they exist.", default=False, is_flag=True)
@click.pass_context
def setup_cookiecutter(
    ctx: click.core.Context, cookiecutter_bin_dir: str = None, listen_port: int = 7117, force: bool = False
) -> None:
    click.echo(click.style(f"gc3admin.setup_cookiecutter(): target_dir={cookiecutter_bin_dir}", fg="green"))
    _warning(f"Test logging for gc3admin.")
    print(f"context: {ctx.parent.gc3_config}")
    setup_cookiecutter_db = SetupHomeCookiecutter(ctx=ctx, cookiecutter_bin_dir=cookiecutter_bin_dir, listen_port=listen_port, force=force)

    sys.exit(0)
