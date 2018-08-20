from change_cloud_pass.lib import *

from change_cloud_pass.lib.logging import Logging


# @pytest.fixture(scope='module')
# def session_setup() -> CloudSession:
#     from .secrets import username, current_password, new_password
#     test_data = TestCase(username=username, current_password=current_password, new_password=new_password, env_name='hcmx-test')
#     # cs = CloudSession(username=username, current_password=current_password, new_password=new_password, env_name=test_data.env_name, headless=False, clean_profile=True)
#     cs = CloudSession(username=username, current_password=current_password, new_password=new_password, identity_domain_name=test_data.env_name, headless=False)
#     print('Yielding Session')
#     yield test_data, cs
#     print(f'setup_session closing Session...')
#     cs.shutdown()

# def test_chrome_driver_path(session_setup):
#     test_data, cs = session_setup
#     assert cs.chrome_profile_dir.exists()
#     assert cs.chrome_driver_path.exists()

# def test_authenticate(session_setup):
#     test_data, cs = session_setup
#     assert cs.chrome_driver_path.exists()
#     r = cs.authenticate()
#     assert cs.authenticated


# def test_get_requestium_session(session_setup):
#     s = session_setup
#     r = s.get('http://www.google.com')
#     assert r.ok
#     s.transfer_session_cookies_to_driver()
#     # r = s.driver.get('http://www.google.com')
#     assert 'browserName' in s.driver.capabilities
#
#


def test_set_default_logging():
    l = "debug"
    level = Logging.set_default_logging_level(l)
    assert level == l
    assert Logging.default_logging_level == l


def test_get_default_logging():
    from change_cloud_pass.lib import get_logging

    l = "critical"
    level = Logging.set_default_logging_level(l)
    assert level == l
    assert Logging.default_logging_level == l
    _debug, _info, _warning, _error, _critical = get_logging(name=__name__)
    assert Logging.default_logging_level == l
