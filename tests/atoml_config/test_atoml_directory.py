
import pytest
import toml
from pathlib import Path

from gc3_query.lib import *
from gc3_query.lib.atoml_cfg.exceptions import *
from gc3_query.lib.atoml_cfg.atoml_file import ATomlFile
from gc3_query.lib.atoml_cfg.atoml_directory import ATomlDirectory
from gc3_query.lib.atoml_cfg.atoml_config import ATomlConfig

from gc3_query.lib.models.gc3_meta_data import GC3MetaData

TEST_BASE_DIR: Path = Path(__file__).parent.joinpath("ATomlDirectory")


def test_test_base_dir():
    assert TEST_BASE_DIR.exists()

def test_load_atoml_files():
    test_dir = TEST_BASE_DIR.joinpath("load_atoml_files")
    assert test_dir.exists()
    atd = ATomlDirectory(directory_path=test_dir)
    assert len(atd.atoml_files) == 4




@pytest.fixture()
def load_atoml_files_from_directory_setup() -> List[str]:
    config_dir: Path = TEST_BASE_DIR.joinpath("load_atoml_files_from_directories")
    assert config_dir.exists()

    def run_data_tests(atd):
        assert len(atd.atoml_files) > 1
        # assert 'ASDF' in atd.toml
        assert 'title' in atd.toml
        assert '__init__' in atd.toml

        assert 'user' in atd.toml
        assert '_meta' in atd.toml['user']

        assert 'mongodb' in atd.toml
        assert 'storage' in atd.toml['mongodb']
        assert 'db_path' in atd.toml['mongodb']['storage']

        assert 'idm_domains' in atd.toml
        assert 'gc3pilot' in atd.toml['idm_domains']
        assert 'rest_url' in atd.toml['idm_domains']['gc3pilot']

        assert 'valid_toml' in atd.toml
        assert 'valid_toml_quoted' in atd.toml
        return True

    yield config_dir, run_data_tests



def test_load_atoml_files_from_flat_dir(load_atoml_files_from_directory_setup):
    config_dir, run_data_tests = load_atoml_files_from_directory_setup
    test_dir = config_dir.joinpath('flat')
    assert test_dir.exists()
    atd = ATomlConfig(directory_path=test_dir)
    test_result = run_data_tests(atd)
    assert test_result



def test_load_atoml_files_from_one_deep_dir(load_atoml_files_from_directory_setup):
    config_dir, test_data = load_atoml_files_from_directory_setup
    test_dir = config_dir.joinpath('one_deep')
    assert test_dir.exists()
    atd = ATomlConfig(directory_path=test_dir)
    test_result = test_data(atd)
    assert test_result
#
#
# def test_load_atoml_files_from_nest_dir(load_atoml_files_from_directory_setup):
#     config_dir, test_data = load_atoml_files_from_directory_setup
#     test_dir = config_dir.joinpath('nested')
#     assert test_dir.exists()
#     atd = ATomlConfig(atoml_dir_path=test_dir)
#     test_result = test_data(atd)
#     assert test_result


