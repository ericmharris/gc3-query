import pytest
import toml
from pathlib import Path

from gc3_query.lib import *
from gc3_query.lib import BASE_DIR

from gc3_query.lib.gc3_config import GC3Config, IDMCredential
from gc3_query.lib.iaas_classic.requests_client import IaaSRequestsClient
from gc3_query.lib.iaas_classic import IaaSServiceBase

TEST_BASE_DIR: Path = Path(__file__).parent
# config_dir = TEST_BASE_DIR.joinpath("config")
config_dir = BASE_DIR.joinpath("etc/config")


def test_setup():
    assert TEST_BASE_DIR.exists()
    assert config_dir.exists()



@pytest.fixture()
def setup_gc30003() -> Tuple[Dict[str, Any]]:
    service = 'Instances'
    idm_domain = 'gc30003'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    service_cfg = gc3_config.iaas_classic.services[service]
    idm_cfg = gc3_config.idm.domains[idm_domain]
    assert service==service_cfg.name
    assert idm_domain==idm_cfg.name
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    yield service_cfg, idm_cfg


def test_init_no_auth(setup_gc30003):
    service_cfg, idm_cfg = setup_gc30003
    iaas_service_base = IaaSServiceBase(service_cfg=service_cfg, idm_cfg=idm_cfg, skip_authentication=True)
    assert iaas_service_base.http_client.skip_authentication==True
    assert iaas_service_base.http_client.idm_domain_name==idm_cfg.name


def test_authentication(setup_gc30003):
    service_cfg, idm_cfg = setup_gc30003
    iaas_service_base = IaaSServiceBase(service_cfg=service_cfg, idm_cfg=idm_cfg)
    assert iaas_service_base.http_client.skip_authentication==False
    assert iaas_service_base.http_client.idm_domain_name==idm_cfg.name
    assert iaas_service_base.http_client.auth_cookie_header is not None
    assert 'nimbula' in iaas_service_base.http_client.auth_cookie_header['Cookie']
