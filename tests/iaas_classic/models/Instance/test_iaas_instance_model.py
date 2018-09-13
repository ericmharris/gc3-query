import datetime
from pathlib import Path

import pytest
from dateutil.tz import tzutc
from pymongo import MongoClient

from gc3_query.lib import gc3_cfg
from gc3_query.lib.export_delegates.mongodb import storage_adapter_init
from gc3_query.lib.gc3_config import GC3Config
from gc3_query.lib.iaas_classic import IaaSRequestsHTTPClient
from gc3_query.lib.iaas_classic.instances import Instances
from gc3_query.lib.iaas_classic.models.instance_model import InstanceModel
# fixme? from gc3_query.lib.open_api import API_SPECS_DIR
# from pprint import pprint, pformat
from mongoengine import QuerySet

TEST_BASE_DIR: Path = Path(__file__).parent
# config_dir = TEST_BASE_DIR.joinpath("config")
config_dir = gc3_cfg.BASE_DIR.joinpath("etc/config")
output_dir = TEST_BASE_DIR.joinpath('output')


def test_setup():
    assert TEST_BASE_DIR.exists()
    # assert API_SPECS_DIR.exists()
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
    connection_config = storage_adapter_init()
    assert service==service_cfg.name
    assert idm_domain==idm_cfg.name
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    yield service_cfg, idm_cfg, http_client, connection_config


def test_init(setup_gc30003):
    service_cfg, idm_cfg, http_client, connection_config = setup_gc30003
    instances = Instances(service_cfg=service_cfg, idm_cfg=idm_cfg, http_client=http_client)
    assert instances.http_client.skip_authentication==False
    assert instances.http_client.idm_domain_name==idm_cfg.name
    assert instances.http_client.auth_cookie_header is not None
    assert 'nimbula' in instances.http_client.auth_cookie_header['Cookie']


def test_get_instance_details(setup_gc30003):
    service_cfg, idm_cfg, http_client, connection_config = setup_gc30003
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





@pytest.fixture()
def setup_gc30003_instances():
    service = 'Instances'
    idm_domain = 'gc30003'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    idm_cfg = gc3_config.idm.domains[idm_domain]
    http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    connection_config = storage_adapter_init()
    instances = Instances(service_cfg=service_cfg, idm_cfg=idm_cfg, http_client=http_client)
    assert service==service_cfg.name
    assert idm_domain==idm_cfg.name
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    yield service_cfg, idm_cfg, http_client, connection_config, instances


def test_instance_model_save(setup_gc30003_instances):
    service_cfg, idm_cfg, http_client, connection_config, instances = setup_gc30003_instances
    name = 'Compute-587626604/eric.harris@oracle.com/gc3_naac_soar_ebs1226_demo_01/8706cea9-6f49-428f-b354-a3748478d1c2/'
    service_response = instances.get_instance(name=name)
    # request_url = http_future.future.request.url
    # service_response = http_future.response()
    # result = service_response.result

    # instance_details = instances.get_instance_details(name=name)
    # assert instance_details.domain == 'compute-587626604.oraclecloud.internal.'
    # instance_model = InstanceModel(instance_details=instance_details)
    # # '/Compute-587626604/eric.harris@oracle.com/gc3_naac_soar_ebs1226_demo_01/8706cea9-6f49-428f-b354-a3748478d1c2'

    assert service_response.metadata.status_code==200
    results_json = service_response.incoming_response.json()['result']
    assert len(results_json) == 1
    result_json = results_json[0]
    instance_model = InstanceModel(**result_json)
    saved = instance_model.save()
    assert saved


def test_instances_model_save():
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

    # container=instances.idm_container_name.replace('/', '')
    # old_container=instances.idm_container_name

    # container='/Compute-587626604'
    # container='Compute-587626604'
    # container=instances.idm_root_container_name

    # http_future = instances.bravado_service_operations.listInstance(container=instances.idm_user_container_name)
    # http_future = instances.bravado_service_operations.listInstance(container=instances.idm_container_name)
    # http_future = instances.bravado_service_operations.listInstance(container=container)
    # http_future = instances.service_operations.discover_root_instance()
    service_response = instances.dump()
    result = service_response.result
    result_json = service_response.incoming_response.json()
    assert service_response.metadata.status_code==200
    # instance_model = InstanceModel(instance_details=instance_details)
    # # '/Compute-587626604/eric.harris@oracle.com/gc3_naac_soar_ebs1226_demo_01/8706cea9-6f49-428f-b354-a3748478d1c2'
    # assert instance_model.name==instance_details.name
    # saved = instance_model.save()
    # assert saved





@pytest.fixture()
def setup_gc30003_model():
    service = 'Instances'
    idm_domain = 'gc30003'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    idm_cfg = gc3_config.idm.domains[idm_domain]
    mongodb_connection: MongoClient = storage_adapter_init(mongodb_config=gc3_cfg.iaas_classic.mongodb.as_dict())
    iaas_service = Instances(service_cfg=service_cfg, idm_cfg=idm_cfg)
    assert service==service_cfg.name
    assert idm_domain==idm_cfg.name
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    yield service_cfg, idm_cfg, iaas_service, mongodb_connection


def test_dump(setup_gc30003_model):
    service_cfg, idm_cfg, iaas_service, mongodb_connection = setup_gc30003_model
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    service_response = iaas_service.dump()
    assert service_response.result
    result = service_response.result


def test_save_one(setup_gc30003_model):
    service_cfg, idm_cfg, iaas_service, mongodb_connection = setup_gc30003_model
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    service_response = iaas_service.dump()
    assert service_response.result
    result = service_response.result
    results = service_response.result.result
    result_dict = service_response.incoming_response.json()
    first_result = results[0]
    first_result_dict = first_result._as_dict()
    instance_model = InstanceModel(**first_result_dict)
    saved = instance_model.save()
    assert saved


def test_save_all(setup_gc30003_model):
    service_cfg, idm_cfg, iaas_service, mongodb_connection = setup_gc30003_model
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    service_response = iaas_service.dump()
    assert service_response.result
    results = service_response.result.result
    for result in results:
        result_dict = result._as_dict()
        instance_model = InstanceModel(**result_dict)
        saved = instance_model.save()



def test_insert_all(setup_gc30003_model):
    service_cfg, idm_cfg, iaas_service, mongodb_connection = setup_gc30003_model
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    service_response = iaas_service.dump()
    assert service_response.result
    results = service_response.result.result
    instances = [InstanceModel(**result._as_dict()) for result in results]
    _ = InstanceModel.objects().insert(instances)
    assert instances





@pytest.fixture()
def setup_gc30003_model_query():
    service = 'Instances'
    idm_domain = 'gc30003'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    idm_cfg = gc3_config.idm.domains[idm_domain]
    mongodb_connection: MongoClient = storage_adapter_init(mongodb_config=gc3_cfg.iaas_classic.mongodb.as_dict())
    iaas_service = Instances(service_cfg=service_cfg, idm_cfg=idm_cfg)
    assert service==service_cfg.name
    assert idm_domain==idm_cfg.name
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    yield service_cfg, idm_cfg, iaas_service, mongodb_connection




def test_query_objects(setup_gc30003_model_query):
    service_cfg, idm_cfg, iaas_service, mongodb_connection = setup_gc30003_model_query
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    objects: QuerySet = InstanceModel.objects()
    assert objects
    object = objects.first()
    assert object
    owner =  object.name.object_owner
    assert '@oracle.com' in owner
    assert  object.name.full_name.startswith('/Compute')

