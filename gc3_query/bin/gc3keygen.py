# -*- coding: utf-8 -*-

"""
#@Filename : gc3keygen
#@Date : [6/14/2018 11:37 AM]
#@Poject: gc3-query
#@AUTHOR : eharris

~~~~~~~~~~~~~~~~

<DESCR SHORT>

<DESCR>
"""


################################################################################
## Standard Library Imports

################################################################################
## Third-Party Imports

################################################################################
## Project Imports
from gc3_query import __version__
from gc3_query.lib.gc3keygen import *

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
    help="""
Help message for gc3keygen cli.
""",
)
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


@cli.command(help="Create SSH keys for new project", short_help="Create SSH keys.", epilog="Create SSH keys.")
@click.option("--region", "-r", required=True, help="Region, eg. NAAC, EMEA, APAC", type=click.Choice(['apac', 'dvtest', 'emea', 'gc3h',
                                                                                                       'japn', 'naac', 'ntag', 'ntsb',
                                                                                                       'ossi', 'sshitest', 'uasg']))
@click.option("--project-code", "-c", required=True, help="Project ID, eg. CDMT", type=str)
@click.option("--password", "-p", required=True, help="Password for the key.", prompt=True, hide_input=True, confirmation_prompt=True, type=str)
@click.option("--key-size", "-b", required=True, help="Bit", type=click.Choice([1024, 2048, 4096]), default=4096)
@click.option("--force", "-f", help="Force, overwrite existing key files if they exist.", default=False, is_flag=True)
@click.pass_context
def create_project_ssh_keys(ctx: click.core.Context, region: str, project_code: str, password: str, key_size: int = 4096, force: bool = False) -> None:
    click.echo(click.style(f"gc3keygen.create_project_ssh_keys(): region={region}, project_id={project_code}, password={password}, key_size={key_size}", fg="green"))
    print(f"context: {ctx.parent.gc3cfg}")

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size, backend=default_backend())
    public_key = private_key.public_key()
    private_key_pem = private_key.private_bytes(
                                                encoding=serialization.Encoding.PEM,
                                                # encoding=serialization.Encoding.OpenSSH,
                                                # format=serialization.PrivateFormat.PKCS8,
                                                format=serialization.PrivateFormat.TraditionalOpenSSL,
                                                encryption_algorithm=serialization.BestAvailableEncryption(password.encode()))
    public_key_pem = public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)

    private_key_path = Path(f"{region}_{project_code}.rsa").resolve()
    public_key_path = Path(f"{region}_{project_code}.pub").resolve()
    if private_key_path.exists() and not force:
        _error(f"Exiting, private key file already exists and --force={force}: {private_key_path}")
        sys.exit(1)
    if public_key_path.exists() and not force:
        _error(f"Exiting, public key file already exists and --force={force}: {public_key_path}")
        sys.exit(1)

    with private_key_path.open('wb') as fd:
        fd.write(private_key_pem)
        click.echo(click.style(f"Private key written to: {str(private_key_path)}", fg="green"))
    with public_key_path.open('wb') as fd:
        fd.write(public_key_pem)
        click.echo(click.style(f"Public key written to: {str(public_key_path)}", fg="green"))

    sys.exit(0)


if __name__=='__main__':
    cli()
