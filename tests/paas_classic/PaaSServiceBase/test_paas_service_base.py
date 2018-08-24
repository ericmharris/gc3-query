import json
from pathlib import Path

import pytest
from bravado_core.spec import Spec
from bravado.response import  BravadoResponse, BravadoResponseMetadata

from gc3_query.lib import gc3_cfg
from gc3_query.lib import *
from gc3_query.lib import gc3_cfg
from gc3_query.lib.paas_classic import PaaSServiceBase
from gc3_query.lib.paas_classic.paas_requests_http_client import PaaSRequestsHTTPClient
# # fixme? from gc3_query.lib.open_api import API_SPECS_DIR

TEST_BASE_DIR: Path = Path(__file__).parent
# config_dir = TEST_BASE_DIR.joinpath("config")
config_dir = gc3_cfg.BASE_DIR.joinpath("etc/config")
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
    service = 'ServiceInstances'
    idm_domain = 'gc30003'
    service_cfg = gc3_cfg.paas_classic.services.database[service]
    idm_cfg = gc3_cfg.idm.domains[idm_domain]
    assert service==service_cfg.name
    assert idm_domain==idm_cfg.name
    assert gc3_cfg.user.cloud_username == 'eric.harris@oracle.com'
    yield service_cfg, idm_cfg


def test_init(setup_gc30003):
    service_cfg, idm_cfg = setup_gc30003
    paas_service_base = PaaSServiceBase(service_cfg=service_cfg, idm_cfg=idm_cfg)
    assert paas_service_base.http_client.skip_authentication==False
    assert paas_service_base.http_client.authenticated
    assert paas_service_base.http_client.idm_domain_name==idm_cfg.name

def test_get_rest_endpoint(setup_gc30003):
    service_cfg, idm_cfg = setup_gc30003
    paas_service_base = PaaSServiceBase(service_cfg=service_cfg, idm_cfg=idm_cfg)
    assert paas_service_base.rest_endpoint=='https://dbaas.oraclecloud.com/'
    assert paas_service_base.http_client.authenticated



def test_bravado_service_call(setup_gc30003):
    service_cfg, idm_cfg = setup_gc30003
    paas_service_base = PaaSServiceBase(service_cfg=service_cfg, idm_cfg=idm_cfg)
    assert paas_service_base.http_client.authenticated
    http_future = paas_service_base.bravado_service_operations.getDomain(identityDomainId=idm_cfg.name,
                                                                         _request_options={"headers":paas_service_base.http_client.authentication_headers})
    service_response: BravadoResponse = http_future.response()
    assert service_response
    result = service_response.result
    metadata: BravadoResponseMetadata = service_response.metadata
    assert metadata.status_code==200
    assert len(result.services) > 0




def test_service_call(setup_gc30003):
    service_cfg, idm_cfg = setup_gc30003
    paas_service_base = PaaSServiceBase(service_cfg=service_cfg, idm_cfg=idm_cfg)
    assert paas_service_base.http_client.authenticated
    http_future = paas_service_base.service_operations.get_domain(identityDomainId=idm_cfg.name)
    service_response: BravadoResponse = http_future.response()
    assert service_response
    result = service_response.result
    metadata: BravadoResponseMetadata = service_response.metadata
    assert metadata.status_code==200
    assert len(result.services) > 0








