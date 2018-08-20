from collections import namedtuple

import pytest

from gc3_query.lib.gc3load import TestCase
from gc3_query.lib.gc3logging import get_logging

from gc3_query.lib import get_logging
_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

TestCase = namedtuple("TestCase", "username password env_name")


@pytest.fixture(scope="module")
def session_setup() -> TestCase:
    from .secrets import username, password

    test_data = TestCase(username=username, password=password, env_name="hcmx-test")
    # cs = TestCase(username=username, password=password, new_password=new_password, env_name=test_data.env_name, headless=False, clean_profile=True)
    cs = TestCase(username=username, password=password, identity_domain_name=test_data.env_name, headless=False)
    print("Yielding Session")
    yield test_data, cs
    print(f"setup_session closing Session...")
    cs.shutdown()


def test_chrome_driver_path(session_setup):
    test_data, cs = session_setup
    assert cs.chrome_profile_dir.exists()
    assert cs.chrome_driver_path.exists()


def test_authenticate(session_setup):
    test_data, cs = session_setup
    assert cs.chrome_driver_path.exists()
    r = cs.authenticate()
    assert cs.authenticated


def test_change_password(session_setup):
    from .secrets import new_password

    test_data, cs = session_setup
    assert cs.chrome_driver_path.exists()
    r = cs.authenticate()
    c = cs.change_password(new_password=new_password)
    assert cs.authenticated


# def test_get_requestium_session(session_setup):
#     s = session_setup
#     r = s.get('http://www.google.com')
#     assert r.ok
#     s.transfer_session_cookies_to_driver()
#     # r = s.driver.get('http://www.google.com')
#     assert 'browserName' in s.driver.capabilities
#
#
# def test_login_bm_profile(session_setup):
#     s = login_bm_profile( username='carolyn_eide_pdx', password='Thumper!', dry_run=False, session=session_setup)
#     logout = s.driver.find_element_by_link_text('LOGOUT')
#     assert logout.text=='LOGOUT'
