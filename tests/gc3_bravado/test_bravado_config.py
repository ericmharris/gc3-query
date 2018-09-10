from pathlib import Path
from requests.auth import _basic_auth_str

import pytest
from bravado_core.formatter import SwaggerFormat, NO_OP
from gc3_query.lib import gc3_cfg
from gc3_query.lib.gc3_config import GC3Config, IDMCredential
from gc3_query.lib.gc3_bravado.bravado_config import BravadoConfig

TEST_BASE_DIR: Path = Path(__file__).parent
# config_dir = TEST_BASE_DIR.joinpath("config")
config_dir = gc3_cfg.BASE_DIR.joinpath("etc/config")
output_dir = TEST_BASE_DIR.joinpath('output')

def test_setup():
    assert TEST_BASE_DIR.exists()
    # assert API_SPECS_DIR.exists()
    if not config_dir.exists():
        config_dir.mkdir()
    if not output_dir.exists():
        output_dir.mkdir()


def test_init():
    gc3_config = GC3Config()
    bravado_config = BravadoConfig()
    assert 'gc30003' in gc3_config['idm']['domains']
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    assert bravado_config





@pytest.fixture()
def get_bravado_config_setup():
    gc3_config = GC3Config()
    bravado_config = BravadoConfig()
    assert 'iaas_classic' in gc3_config
    yield gc3_config, bravado_config

def test_bravado_client_config(get_bravado_config_setup):
    gc3_config, bravado_config = get_bravado_config_setup
    assert 'iaas_classic' in gc3_config
    bravado_client_config = bravado_config.bravado_client_config
    assert bravado_client_config
    assert 'formats' not in bravado_client_config
    assert not 'include_missing_properties' in bravado_client_config
    assert 'also_return_response' in bravado_client_config
    bravado_client_config_2 = bravado_config.bravado_client_config
    assert bravado_client_config==bravado_client_config_2
    assert bravado_client_config is not bravado_client_config_2
    assert isinstance(bravado_client_config, dict)

def test_bravado_core_config(get_bravado_config_setup):
    gc3_config, bravado_config = get_bravado_config_setup
    assert 'iaas_classic' in gc3_config
    bravado_core_config = bravado_config.bravado_core_config
    assert bravado_core_config
    assert 'formats' in bravado_core_config
    assert 'include_missing_properties' in bravado_core_config
    assert not 'also_return_response' in bravado_core_config
    bravado_core_config_2 = bravado_config.bravado_core_config
    assert bravado_core_config==bravado_core_config_2
    assert bravado_core_config is not bravado_core_config_2
    assert isinstance(bravado_core_config, dict)
    assert isinstance(bravado_core_config['formats'], list)

    

def test_bravado_config(get_bravado_config_setup):
    gc3_config, bravado_config = get_bravado_config_setup
    assert 'iaas_classic' in gc3_config
    bravado_config = bravado_config.bravado_config
    assert bravado_config
    assert 'formats' in bravado_config
    assert 'include_missing_properties' in bravado_config
    assert 'also_return_response' in bravado_config
    # bravado_config_2 = bravado_config.bravado_config
    # assert bravado_config==bravado_config_2
    # assert bravado_config is not bravado_config_2
    # assert isinstance(bravado_config, dict)
    # assert isinstance(bravado_config['formats'], list)



