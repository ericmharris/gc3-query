from pathlib import Path

import pytest

from bravado.response import  BravadoResponse

from gc3_query.lib import gc3_cfg
from gc3_query.lib.gc3_config import GC3Config
from gc3_query.lib.iaas_classic import IaaSRequestsHTTPClient
from gc3_query.lib.iaas_classic.instances import Instances

# from pprint import pprint, pformat

TEST_BASE_DIR: Path = Path(__file__).parent
# config_dir = TEST_BASE_DIR.joinpath("config")
config_dir = gc3_cfg.BASE_DIR.joinpath("etc/config")
output_dir = TEST_BASE_DIR.joinpath('output')




def test_setup():
    assert TEST_BASE_DIR.exists()
    if not config_dir.exists():
        config_dir.mkdir()
    if not output_dir.exists():
        output_dir.mkdir()



@pytest.fixture()
def setup_gc30003():
    service = 'Instances'
    idm_domain = 'gc30003'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    idm_cfg = gc3_config.idm.domains[idm_domain]
    http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    assert service==service_cfg.name
    assert idm_domain==idm_cfg.name
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    yield service_cfg, idm_cfg, http_client


# def test_init_no_auth(setup_gc30003):
#     service_cfg, idm_cfg, http_client = setup_gc30003
#     instances = Instances(service_cfg=service_cfg, idm_cfg=idm_cfg, http_client=http_client,  skip_authentication=True)
#     assert instances.http_client.skip_authentication==True
#     assert instances.http_client.idm_domain_name==idm_cfg.name


def test_init(setup_gc30003):
    service_cfg, idm_cfg, http_client = setup_gc30003
    instances = Instances(service_cfg=service_cfg, idm_cfg=idm_cfg, http_client=http_client)
    assert instances.http_client.skip_authentication==False
    assert instances.http_client.idm_domain_name==idm_cfg.name
    assert instances.http_client.auth_cookie_header is not None
    assert 'nimbula' in instances.http_client.auth_cookie_header['Cookie']


def test_discover_root_instance(setup_gc30003):
    service_cfg, idm_cfg, http_client = setup_gc30003
    instances = Instances(service_cfg=service_cfg, idm_cfg=idm_cfg, http_client=http_client)
    # http_future = instances.service_operations.discover_root_instance()
    # http_future = instances.bravado_service_operations.discoverRootInstance()
    # http_future = instances.swagger_client.Instances.discoverRootInstance()
    # http_future = instances.swagger_client.Instances.discoverRootInstance(_request_options={"headers": {"Accept": "application/oracle-compute-v3+directory+json"}})
    http_future = instances.service_operations.discover_root_instance()
    request_url = http_future.future.request.url
    service_response = http_future.response()
    result = service_response.result
    http_response = service_response.incoming_response
    http_response_json = http_response.json()

    assert service_response.metadata.status_code==200
    assert f"/Compute-{instances.idm_cfg.service_instance_id}" in service_response.result

def test_discover_instance(setup_gc30003):
    service_cfg, idm_cfg, http_client = setup_gc30003
    instances = Instances(service_cfg=service_cfg, idm_cfg=idm_cfg, http_client=http_client)
    container=instances.idm_container_name
    # http_future = instances.bravado_service_operations.discoverInstance(container=container)
    http_future = instances.service_operations.discover_instance(container=container)
    request_url = http_future.future.request.url
    service_response = http_future.response()
    result = service_response.result
    http_response = service_response.incoming_response
    http_response_json = http_response.json()
    assert service_response.metadata.status_code==200


def test_list_instance(setup_gc30003):
    service_cfg, idm_cfg, http_client = setup_gc30003
    instances = Instances(service_cfg=service_cfg, idm_cfg=idm_cfg, http_client=http_client)
    container=instances.idm_root_container_name
    # http_future = instances.bravado_service_operations.listInstance(container=container)
    http_future = instances.service_operations.list_instance(container=container)
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
    # http_future = instances.bravado_service_operations.getInstance(name=name)
    http_future = instances.service_operations.get_instance(name=name)
    request_url = http_future.future.request.url
    service_response = http_future.response()
    result = service_response.result
    http_response = service_response.incoming_response
    http_response_json = http_response.json()
    assert service_response.metadata.status_code==200

def test_get_instance_details(setup_gc30003):
    service_cfg, idm_cfg, http_client = setup_gc30003
    instances = Instances(service_cfg=service_cfg, idm_cfg=idm_cfg, http_client=http_client)
    name = 'Compute-587626604/eric.harris@oracle.com/gc3_naac_soar_ebs1226_demo_01/8706cea9-6f49-428f-b354-a3748478d1c2/'
    instance_details = instances.get_instance_details(name=name)
    assert instance_details.domain == 'compute-587626604.oraclecloud.internal.'

    toml_path = output_dir.joinpath('test_get_instance_details.toml')
    toml_fd = instance_details.export(file_path=toml_path, format='toml', overwrite=True)
    assert toml_fd.exists()

    yaml_path = output_dir.joinpath('test_get_instance_details.yaml')
    yaml_fd = instance_details.export(file_path=yaml_path, format='yaml', overwrite=True)
    assert yaml_fd.exists()

    json_path = output_dir.joinpath('test_get_instance_details.json')
    json_fd = instance_details.export(file_path=json_path, format='json', overwrite=True)
    assert json_fd.exists()

