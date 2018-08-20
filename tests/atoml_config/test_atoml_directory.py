from pathlib import Path

import pytest

from gc3_query.lib.atoml.atoml_config import ATomlDirectory

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

    # def run_data_tests(atd):
    #     assert len(atd.atoml_files) > 1
    #     # assert 'ASDF' in atd._toml
    #     # assert 'title' in atd._toml
    #     # assert '__init__' in atd._toml
    #
    #     assert 'user' in atd._toml
    #     assert '_meta' in atd._toml['user']
    #
    #     assert 'mongodb' in atd._toml
    #     assert 'storage' in atd._toml['mongodb']
    #     assert 'db_path' in atd._toml['mongodb']['storage']
    #
    #     assert 'idm_domains'in atd._toml
    #     assert 'gc3pilot' in atd._toml['idm_domains']
    #     assert 'rest_url' in atd._toml['idm_domains']['gc3pilot']
    #
    #     assert 'valid_toml' in atd._toml
    #     assert 'valid_toml_quoted' in atd._toml
    #     return True

    yield config_dir


def test_load_atoml_files_from_flat_dir(load_atoml_files_from_directory_setup):
    config_dir = load_atoml_files_from_directory_setup
    test_dir = config_dir.joinpath('flat')
    assert test_dir.exists()
    atd = ATomlDirectory(directory_path=test_dir)
    assert 'user' in atd._toml
    assert '_meta' in atd._toml['user']

    assert 'mongodb' in atd._toml
    assert 'storage' in atd._toml['mongodb']
    assert 'db_path' in atd._toml['mongodb']['storage']

    assert 'idm_domains' in atd._toml
    assert 'gc3pilot' in atd._toml['idm_domains']
    assert 'rest_url' in atd._toml['idm_domains']['gc3pilot']

    assert 'valid_toml' in atd._toml
    assert 'valid_toml_quoted' in atd._toml

    assert len(atd.atoml_directories) == 0


def test_load_atoml_files_from_one_deep_dir(load_atoml_files_from_directory_setup):
    config_dir = load_atoml_files_from_directory_setup
    test_dir = config_dir.joinpath('one_deep')
    assert test_dir.exists()
    atd = ATomlDirectory(directory_path=test_dir)

    assert 'user' in atd._toml
    assert '_meta' in atd._toml['user']

    assert 'valid_toml' in atd._toml
    assert 'valid_toml_quoted' in atd._toml

    assert len(atd.atoml_directories) == 2


def test_load_atoml_files_from_nested_dir_01(load_atoml_files_from_directory_setup):
    config_dir = load_atoml_files_from_directory_setup
    test_dir = config_dir.joinpath('nested_01')
    assert test_dir.exists()
    atd = ATomlDirectory(directory_path=test_dir)

    assert 'user' in atd._toml
    assert '_meta' in atd._toml['user']

    assert len(atd.atoml_directories) == 1

    catd = atd.atoml_directories[0]
    assert 'mongodb' in catd._toml
    assert 'storage' in catd._toml['mongodb']
    assert 'db_path' in catd._toml['mongodb']['storage']


def test_load_atoml_files_from_nested_dir_02(load_atoml_files_from_directory_setup):
    config_dir = load_atoml_files_from_directory_setup
    test_dir = config_dir.joinpath('nested_02')
    assert test_dir.exists()
    atd = ATomlDirectory(directory_path=test_dir)

    assert 'user' in atd._toml
    assert 'idm_domains' in atd._toml
    assert 'gc30003' in atd._toml['idm_domains']
    assert 'gc3pilot' in atd._toml['idm_domains']
    assert 'sites' in atd._toml['idm_domains']['gc3pilot']
    assert 'us006_z70' in atd._toml['idm_domains']['gc3pilot']['sites']

    assert 'mongodb' in atd._toml
    assert 'net' in atd._toml['mongodb']
    assert 'listen_port' in atd._toml['mongodb']['net']
    assert atd._toml['mongodb']['net']['listen_port'] == 7117


def test_load_atoml_files_from_nested_dir_03(load_atoml_files_from_directory_setup):
    config_dir = load_atoml_files_from_directory_setup
    test_dir = config_dir.joinpath('nested_03')
    assert test_dir.exists()
    atd = ATomlDirectory(directory_path=test_dir)

    assert 'user' in atd._toml
    assert 'idm_domains' in atd._toml
    assert 'gc30003' in atd._toml['idm_domains']
    assert 'gc3pilot' in atd._toml['idm_domains']
    assert 'sites' in atd._toml['idm_domains']['gc3pilot']
    assert 'us006_z70' in atd._toml['idm_domains']['gc3pilot']['sites']

    assert 'mongodb' in atd._toml
    assert 'net' in atd._toml['mongodb']
    assert 'listen_port' in atd._toml['mongodb']['net']
    assert atd._toml['mongodb']['net']['listen_port'] == 7117
