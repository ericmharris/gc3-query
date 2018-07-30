import pytest
import toml
from pathlib import Path

from gc3_query.lib import *

from gc3_query.lib.gc3_config import GC3Config, IDMCredential
from gc3_query.lib.iaas_classic.requests_client import IaaSRequestsClient

TEST_BASE_DIR: Path = Path(__file__).parent
config_dir = TEST_BASE_DIR.joinpath("config")


def test_setup():
    assert TEST_BASE_DIR.exists()
    assert config_dir.exists()



@pytest.fixture()
def setup_gc30003() -> Dict[str, Any]:
    idm_domain = 'gc30003'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    assert idm_domain in gc3_config['idm']['domains']
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    yield (gc3_config['idm']['domains'][idm_domain])


def test_init_no_auth(setup_gc30003):
    idm_cfg = setup_gc30003
    iaas_client = IaaSRequestsClient(idm_cfg=idm_cfg, skip_authentication=True)
    assert iaas_client.skip_authentication==True
    assert iaas_client.idm_domain_name==idm_cfg.name


def test_authentication(setup_gc30003):
    idm_cfg = setup_gc30003
    iaas_client = IaaSRequestsClient(idm_cfg=idm_cfg)
    assert iaas_client.skip_authentication==False
    assert iaas_client.idm_domain_name==idm_cfg.name
    assert iaas_client.auth_cookie_header is not None
    assert 'nimbula' in iaas_client.auth_cookie_header['Cookie']
