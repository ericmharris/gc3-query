from pathlib import Path
# from pprint import pprint, pformat

from pathlib import Path

from gc3_query import BASE_DIR
from gc3_query.lib.iaas_classic.iaas_swagger_client import BRAVADO_CLIENT_CONFIG, BRAVADO_CORE_CONFIG, BRAVADO_CONFIG
from gc3_query.lib.open_api import API_SPECS_DIR

# from pprint import pprint, pformat

TEST_BASE_DIR: Path = Path(__file__).parent
# config_dir = TEST_BASE_DIR.joinpath("config")
config_dir = BASE_DIR.joinpath("etc/config")
output_dir = TEST_BASE_DIR.joinpath('output')


def test_setup():
    assert TEST_BASE_DIR.exists()
    assert API_SPECS_DIR.exists()
    if not config_dir.exists():
        config_dir.mkdir()
    if not output_dir.exists():
        output_dir.mkdir()


def test_bravado_client_and_core_config():
    bravado_client_config = BRAVADO_CLIENT_CONFIG
    bravado_core_config = BRAVADO_CORE_CONFIG
    bravado_config = BRAVADO_CONFIG
    assert BRAVADO_CLIENT_CONFIG
    assert BRAVADO_CORE_CONFIG
    assert BRAVADO_CONFIG
    assert 'include_missing_properties' in BRAVADO_CORE_CONFIG
    assert not 'include_missing_properties' in BRAVADO_CLIENT_CONFIG
    assert 'include_missing_properties' in BRAVADO_CONFIG

    assert not 'also_return_response' in BRAVADO_CORE_CONFIG
    assert 'also_return_response' in BRAVADO_CLIENT_CONFIG
    assert 'also_return_response' in BRAVADO_CONFIG

    assert isinstance(BRAVADO_CLIENT_CONFIG, dict)
    assert isinstance(BRAVADO_CORE_CONFIG, dict)
    assert isinstance(BRAVADO_CONFIG, dict)


