import pytest
import toml
from pathlib import Path

from gc3_query.lib import *
from gc3_query.lib import gc3_cfg
from gc3_query.lib import BASE_DIR

from gc3_query.lib.gc3_config import GC3Config, IDMCredential
from gc3_query.lib.iaas_classic.requests_client import IaaSRequestsHTTPClient
from gc3_query.lib.iaas_classic import IaaSServiceBase, API_SPEC_DIR

TEST_BASE_DIR: Path = Path(__file__).parent
# config_dir = TEST_BASE_DIR.joinpath("config")
config_dir = BASE_DIR.joinpath("etc/config")


def test_setup():
    assert TEST_BASE_DIR.exists()
    assert config_dir.exists()
    assert API_SPEC_DIR.exists()



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


def test_service_call(setup_gc30003):
    service_cfg, idm_cfg = setup_gc30003
    iaas_service_base = IaaSServiceBase(service_cfg=service_cfg, idm_cfg=idm_cfg)
    assert 'nimbula' in iaas_service_base.http_client.auth_cookie_header['Cookie']
    http_future = iaas_service_base.service_operations.discover_root_instance()
    service_response = http_future.response()
    assert service_response.metadata.status_code==200
    assert "/Compute-" in service_response.result


def test_pre_authenticated_http_client(setup_gc30003):
    service_cfg, idm_cfg = setup_gc30003
    http_client = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    http_client_id = id(http_client)
    assert http_client.skip_authentication==False
    assert http_client.idm_domain_name==idm_cfg.name
    assert http_client.auth_cookie_header is not None
    assert 'nimbula' in http_client.auth_cookie_header['Cookie']

    iaas_service_base = IaaSServiceBase(service_cfg=service_cfg, idm_cfg=idm_cfg, http_client=http_client)
    assert 'nimbula' in iaas_service_base.http_client.auth_cookie_header['Cookie']
    http_future = iaas_service_base.service_operations.discover_root_instance()
    service_response = http_future.response()
    assert service_response.metadata.status_code==200
    assert "/Compute-" in service_response.result
    assert id(iaas_service_base.http_client)==http_client_id
    assert iaas_service_base.http_client is http_client



@pytest.fixture()
def setup_preauthed_gc30003():
    service = 'Instances'
    idm_domain = 'gc30003'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    service_cfg = gc3_config.iaas_classic.services[service]
    idm_cfg = gc3_config.idm.domains[idm_domain]
    http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    assert service==service_cfg.name
    assert idm_domain==idm_cfg.name
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    yield service_cfg, idm_cfg, http_client


def test_get_idm_container_names(setup_preauthed_gc30003):
    service_cfg, idm_cfg, http_client = setup_preauthed_gc30003
    iaas_service_base = IaaSServiceBase(service_cfg=service_cfg, idm_cfg=idm_cfg, http_client=http_client)
    http_future = iaas_service_base.service_operations.discover_root_instance()
    service_response = http_future.response()
    # '/Compute-587626604/'
    idm_container_name = service_response.incoming_response.json()['result'][0]
    # '/Compute-587626604/eric.harris@oracle.com/'
    idm_user_container_name = f"{idm_container_name}{gc3_cfg.user.cloud_username}/"
    assert iaas_service_base.idm_container_name==idm_container_name
    assert iaas_service_base.idm_user_container_name==idm_user_container_name
    assert iaas_service_base.get_idm_container_name(cloud_username="foo.bar@oracle.com")==f"{idm_container_name}foo.bar@oracle.com/"





