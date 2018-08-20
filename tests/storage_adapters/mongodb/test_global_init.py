from pathlib import Path

from gc3_query.lib.export_delegates.mongodb import storage_adapter_init
from gc3_query.lib.open_api import API_SPECS_DIR

TEST_BASE_DIR: Path = Path(__file__).parent
# config_dir = TEST_BASE_DIR.joinpath("config")
config_dir = BASE_DIR.joinpath("etc/config")


def test_setup():
    assert TEST_BASE_DIR.exists()
    assert config_dir.exists()
    assert API_SPECS_DIR.exists()




def test_global_init():
    connection_registered = storage_adapter_init()
    assert connection_registered
    assert 'port' in connection_registered

