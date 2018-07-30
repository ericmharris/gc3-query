import pytest
import toml
from pathlib import Path

from gc3_query.lib import *

from gc3_query.lib.gc3_config import GC3Config, IDMCredential

TEST_BASE_DIR: Path = Path(__file__).parent.joinpath("GC3Config")


def test_init():
    config_dir = TEST_BASE_DIR.joinpath("config")
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    assert 'gc30003' in gc3_config['idm_domains']
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'


def test_set_credential():
    config_dir = TEST_BASE_DIR.joinpath("config")
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    assert 'gc3test' in gc3_config['idm_domains']
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    credential = gc3_config.set_credential(idm_domain_name='gc3test', password='Welcome123' )
    assert credential
    assert credential.password == 'Welcome123'
    assert credential.idm_domain_name == 'gc3test'




@pytest.fixture()
def get_credential_setup() -> IDMCredential:
    config_dir = TEST_BASE_DIR.joinpath("config")
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    assert 'gc3test' in gc3_config['idm_domains']
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    credential = gc3_config.set_credential(idm_domain_name='gc3test', password='123Welcome' )
    yield (credential)


def test_load_atoml_files_individually(get_credential_setup):
    credential = get_credential_setup
    config_dir = TEST_BASE_DIR.joinpath("config")
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    assert 'gc3test' in gc3_config['idm_domains']
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    check_credential = gc3_config.get_credential(idm_domain_name='gc3test')
    assert check_credential==credential
