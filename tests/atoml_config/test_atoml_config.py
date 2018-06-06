
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
        atc = ATomlConfig(atoml_file_paths=None, atoml_dir_path=None)




def test_load_atoml_settings_file_present():
    config_dir = TEST_BASE_DIR.joinpath("load_atoml_settings_file/present")
    atoml_settings_file = config_dir.joinpath('__init__.toml')
    atc = ATomlConfig(atoml_dir_path=config_dir)
    assert config_dir.exists()
    assert atoml_settings_file.exists()
    assert atc._atoml_settings_file.file_path == atoml_settings_file

def test_load_atoml_settings_file_absent():
    config_dir = TEST_BASE_DIR.joinpath("load_atoml_settings_file/absent")
    atoml_settings_file = config_dir.joinpath('__init__.toml')
    atc = ATomlConfig(atoml_dir_path=config_dir)
    assert config_dir.exists()
    assert not atoml_settings_file.exists()
    assert atc._atoml_settings_file==None


@pytest.fixture()
def load_atoml_files_individually_setup() -> List[str]:
    config_dir = TEST_BASE_DIR.joinpath("load_atoml_files/test_load_atoml_files_individually")
    assert config_dir.exists()
    yield (config_dir)

def test_load_atoml_files_individually(load_atoml_files_individually_setup):
    config_dir = load_atoml_files_individually_setup
    at_files = config_dir.glob('*.toml')
    atc = ATomlConfig(atoml_file_paths=at_files)
    assert len(atc.atoml_files) > 1
    assert 'title' in atc.toml
    assert 'rest_url' in atc.toml['idm_domains']['gc3pilot']


def test_file_names(load_atoml_files_individually_setup):
    config_dir = load_atoml_files_individually_setup
    at_files = config_dir.glob('*.toml')
    atc = ATomlConfig(atoml_file_paths=at_files)
    assert '__init__.toml' in atc.file_names
    assert 'user_info.toml' in atc.file_names


def test_load_atoml_files_from_dir():
    assert False



# def test_load_atoml_files_from_directory():
#     config_dir = TEST_BASE_DIR.joinpath("load_atoml_files/test_load_atoml_files_from_directory")
#     assert config_dir.exists()
#     atc = ATomlConfig(atoml_dir=config_dir)
#     assert len(atc.atoml_files)>0





# @pytest.fixture()
# def load_atoml_files_setup() -> List[str]:
#
#     valid_toml = [
#         "first = Eric",
#         "  last_name  =   Harris",
#         "role = primary=admin",
#         "email = eric.harris@oracle.com",
#         r"home_directory = C:\Users\eharris"]
#
#
#     annotated_toml = {
#         "first: str = Eric": "str",
#         "last name: str = Harris": "str",
#         "emplid: int = 12345": "int",
#         " role: Role   = primary=admin": "Role",
#         "primary@address: email = eric.harris@oracle.com": "email"
#     }
#
#     one_off_cases_toml = {
#         # "first: str = Eric": "str",
#         "last name = Harris": "None",
#         " role: Role   = primary=admin": "Role",
#         "primary@address: email = eric.harris@oracle.com": "email",
#         "line with no eq in it": "None"
#     }
#
#     yield (valid_toml, annotated_toml, one_off_cases_toml)
#
#
# def test_toml_file_with_valid(atoml_config_setup):
#     valid_toml, annotated_toml, one_off_cases_toml = atoml_config_setup
#     for s in valid_toml:
#         pre_proc_line = ATomlFile.pre_process_line(s)
#         assert pre_proc_line.type_name=='None'
#         assert pre_proc_line.input in valid_toml



