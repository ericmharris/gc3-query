import pytest

from gc3_query.lib.models.gc3_meta_data import GC3MetaData


@pytest.fixture()
def session_setup() -> GC3MetaData:
    model = GC3MetaData()
    yield model
    print(f"setup_session closing Session...")


def test_username(session_setup):
    model = session_setup
    assert model.username == "eric.harris@oracle.com"
