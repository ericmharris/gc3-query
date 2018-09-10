from pathlib import Path

from gc3_query.lib import gc3_cfg
# from gc3_query.lib.iaas_classic.models import IaaSServiceModelDynamicDocument
# fixme? from gc3_query.lib.open_api import API_SPECS_DIR

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


# def test_init():
#     model_base = IaaSServiceModelDynamicDocument()
#     assert model_base.connection_config
#     assert 'port' in model_base.connection_config