def test_get_root_instance_name(setup_gc30003):
    service_cfg, idm_cfg, http_client = setup_gc30003
    instances = Instances(service_cfg=service_cfg, idm_cfg=idm_cfg, http_client=http_client)
    root_instance_name = instances.idm_root_container_name
    assert root_instance_name
    assert str(idm_cfg.service_instance_id) in root_instance_name

def test_idm_root_container_name(setup_gc30003):
    service_cfg, idm_cfg, http_client = setup_gc30003
    instances = Instances(service_cfg=service_cfg, idm_cfg=idm_cfg, http_client=http_client)
    idm_root_container_name = instances.idm_root_container_name
    assert idm_root_container_name
    expected_name = f"Compute-{idm_cfg.service_instance_id}"
    literal_name = 'Compute-587626604'
    assert expected_name==idm_root_container_name
    assert literal_name==idm_root_container_name


def test_get_all_instances(setup_gc30003):
    service_cfg, idm_cfg, http_client = setup_gc30003
    instances = Instances(service_cfg=service_cfg, idm_cfg=idm_cfg, http_client=http_client)
    instance_details = instances.get_all_instances()
    assert instance_details






@pytest.fixture()
def setup_gc30003_dump():
    service = 'Instances'
    idm_domain = 'gc30003'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    idm_cfg = gc3_config.idm.domains[idm_domain]
    iaas_service = Instances(service_cfg=service_cfg, idm_cfg=idm_cfg)
    assert service==service_cfg.name
    assert idm_domain==idm_cfg.name
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    yield service_cfg, idm_cfg, iaas_service




def test_dump(setup_gc30003_dump):
    service_cfg, idm_cfg, iaas_service = setup_gc30003_dump
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    service_response = iaas_service.dump()
    assert service_response.result
    result = service_response.result
    results = service_response.result.result
    first_result = results[0]
    result_text = service_response.incoming_response.text
    result_dict = service_response.incoming_response.json()
    first_result_dict = first_result._as_dict()
    assert first_result




# @pytest.fixture()
# def setup_gc30003_from_url():
#     service = 'Instances'
#     idm_domain = 'gc30003'
#     gc3_config = GC3Config(atoml_config_dir=config_dir)
#     service_cfg = gc3_config.iaas_classic.services.compute[service]
#     idm_cfg = gc3_config.idm.domains[idm_domain]
#     http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
#     assert service==service_cfg.name
#     assert idm_domain==idm_cfg.name
#     assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
#     yield service_cfg, idm_cfg, http_client
#
# def test_discover_instance_from_url(setup_gc30003_from_url):
#     service_cfg, idm_cfg, http_client = setup_gc30003_from_url
#     instances = Instances(service_cfg=service_cfg, idm_cfg=idm_cfg, http_client=http_client, from_url=True)
#     http_future = instances.bravado_service_operations.discoverInstance(container=instances.idm_container_name)
#     request_url = http_future.future.request.url
#     service_response = http_future.response()
#     result = service_response.result
#     assert service_response.metadata.status_code==200

def test_discover_root_instance_from_url_01():
    service = 'Instances'
    idm_domain = 'gc30003'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    idm_cfg = gc3_config.idm.domains[idm_domain]
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    assert service==service_cfg.name
    assert idm_domain==idm_cfg.name
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    instances = Instances(service_cfg=service_cfg, idm_cfg=idm_cfg, from_url=True)
    # http_future = instances.swagger_client.Instances.discoverRootInstance()
    # http_future = instances.bravado_service_operations.discoverRootInstance()
    # http_future = instances.bravado_service_operations.discoverRootInstance(_request_options={"headers": {"Accept": "application/oracle-compute-v3+directory+json"}})
    http_future = instances.service_operations.discover_root_instance()
    # http_future.future.session.headers['Content-Type'] = http_future.operation.produces[0]
    # http_future = instances.service_operations.discover_root_instance()
    request_url = http_future.future.request.url
    service_response = http_future.response()
    result = service_response.result
    assert service_response.metadata.status_code==200


def test_discover_instance_from_url_01():
    service = 'Instances'
    idm_domain = 'gc30003'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    idm_cfg = gc3_config.idm.domains[idm_domain]
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    assert service==service_cfg.name
    assert idm_domain==idm_cfg.name
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    instances = Instances(service_cfg=service_cfg, idm_cfg=idm_cfg, from_url=True)
    # http_future = instances.bravado_service_operations.discoverInstance(container=instances.idm_container_name)
    http_future = instances.service_operations.discover_instance(container=instances.idm_container_name)
    # http_future = instances.service_operations.discover_root_instance()
    request_url = http_future.future.request.url
    service_response = http_future.response()
    result = service_response.result
    assert service_response.metadata.status_code==200


def test_list_instance_from_url_01():
    service = 'Instances'
    idm_domain = 'gc30003'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    idm_cfg = gc3_config.idm.domains[idm_domain]
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    assert service==service_cfg.name
    assert idm_domain==idm_cfg.name
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    instances = Instances(service_cfg=service_cfg, idm_cfg=idm_cfg, from_url=True)
    container=instances.idm_container_name.replace('/', '')
    old_container=instances.idm_container_name
    # http_future = instances.bravado_service_operations.listInstance(container=instances.idm_user_container_name)
    # http_future = instances.bravado_service_operations.listInstance(container=instances.idm_container_name)
    # http_future = instances.bravado_service_operations.listInstance(container=container)
    http_future = instances.service_operations.list_instance(container=container)
    # http_future = instances.service_operations.discover_root_instance()
    request_url = http_future.future.request.url
    service_response = http_future.response()
    result = service_response.result
    result_json = service_response.incoming_response.json()
    assert service_response.metadata.status_code==200



