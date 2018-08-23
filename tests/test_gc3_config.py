from pathlib import Path

import pytest

from gc3_query.lib.gc3_config import GC3Config, IDMCredential

TEST_BASE_DIR: Path = Path(__file__).parent.joinpath("GC3Config")
config_dir = TEST_BASE_DIR.joinpath("config")

def test_setup():
    assert TEST_BASE_DIR.exists()
    assert config_dir.exists()

def test_init():
    gc3_config = GC3Config()
    assert 'gc30003' in gc3_config['idm']['domains']
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'


def test_set_credential():
    gc3_config = GC3Config()
    assert 'gc3test' in gc3_config['idm']['domains']
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    credential = gc3_config.set_credential(idm_domain_name='gc3test', password='Welcome123' )
    assert credential
    assert credential.password == 'Welcome123'
    assert credential.idm_domain_name == 'gc3test'




@pytest.fixture()
def get_credential_setup() -> IDMCredential:
    gc3_config = GC3Config()
    assert 'gc3test' in gc3_config['idm']['domains']
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    credential = gc3_config.set_credential(idm_domain_name='gc3test', password='123Welcome' )
    yield (credential)


def test_load_atoml_files_individually(get_credential_setup):
    credential = get_credential_setup
    gc3_config = GC3Config()
    assert 'gc3test' in gc3_config['idm']['domains']
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    check_credential = gc3_config.get_credential(idm_domain_name='gc3test')
    assert check_credential==credential


def test_get_main_credential():
    gc3_config = GC3Config()
    check_credential = gc3_config.get_credential(idm_domain_name='gc30003')
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    assert check_credential.idm_domain_name=='gc30003'


@pytest.fixture()
def get_bravado_config_setup():
    gc3_config = GC3Config()
    assert 'iaas_classic' in gc3_config
    yield (gc3_config)

def test_bravado_client_config(get_bravado_config_setup):
    gc3_config = get_bravado_config_setup
    assert 'iaas_classic' in gc3_config
    bravado_client_config = gc3_config.bravado_client_config
    assert bravado_client_config
    assert 'formats' not in bravado_client_config
    assert not 'include_missing_properties' in bravado_client_config
    assert 'also_return_response' in bravado_client_config
    bravado_client_config_2 = gc3_config.bravado_client_config
    assert bravado_client_config==bravado_client_config_2
    assert bravado_client_config is not bravado_client_config_2
    assert isinstance(bravado_client_config, dict)

def test_bravado_core_config(get_bravado_config_setup):
    gc3_config = get_bravado_config_setup
    assert 'iaas_classic' in gc3_config
    bravado_core_config = gc3_config.bravado_core_config
    assert bravado_core_config
    assert 'formats' in bravado_core_config
    assert 'include_missing_properties' in bravado_core_config
    assert not 'also_return_response' in bravado_core_config
    bravado_core_config_2 = gc3_config.bravado_core_config
    assert bravado_core_config==bravado_core_config_2
    assert bravado_core_config is not bravado_core_config_2
    assert isinstance(bravado_core_config, dict)
    assert isinstance(bravado_core_config['formats'], list)

    

def test_bravado_config(get_bravado_config_setup):
    gc3_config = get_bravado_config_setup
    assert 'iaas_classic' in gc3_config
    bravado_config = gc3_config.bravado_config
    assert bravado_config
    assert 'formats' in bravado_config
    assert 'include_missing_properties' in bravado_config
    assert 'also_return_response' in bravado_config
    bravado_config_2 = gc3_config.bravado_config
    assert bravado_config==bravado_config_2
    assert bravado_config is not bravado_config_2
    assert isinstance(bravado_config, dict)
    assert isinstance(bravado_config['formats'], list)


@pytest.fixture()
def get_constants_setup():
    gc3_config = GC3Config()
    assert 'iaas_classic' in gc3_config
    yield (gc3_config)

def test_open_api_catalog_dir(get_constants_setup):
    gc3_config = get_constants_setup
    open_api_catalog_dir = gc3_config.OPEN_API_CATALOG_DIR
    assert open_api_catalog_dir

def test_BRAVADO_CONFIG(get_constants_setup):
    gc3_config = get_constants_setup
    bravado_config = gc3_config.BRAVADO_CONFIG
    assert bravado_config
    assert 'formats' in bravado_config
    assert 'include_missing_properties' in bravado_config
    assert 'also_return_response' in bravado_config
    bravado_config_2 = gc3_config.bravado_config
    assert bravado_config==bravado_config_2
    assert bravado_config is not bravado_config_2
    assert isinstance(bravado_config, dict)
    assert isinstance(bravado_config['formats'], list)
