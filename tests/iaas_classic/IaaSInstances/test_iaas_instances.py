import pytest
import toml
from pathlib import Path

from gc3_query.lib import *
from gc3_query.lib import BASE_DIR

from gc3_query.lib.gc3_config import GC3Config, IDMCredential
from gc3_query.lib.iaas_classic.iaas_requests_http_client import IaaSRequestsHTTPClient
from gc3_query.lib.iaas_classic import IaaSServiceBase, API_SPEC_DIR, IaaSRequestsHTTPClient
from gc3_query.lib.iaas_classic.instances import Instances

TEST_BASE_DIR: Path = Path(__file__).parent
# config_dir = TEST_BASE_DIR.joinpath("config")
config_dir = BASE_DIR.joinpath("etc/config")


def test_setup():
    assert TEST_BASE_DIR.exists()
    assert config_dir.exists()
    assert API_SPEC_DIR.exists()



@pytest.fixture()
def setup_gc30003():
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


def test_init_no_auth(setup_gc30003):
    service_cfg, idm_cfg, http_client = setup_gc30003
    instances = Instances(service_cfg=service_cfg, idm_cfg=idm_cfg, http_client=http_client,  skip_authentication=True)
    assert instances.http_client.skip_authentication==True
    assert instances.http_client.idm_domain_name==idm_cfg.name


def test_authentication(setup_gc30003):
    service_cfg, idm_cfg, http_client = setup_gc30003
    instances = Instances(service_cfg=service_cfg, idm_cfg=idm_cfg, http_client=http_client)
    assert instances.http_client.skip_authentication==False
    assert instances.http_client.idm_domain_name==idm_cfg.name
    assert instances.http_client.auth_cookie_header is not None
    assert 'nimbula' in instances.http_client.auth_cookie_header['Cookie']


def test_discover_root_instance(setup_gc30003):
    service_cfg, idm_cfg, http_client = setup_gc30003
    instances = Instances(service_cfg=service_cfg, idm_cfg=idm_cfg, http_client=http_client)
    http_future = instances.service_operations.discover_root_instance()
    service_response = http_future.response()
    assert service_response.metadata.status_code==200
    assert f"/Compute-{instances.idm_cfg.service_instance_id}" in service_response.result

def test_discover_instance(setup_gc30003):
    service_cfg, idm_cfg, http_client = setup_gc30003
    instances = Instances(service_cfg=service_cfg, idm_cfg=idm_cfg, http_client=http_client)
    container=instances.idm_container_name
    http_future = instances.bravado_service_operations.discoverInstance(container=container)
    request_url = http_future.future.request.url
    service_response = http_future.response()
    result = service_response.result
    http_response = service_response.incoming_response
    http_response_json = http_response.json()
    assert service_response.metadata.status_code==200


def test_list_instance(setup_gc30003):
    service_cfg, idm_cfg, http_client = setup_gc30003
    instances = Instances(service_cfg=service_cfg, idm_cfg=idm_cfg, http_client=http_client)
    container=instances.idm_container_name.replace('/', '')
    container=instances.idm_user_container_name[0:-1]
    http_future = instances.bravado_service_operations.listInstance(container=container)
    request_url = http_future.future.request.url
    service_response = http_future.response()
    result = service_response.result
    http_response = service_response.incoming_response
    http_response_json = http_response.json()
    assert service_response.metadata.status_code==200

def test_get_instance(setup_gc30003):
    service_cfg, idm_cfg, http_client = setup_gc30003
    instances = Instances(service_cfg=service_cfg, idm_cfg=idm_cfg, http_client=http_client)
    container=instances.idm_container_name.replace('/', '')
    container=instances.idm_user_container_name[0:-1]
    name = '/Compute-587626604/eric.harris@oracle.com/gc3_naac_soar_ebs1226_demo_01'
    name = '/Compute-587626604/eric.harris@oracle.com/gc3_naac_soar_ebs1226_demo_01/'
    # this nanme returned the next value
    name = 'Compute-587626604/eric.harris@oracle.com/gc3_naac_soar_ebs1226_demo_01'
    name = '/Compute-587626604/eric.harris@oracle.com/gc3_naac_soar_ebs1226_demo_01/8706cea9-6f49-428f-b354-a3748478d1c2'
    # returned an empty list
    name = 'Compute-587626604/eric.harris@oracle.com/gc3_naac_soar_ebs1226_demo_01/8706cea9-6f49-428f-b354-a3748478d1c2'
    name = 'Compute-587626604/eric.harris@oracle.com/gc3_naac_soar_ebs1226_demo_01/8706cea9-6f49-428f-b354-a3748478d1c2/'
    http_future = instances.bravado_service_operations.getInstance(name=name)
    request_url = http_future.future.request.url
    service_response = http_future.response()
    result = service_response.result
    http_response = service_response.incoming_response
    http_response_json = http_response.json()
    assert service_response.metadata.status_code==200


@pytest.fixture()
def setup_gc30003_from_url():
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

def test_discover_instance_from_url(setup_gc30003_from_url):
    service_cfg, idm_cfg, http_client = setup_gc30003_from_url
    instances = Instances(service_cfg=service_cfg, idm_cfg=idm_cfg, http_client=http_client, from_url=True)
    http_future = instances.bravado_service_operations.discoverInstance(container=instances.idm_container_name)
    request_url = http_future.future.request.url
    service_response = http_future.response()
    result = service_response.result
    assert service_response.metadata.status_code==200


