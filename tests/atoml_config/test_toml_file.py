
from pathlib import Path

import pytest

from gc3_query.lib import *
from gc3_query.lib.atoml.atoml_file import ATomlFile

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
    tf = ATomlFile(file_path=test_toml_file)
    assert True
    assert tf is not None



#### These two lines throw an exception from toml
# 'rest_url:url' = 'https://compute.uscom-central-1.oraclecloud.com/'
# 'sftp_url:url' = 'sftp://sftp.us2.cloud.oracle.com:22'
def test_annotated_file_01():
    config_dir = Path(__file__).parent.joinpath("ATomlFile/test_annotated_file_01")
    at_file = config_dir.joinpath("idm.toml")
    assert at_file.exists()
    atf = ATomlFile(file_path=at_file)
    assert atf.toml is not None
    assert 'rest_url' in atf.toml['idm']['gc3pilot']

# Test the rest of that file
def test_annotated_file_02():
    config_dir = Path(__file__).parent.joinpath("ATomlFile/test_annotated_file_02")
    at_file = config_dir.joinpath("idm.toml")
    assert at_file.exists()
    atf = ATomlFile(file_path=at_file)
    assert atf.toml is not None
    assert 'rest_url' in atf.toml['idm']['gc3pilot']

# Make sure the in-memory representation of the file has the same number of lines as the actual file (ie. no extra \n's)
def test_file_length():
    config_dir = Path(__file__).parent.joinpath("ATomlFile/test_file_length")
    tfile_orig = config_dir.joinpath("gc30003.toml")
    # tfile_in_memory = config_dir.joinpath("gc30003_in_memory.toml")
    atf_orig = ATomlFile(file_path=tfile_orig)
    assert tfile_orig.exists()
    # assert tfile_in_memory.exists()
    assert len(atf_orig._lines) == len(atf_orig.toml_text.splitlines())