# def test_bravado_service_call(setup_gc30003):
#     service_cfg, idm_cfg = setup_gc30003
#     paas_service_base = PaaSServiceBase(service_cfg=service_cfg, idm_cfg=idm_cfg)
#     # http_future = paas_service_base.service_operations.discover_root_instance(_request_options={"headers": {"Accept": "application/oracle-compute-v3+directory+json"}})
#     # http_future = paas_service_base.bravado_service_operations.discoverRootInstance(_request_options={"headers": {"Accept": "application/oracle-compute-v3+directory+json"}})
#     http_future = paas_service_base.service_operations.discover_root_instance()
#     service_response = http_future.response()
#     assert service_response.metadata.status_code==200
#     assert "/Compute-" in service_response.result
#
#
#
# def test_pre_authenticated_http_client(setup_gc30003):
#     service_cfg, idm_cfg = setup_gc30003
#     http_client = PaaSRequestsHTTPClient(idm_cfg=idm_cfg)
#     http_client_id = id(http_client)
#     assert http_client.skip_authentication==False
#     assert http_client.idm_domain_name==idm_cfg.name
#     assert http_client.auth_cookie_header is not None
#
#     paas_service_base = PaaSServiceBase(service_cfg=service_cfg, idm_cfg=idm_cfg, http_client=http_client)
#     # http_future = paas_service_base.service_operations.discover_root_instance()
#     # http_future = paas_service_base.service_operations.discover_root_instance(_request_options={"headers": {"Accept": "application/oracle-compute-v3+directory+json"}})
#     http_future = paas_service_base.service_operations.discover_root_instance()
#     service_response = http_future.response()
#     assert service_response.metadata.status_code==200
#     assert "/Compute-" in service_response.result
#     assert id(paas_service_base.http_client)==http_client_id
#     assert paas_service_base.http_client is http_client
#
#
#
#
#
#
# @pytest.fixture()
# def setup_preauthed_gc30003():
#     service = 'ServiceInstances'
#     idm_domain = 'gc30003'
#     service_cfg = gc3_cfg.paas_classic.services.database[service]
#     idm_cfg = gc3_cfg.idm.domains[idm_domain]
#     http_client: PaaSRequestsHTTPClient = PaaSRequestsHTTPClient(idm_cfg=idm_cfg)
#     assert service==service_cfg.name
#     assert idm_domain==idm_cfg.name
#     assert gc3_cfg.user.cloud_username == 'eric.harris@oracle.com'
#     yield service_cfg, idm_cfg, http_client
#
#
# def test_get_idm_container_names(setup_preauthed_gc30003):
#     service_cfg, idm_cfg, http_client = setup_preauthed_gc30003
#     paas_service_base = PaaSServiceBase(service_cfg=service_cfg, idm_cfg=idm_cfg, http_client=http_client)
#     # http_future = paas_service_base.service_operations.discover_root_instance()
#     # http_future = paas_service_base.service_operations.discover_root_instance(_request_options={"headers": {"Accept": "application/oracle-compute-v3+directory+json"}})
#     http_future = paas_service_base.service_operations.discover_root_instance()
#     service_response = http_future.response()
#     # '/Compute-587626604/'
#     idm_container_name = service_response.incoming_response.json()['result'][0].lstrip('/').rstrip('/')
#     # '/Compute-587626604/eric.harris@oracle.com/'
#     idm_user_container_name = f"{idm_container_name}/{gc3_cfg.user.cloud_username}"
#     idm_container_name = f"{idm_container_name}"
#     idm_root_container_name = f"{idm_container_name}"
#     assert paas_service_base.idm_container_name==idm_container_name
#     assert paas_service_base.idm_user_container_name==idm_user_container_name
#     assert paas_service_base.idm_root_container_name==idm_root_container_name
#     assert paas_service_base.get_idm_user_container_name(cloud_username="foo.bar@oracle.com") == f"{idm_container_name}/foo.bar@oracle.com"
#
#
# def test_idm_root_container_name(setup_preauthed_gc30003):
#     service_cfg, idm_cfg, http_client = setup_preauthed_gc30003
#     instances = PaaSServiceBase(service_cfg=service_cfg, idm_cfg=idm_cfg, http_client=http_client)
#     idm_root_container_name = instances.idm_root_container_name
#     assert idm_root_container_name
#     expected_name = f"Compute-{idm_cfg.service_instance_id}"
#     literal_name = 'Compute-587626604'
#     assert expected_name==idm_root_container_name
#     assert literal_name==idm_root_container_name
#
#
#
# @pytest.fixture()
# def setup_gc30003_oapi_spec_catalog() -> Tuple[Dict[str, Any]]:
#     service = 'ServiceInstances'
#     idm_domain = 'gc30003'
#     service_cfg = gc3_cfg.paas_classic.services.database[service]
#     idm_cfg = gc3_cfg.idm.domains[idm_domain]
#     assert service==service_cfg.name
#     assert idm_domain==idm_cfg.name
#     assert gc3_cfg.user.cloud_username == 'eric.harris@oracle.com'
#     yield service_cfg, idm_cfg
#
#
# def test_oapi_spec_catalog(setup_gc30003_oapi_spec_catalog):
#     service_cfg, idm_cfg = setup_gc30003_oapi_spec_catalog
#     paas_service_base = PaaSServiceBase(service_cfg=service_cfg, idm_cfg=idm_cfg)
#     # http_future = paas_service_base.service_operations.discover_root_instance(_request_options={"headers": {"Accept": "application/oracle-compute-v3+directory+json"}})
#     # http_future = paas_service_base.bravado_service_operations.discoverRootInstance(_request_options={"headers": {"Accept": "application/oracle-compute-v3+directory+json"}})
#     http_future = paas_service_base.service_operations.discover_root_instance()
#     service_response = http_future.response()
#     assert service_response.metadata.status_code==200
#     assert "/Compute-" in service_response.result

#
# def test_swagger_spec_and_spec_dict_throws():
#     service = 'SecRules'
#     idm_domain = 'gc30003'
#     spec_file_name = 'SecRules_string_type.json'
#     spec_file = spec_files_dir.joinpath(spec_file_name)
#     assert spec_file.exists()
#     service_cfg = gc3_cfg.paas_classic.services.database[service]
#     idm_cfg = gc3_cfg.idm.domains[idm_domain]
#     with spec_file.open() as fd:
#         spec_dict = json.load(fp=fd)
#     assert spec_dict
#     http_client: PaaSRequestsHTTPClient =  PaaSRequestsHTTPClient(idm_cfg=idm_cfg)
#     bravado_config = gc3_cfg.
#     assert 'json_bool' in [f.format for f in bravado_config['formats']]
#     swagger_spec = Spec.from_dict(spec_dict=spec_dict, origin_url=idm_cfg.rest_endpoint, http_client=http_client, config=bravado_config)
#     # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
#     assert service==service_cfg.name
#     assert idm_domain==idm_cfg.name
#     assert gc3_cfg.user.cloud_username == 'eric.harris@oracle.com'
#
#     # sec_rules = SecRules(service_cfg=service_cfg, idm_cfg=idm_cfg, spec_dict=spec_dict, swagger_spec=swagger_spec)
#     with pytest.raises(RuntimeError) as e:
#         sec_rules = SecRules(service_cfg=service_cfg, idm_cfg=idm_cfg, http_client=http_client, spec_dict=spec_dict, swagger_spec=swagger_spec)

