import pytest

from gc3_query.lib.models.instance import Instance


@pytest.fixture()
def session_setup() -> Instance:
    instance = Instance()
    yield instance
    print(f"setup_session closing Session...")


def test_username(session_setup):
    instance = session_setup
    assert instance.gc3_meta_data.username == "eric.harris@oracle.com"
