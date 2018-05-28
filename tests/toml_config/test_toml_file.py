import pytest
from pathlib import Path

from gc3_query.lib.toml_cfg import cfg
from gc3_query.lib.toml_cfg.toml_file import TOMLFile

from gc3_query.lib.models.gc3_meta_data import GC3MetaData
TEST_BASE_DIR: Path = Path(__file__).parent
CONFIG_DIR: Path = Path(__file__).parent.joinpath('config')

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



def test_open_missing_file():
    missing_file = CONFIG_DIR.joinpath('not_there.toml')
    with pytest.raises(RuntimeError) as excinfo:
        cfgf = TOMLFile(path=missing_file)


def test_quote_key():
    toml_file = CONFIG_DIR.joinpath('_quote_key.toml')
    cfgf = TOMLFile(path=toml_file)


