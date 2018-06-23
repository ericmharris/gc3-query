import pytest
import toml
from pathlib import Path

from gc3_query.lib import *
from gc3_query.lib.atoml_cfg.exceptions import *
from gc3_query.lib.atoml_cfg.atoml_file import ATomlFile
from gc3_query.lib.atoml_cfg.atoml_config import ATomlConfig

from gc3_query.lib.models.gc3_meta_data import GC3MetaData

TEST_BASE_DIR: Path = Path(__file__).parent.joinpath("ATomlConfig")


def test_no_input_throws_error():
    with pytest.raises(ATomlConfigError) as e:
        atc = ATomlConfig(file_paths=None, directory_path=None)


def test_load_atoml_settings_file_present():
    config_dir = TEST_BASE_DIR.joinpath("load_atoml_settings_file/present")
    atoml_settings_file = config_dir.joinpath('__init__.toml')
    atc = ATomlConfig(directory_path=config_dir)
    assert config_dir.exists()
    assert atoml_settings_file.exists()
    assert atc._atoml_settings_file.file_path == atoml_settings_file


def test_load_atoml_settings_file_absent():
    config_dir = TEST_BASE_DIR.joinpath("load_atoml_settings_file/absent")
    atoml_settings_file = config_dir.joinpath('__init__.toml')
    atc = ATomlConfig(directory_path=config_dir)
    assert config_dir.exists()
    assert not atoml_settings_file.exists()
    assert atc._atoml_settings_file == None


@pytest.fixture()
def load_atoml_files_individually_setup() -> List[str]:
    config_dir = TEST_BASE_DIR.joinpath("load_atoml_files/test_load_atoml_files_individually")
    assert config_dir.exists()
    yield (config_dir)


def test_load_atoml_files_individually(load_atoml_files_individually_setup):
    config_dir = load_atoml_files_individually_setup
    at_files = config_dir.glob('*.toml')
    atc = ATomlConfig(file_paths=at_files)
    assert len(atc.atoml_files) > 1
    assert 'title' in atc.toml
    assert 'rest_url' in atc.toml['idm_domains']['gc3pilot']


def test_file_names(load_atoml_files_individually_setup):
    config_dir = load_atoml_files_individually_setup
    at_files = config_dir.glob('*.toml')
    atc = ATomlConfig(file_paths=at_files)
    assert '__init__.toml' in atc.file_names
    assert 'user_info.toml' in atc.file_names


@pytest.fixture()
def load_atoml_files_from_directory_setup() -> List[str]:
    config_dir: Path = TEST_BASE_DIR.joinpath("load_atoml_files/test_load_atoml_files_from_directories")
    assert config_dir.exists()

    def test_data(atc):
        assert 'title' in atc.toml
        assert '__init__' in atc.toml

        assert 'user' in atc.toml
        assert '_meta' in atc.toml['user']

        assert 'mongodb' in atc.toml
        assert 'storage' in atc.toml['mongodb']
        assert 'db_path' in atc.toml['mongodb']['storage']

        assert 'idm_domains' in atc.toml
        assert 'gc3pilot' in atc.toml['idm_domains']
        assert 'rest_url' in atc.toml['idm_domains']['gc3pilot']

        assert 'valid_toml' in atc.toml
        assert 'valid_toml_quoted' in atc.toml
        return True

    yield config_dir, test_data


def test_load_atoml_files_from_flat_dir(load_atoml_files_from_directory_setup):
    config_dir, test_data = load_atoml_files_from_directory_setup
    test_dir = config_dir.joinpath('flat')
    assert test_dir.exists()
    atc = ATomlConfig(directory_path=test_dir)
    test_result = test_data(atc)
    assert len(atc.atoml_files) == 4
    assert test_result


def test_load_atoml_files_from_one_deep_dir(load_atoml_files_from_directory_setup):
    config_dir, test_data = load_atoml_files_from_directory_setup
    test_dir = config_dir.joinpath('one_deep')
    assert test_dir.exists()
    atc = ATomlConfig(directory_path=test_dir)
    test_result = test_data(atc)
    assert len(atc.atoml_files) == 2
    assert test_result


def test_load_atoml_files_from_nest_dir(load_atoml_files_from_directory_setup):
    config_dir, test_data = load_atoml_files_from_directory_setup
    test_dir = config_dir.joinpath('nested')
    assert test_dir.exists()
    atc = ATomlConfig(directory_path=test_dir)
    test_result = test_data(atc)

    assert len(atc.atoml_files) == 1
    assert test_result




@pytest.fixture()
def abc_mapping_setup() -> Path:
    config_dir = TEST_BASE_DIR.joinpath("abc_mapping")
    assert config_dir.exists()
    yield (config_dir)


def test_data_access(abc_mapping_setup):
    config_dir = abc_mapping_setup
    test_dir = config_dir.joinpath('data_access')
    assert test_dir.exists()
    atc = ATomlConfig(directory_path=test_dir)
    assert len(atc.atoml_files) == 4

    assert "user" in atc
    assert "valid_toml" in atc
    assert "ASDF" not in atc

    assert "user" in atc.keys()

    assert "first_name" in atc["user"]
    assert atc["user"]["first_name"] == 'Eric'

    assert 'Eric' in atc["user"].values()

    atc_items = atc.items()
    assert len(atc_items) > 0

    assert 'first_name' in atc.get("user")




def test_load_atoml_multiple_paths():
    config_dir_01 = TEST_BASE_DIR.joinpath("load_atoml_settings_file/present")
    config_dir_02 = TEST_BASE_DIR.joinpath("load_atoml_settings_file/absent")
    atoml_settings_file = config_dir_01.joinpath('__init__.toml')
    atc = ATomlConfig(directory_path=[config_dir_01, config_dir_02])
    assert config_dir_01.exists()
    assert config_dir_02.exists()
    assert atoml_settings_file.exists()
    assert atc._atoml_settings_file.file_path == atoml_settings_file


