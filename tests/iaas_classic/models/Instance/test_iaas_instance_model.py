import pytest
import toml
from pathlib import Path
# from pprint import pprint, pformat
from prettyprinter import pprint, pformat

from gc3_query.lib import *
from gc3_query.lib import BASE_DIR

from gc3_query.lib.gc3_config import GC3Config, IDMCredential
from gc3_query.lib.iaas_classic.iaas_requests_http_client import IaaSRequestsHTTPClient
from gc3_query.lib.iaas_classic import IaaSServiceBase, API_SPECS_DIR, IaaSRequestsHTTPClient
from gc3_query.lib.iaas_classic.instances import Instances
from gc3_query.lib.iaas_classic.models.instance_model import InstanceModel
from gc3_query.lib.storage_adapters.mongodb import storage_adapter_init

TEST_BASE_DIR: Path = Path(__file__).parent
# config_dir = TEST_BASE_DIR.joinpath("config")
config_dir = BASE_DIR.joinpath("etc/config")
output_dir = TEST_BASE_DIR.joinpath('output')




def test_setup():
    assert TEST_BASE_DIR.exists()
    assert config_dir.exists()
    assert API_SPECS_DIR.exists()
    assert output_dir.exists()


@pytest.fixture()
def setup_gc30003():
    service = 'Instances'
    idm_domain = 'gc30003'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    service_cfg = gc3_config.iaas_classic.services[service]
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
    service_cfg = gc3_config.iaas_classic.services[service]
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
    instance_details = instances.get_instance_details(name=name)
    assert instance_details.domain == 'compute-587626604.oraclecloud.internal.'
    instance_model = InstanceModel(instance_details=instance_details)
    # '/Compute-587626604/eric.harris@oracle.com/gc3_naac_soar_ebs1226_demo_01/8706cea9-6f49-428f-b354-a3748478d1c2'
    assert instance_model.name==instance_details.name
    saved = instance_model.save()
    assert saved
