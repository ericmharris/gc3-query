import json
from pathlib import Path

import pytest
from bravado_core.spec import Spec

from gc3_query import BASE_DIR
from gc3_query.lib import *
from gc3_query.lib import gc3_cfg
from gc3_query.lib.gc3_config import GC3Config
from gc3_query.lib.iaas_classic import BRAVADO_CONFIG
from gc3_query.lib.iaas_classic import IaaSServiceBase
from gc3_query.lib.iaas_classic.iaas_requests_http_client import IaaSRequestsHTTPClient
from gc3_query.lib.iaas_classic.sec_rules import SecRules
# from gc3_query.lib.open_api import API_SPECS_DIR

TEST_BASE_DIR: Path = Path(__file__).parent
# config_dir = TEST_BASE_DIR.joinpath("config")
config_dir = BASE_DIR.joinpath("etc/config")
output_dir = TEST_BASE_DIR.joinpath('output')
spec_files_dir = TEST_BASE_DIR.joinpath('spec_files')


def test_setup():
    assert TEST_BASE_DIR.exists()
    if not config_dir.exists():
        config_dir.mkdir()
    if not output_dir.exists():
        output_dir.mkdir()
    if not spec_files_dir.exists():
        spec_files_dir.mkdir()



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
    # http_future = iaas_service_base.service_operations.discover_root_instance(_request_options={"headers": {"Accept": "application/oracle-compute-v3+directory+json"}})
    http_future = iaas_service_base.service_operations.discover_root_instance()
    service_response = http_future.response()
    assert service_response.metadata.status_code==200
    assert "/Compute-" in service_response.result


def test_bravado_service_call(setup_gc30003):
    service_cfg, idm_cfg = setup_gc30003
    iaas_service_base = IaaSServiceBase(service_cfg=service_cfg, idm_cfg=idm_cfg)
    assert 'nimbula' in iaas_service_base.http_client.auth_cookie_header['Cookie']
    # http_future = iaas_service_base.service_operations.discover_root_instance(_request_options={"headers": {"Accept": "application/oracle-compute-v3+directory+json"}})
    # http_future = iaas_service_base.bravado_service_operations.discoverRootInstance(_request_options={"headers": {"Accept": "application/oracle-compute-v3+directory+json"}})
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
    # http_future = iaas_service_base.service_operations.discover_root_instance()
    # http_future = iaas_service_base.service_operations.discover_root_instance(_request_options={"headers": {"Accept": "application/oracle-compute-v3+directory+json"}})
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
    # http_future = iaas_service_base.service_operations.discover_root_instance()
    # http_future = iaas_service_base.service_operations.discover_root_instance(_request_options={"headers": {"Accept": "application/oracle-compute-v3+directory+json"}})
    http_future = iaas_service_base.service_operations.discover_root_instance()
    service_response = http_future.response()
    # '/Compute-587626604/'
    idm_container_name = service_response.incoming_response.json()['result'][0].lstrip('/').rstrip('/')
    # '/Compute-587626604/eric.harris@oracle.com/'
    idm_user_container_name = f"{idm_container_name}/{gc3_cfg.user.cloud_username}"
    idm_container_name = f"{idm_container_name}"
    idm_root_container_name = f"{idm_container_name}"
    assert iaas_service_base.idm_container_name==idm_container_name
    assert iaas_service_base.idm_user_container_name==idm_user_container_name
    assert iaas_service_base.idm_root_container_name==idm_root_container_name
    assert iaas_service_base.get_idm_user_container_name(cloud_username="foo.bar@oracle.com") == f"{idm_container_name}/foo.bar@oracle.com"


def test_idm_root_container_name(setup_preauthed_gc30003):
    service_cfg, idm_cfg, http_client = setup_preauthed_gc30003
    instances = IaaSServiceBase(service_cfg=service_cfg, idm_cfg=idm_cfg, http_client=http_client)
    idm_root_container_name = instances.idm_root_container_name
    assert idm_root_container_name
    expected_name = f"Compute-{idm_cfg.service_instance_id}"
    literal_name = 'Compute-587626604'
    assert expected_name==idm_root_container_name
    assert literal_name==idm_root_container_name



@pytest.fixture()
def setup_gc30003_oapi_spec_catalog() -> Tuple[Dict[str, Any]]:
    service = 'Instances'
    idm_domain = 'gc30003'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    service_cfg = gc3_config.iaas_classic.services[service]
    idm_cfg = gc3_config.idm.domains[idm_domain]
    assert service==service_cfg.name
    assert idm_domain==idm_cfg.name
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    yield service_cfg, idm_cfg


def test_oapi_spec_catalog(setup_gc30003_oapi_spec_catalog):
    service_cfg, idm_cfg = setup_gc30003_oapi_spec_catalog
    iaas_service_base = IaaSServiceBase(service_cfg=service_cfg, idm_cfg=idm_cfg)
    assert 'nimbula' in iaas_service_base.http_client.auth_cookie_header['Cookie']
    # http_future = iaas_service_base.service_operations.discover_root_instance(_request_options={"headers": {"Accept": "application/oracle-compute-v3+directory+json"}})
    # http_future = iaas_service_base.bravado_service_operations.discoverRootInstance(_request_options={"headers": {"Accept": "application/oracle-compute-v3+directory+json"}})
    http_future = iaas_service_base.service_operations.discover_root_instance()
    service_response = http_future.response()
    assert service_response.metadata.status_code==200
    assert "/Compute-" in service_response.result


def test_swagger_spec_and_spec_dict_throws():
    service = 'SecRules'
    idm_domain = 'gc30003'
    spec_file_name = 'SecRules_string_type.json'
    spec_file = spec_files_dir.joinpath(spec_file_name)
    assert spec_file.exists()
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    service_cfg = gc3_config.iaas_classic.services[service]
    idm_cfg = gc3_config.idm.domains[idm_domain]
    with spec_file.open() as fd:
        spec_dict = json.load(fp=fd)
    assert spec_dict
    http_client: IaaSRequestsHTTPClient =  IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    bravado_config = BRAVADO_CONFIG
    assert 'boolean_string' in [f.format for f in bravado_config['formats']]
    swagger_spec = Spec.from_dict(spec_dict=spec_dict, origin_url=idm_cfg.rest_endpoint, http_client=http_client, config=bravado_config)
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    assert service==service_cfg.name
    assert idm_domain==idm_cfg.name
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'

    # sec_rules = SecRules(service_cfg=service_cfg, idm_cfg=idm_cfg, spec_dict=spec_dict, swagger_spec=swagger_spec)
    with pytest.raises(RuntimeError) as e:
        sec_rules = SecRules(service_cfg=service_cfg, idm_cfg=idm_cfg, http_client=http_client, spec_dict=spec_dict, swagger_spec=swagger_spec)

