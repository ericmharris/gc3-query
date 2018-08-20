from pathlib import Path

import pytest

from gc3_query.lib.atoml.util import quote_key

TEST_BASE_DIR: Path = Path(__file__).parent
CONFIG_DIR: Path = Path(__file__).parent.joinpath("config")





@pytest.fixture()
def quote_key_setup() -> List[str]:
    toml_file = CONFIG_DIR.joinpath("quote_key.toml_text")

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
        "line with no eq in it",
        r"home directory c:\ = C:\Users\eharris"
    ]

    invalid_toml_quoted = [
        "'first: str' = Eric",
        "'last name' = Harris",
        "'role: Role' = primary=admin",
        "'email@address' = eric.harris@oracle.com",
        "line with no eq in it",
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











