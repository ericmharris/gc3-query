import pytest
import toml
from pathlib import Path

from gc3_query.lib import *
from gc3_query.lib.toml_cfg import cfg
from gc3_query.lib.toml_cfg.util import quote_key
from gc3_query.lib.toml_cfg.toml_file import TOMLFile

from gc3_query.lib.models.gc3_meta_data import GC3MetaData

TEST_BASE_DIR: Path = Path(__file__).parent
CONFIG_DIR: Path = Path(__file__).parent.joinpath("config")


# @pytest.fixture()
# def session_setup() -> TOMLConfig:
#     config = TOMLConfig()
#     yield config
#     print(f"setup_session closing Session...")
#
#
# def test_username(session_setup):
#     config = session_setup
#     assert config.username == "eric.harris@oracle.com"


# def test_get_requestium_session(session_setup):
#     s = session_setup
#     r = s.get("http://www.google.com")
#     assert r.ok
#     s.transfer_session_cookies_to_driver()
#     # r = s.driver.get("http://www.google.com")
#     assert "browserName" in s.driver.capabilities
#
#
# def test_login_bm_profile(session_setup):
#     s = login_bm_profile( username="carolyn_eide_pdx", password="Thumper!", dry_run=False, session=session_setup)
#     logout = s.driver.find_element_by_link_text("LOGOUT")
#     assert logout.text=="LOGOUT"


@pytest.fixture()
def quote_key_setup() -> List[str]:
    toml_file = CONFIG_DIR.joinpath("quote_key.toml")

    valid_toml = [
        "first = Eric",
        "  last_name  =   Harris",
        "role = primary=admin",
        "email = eric.harris@oracle.com",
        r"home_directory = C:\Users\eharris"]

    valid_toml_quoted = [
        "'first' = Eric",
        "'last_name' = Harris",
        "'role' = primary=admin",
        "'email' = eric.harris@oracle.com",
        "'os_username' = eharris",
        r"'home_directory' = C:\Users\eharris"]

    invalid_toml = [
        "first: str = Eric",
        "last name = Harris",
        " role: Role   = primary=admin",
        "email@address = eric.harris@oracle.com",
        r"home directory c:\ = C:\Users\eharris"
    ]

    invalid_toml_quoted = [
        "'first: str' = Eric",
        "'last name' = Harris",
        "'role: Role' = primary=admin",
        "'email@address' = eric.harris@oracle.com",
        r"'home directory c:\' = C:\Users\eharris"]

    yield (valid_toml, valid_toml_quoted, invalid_toml, invalid_toml_quoted)


def test_quote_key_with_valid(quote_key_setup):
    valid_toml, valid_toml_quoted, invalid_toml, invalid_toml_quoted = quote_key_setup
    for k in valid_toml:
        kq = quote_key(k)
        print(f"k={k}, kq={kq}")
        assert kq in valid_toml_quoted


def test_quote_key_with_invalid(quote_key_setup):
    valid_toml, valid_toml_quoted, invalid_toml, invalid_toml_quoted = quote_key_setup
    for k in invalid_toml:
        kq = quote_key(k)
        print(f"k={k}, kq={kq}")
        assert kq in invalid_toml_quoted


def test_quote_key_toml_file_classmethod_with_invalid(quote_key_setup):
    valid_toml, valid_toml_quoted, invalid_toml, invalid_toml_quoted = quote_key_setup
    for k in invalid_toml:
        kq = TOMLFile.quote_key(k)
        print(f"k={k}, kq={kq}")
        assert kq in invalid_toml_quoted








