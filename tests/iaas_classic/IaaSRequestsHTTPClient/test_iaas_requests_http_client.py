from pathlib import Path

import pytest

from gc3_query.lib import *
from gc3_query.lib.gc3_config import GC3Config
from gc3_query.lib.iaas_classic.iaas_requests_http_client import IaaSRequestsHTTPClient

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
    http_client = IaaSRequestsHTTPClient(idm_cfg=idm_cfg, skip_authentication=True)
    assert http_client.skip_authentication==True
    assert http_client.idm_domain_name==idm_cfg.name


def test_authentication(setup_gc30003):
    idm_cfg = setup_gc30003
    http_client = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    assert http_client.skip_authentication==False
    assert http_client.idm_domain_name==idm_cfg.name
    assert http_client.auth_cookie_header is not None
    assert 'nimbula' in http_client.auth_cookie_header['Cookie']



@pytest.fixture()
def setup_gc35001() -> Dict[str, Any]:
    idm_domain = 'gc35001'
    gc3_config = GC3Config()
    assert idm_domain in gc3_config['idm']['domains']
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    check_credential = gc3_config.get_credential(idm_domain_name=idm_domain)
    idm_cfg = gc3_config['idm']['domains'][idm_domain]
    yield idm_cfg


def test_init_no_auth_idcs(setup_gc35001):
    idm_cfg = setup_gc35001
    http_client = IaaSRequestsHTTPClient(idm_cfg=idm_cfg, skip_authentication=True)
    assert http_client.skip_authentication==True
    assert http_client.idm_domain_name==idm_cfg.name


def test_authentication_idcs(setup_gc35001):
    idm_cfg = setup_gc35001
    http_client = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    assert http_client.skip_authentication==False
    assert http_client.idm_domain_name==idm_cfg.name
    assert http_client.auth_cookie_header is not None
    assert 'nimbula' in http_client.auth_cookie_header['Cookie']


