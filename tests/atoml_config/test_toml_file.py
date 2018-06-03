
import pytest
import toml
from pathlib import Path

from gc3_query.lib import *
from gc3_query.lib.atoml_cfg.atoml_file import ATomlFile

from gc3_query.lib.models.gc3_meta_data import GC3MetaData

TEST_BASE_DIR: Path = Path(__file__).parent
CONFIG_DIR: Path = Path(__file__).parent.joinpath("test_load_file")


@pytest.fixture()
def pre_process_line_setup() -> List[str]:

    valid_toml = [
        "first = Eric",
        "  last_name  =   Harris",
        "role = primary=admin",
        "email = eric.harris@oracle.com",
        r"home_directory = C:\Users\eharris"]


    annotated_toml = {
        "first: str = Eric": "str",
        "last name: str = Harris": "str",
        "emplid: int = 12345": "int",
        " role: Role   = primary=admin": "Role",
        "primary@address: email = eric.harris@oracle.com": "email"
    }

    one_off_cases_toml = {
        # "first: str = Eric": "str",
        "last name = Harris": "None",
        " role: Role   = primary=admin": "Role",
        "primary@address: email = eric.harris@oracle.com": "email",
        "line with no eq in it": "None"
    }

    yield (valid_toml, annotated_toml, one_off_cases_toml)


def test_toml_file_with_valid(pre_process_line_setup):
    valid_toml, annotated_toml, one_off_cases_toml = pre_process_line_setup
    for s in valid_toml:
        pre_proc_line = ATomlFile.pre_process_line(s)
        assert pre_proc_line.type_name=='None'
        assert pre_proc_line.input in valid_toml


def test_with_annotations(pre_process_line_setup):
    valid_toml, annotated_toml, one_off_cases_toml = pre_process_line_setup
    for s, type in annotated_toml.items():
        pre_proc_line = ATomlFile.pre_process_line(s)
        assert pre_proc_line.type_name in s
        assert pre_proc_line.type_name == type
        assert pre_proc_line.type_name not in pre_proc_line.toml


def test_one_off_cases_toml(pre_process_line_setup):
    valid_toml, annotated_toml, one_off_cases_toml = pre_process_line_setup
    for s, type in one_off_cases_toml.items():
        pre_proc_line = ATomlFile.pre_process_line(s)
        assert pre_proc_line.type_name == type



@pytest.fixture()
def test_load_file_setup():
    assert CONFIG_DIR.exists()
    yield CONFIG_DIR


def test_file_load_01(test_load_file_setup):
    config_dir = test_load_file_setup
    test_toml_file: Path = config_dir.joinpath('user_info_basic.toml')
    assert test_toml_file.exists()
    tf = ATomlFile(path=test_toml_file)
    assert True
    assert tf is not None
