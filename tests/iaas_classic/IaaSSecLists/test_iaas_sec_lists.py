from pathlib import Path

import pytest

from gc3_query.lib import gc3_cfg
from gc3_query.lib.gc3_config import GC3Config
from gc3_query.lib.iaas_classic.sec_lists import SecLists
# fixme? from gc3_query.lib.open_api import API_SPECS_DIR

# from pprint import pprint, pformat

TEST_BASE_DIR: Path = Path(__file__).parent
# config_dir = TEST_BASE_DIR.joinpath("config")
config_dir = gc3_cfg.BASE_DIR.joinpath("etc/config")
output_dir = TEST_BASE_DIR.joinpath('output')
spec_files_dir = TEST_BASE_DIR.joinpath('spec_files')


def test_setup():
    assert TEST_BASE_DIR.exists()
    # assert API_SPECS_DIR.exists()
    if not config_dir.exists():
        config_dir.mkdir()
    if not output_dir.exists():
        output_dir.mkdir()
    if not spec_files_dir.exists():
        spec_files_dir.mkdir()

def test_init():
    service = 'SecLists'
    idm_domain = 'gc30003'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    idm_cfg = gc3_config.idm.domains[idm_domain]
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    assert service==service_cfg.name
    assert idm_domain==idm_cfg.name
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    sec_lists = SecLists(service_cfg=service_cfg, idm_cfg=idm_cfg, from_url=True)
    assert sec_lists.name==service


@pytest.fixture()
def setup_gc30003_dump():
    service = 'SecLists'
    idm_domain = 'gc30003'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    idm_cfg = gc3_config.idm.domains[idm_domain]
    iaas_service = SecLists(service_cfg=service_cfg, idm_cfg=idm_cfg)
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



#
#
# def test_overlays_applied():
#     service = 'SecLists'
#     idm_domain = 'gc30003'
#     gc3_config = GC3Config(atoml_config_dir=config_dir)
#     service_cfg = gc3_config.iaas_classic.services.compute[service]
#     idm_cfg = gc3_config.idm.domains[idm_domain]
#     # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
#     assert service==service_cfg.name
#     assert idm_domain==idm_cfg.name
#     assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
#     sec_lists = SecLists(service_cfg=service_cfg, idm_cfg=idm_cfg)
#     # container=sec_lists.idm_container_name.replace('/', '')
#     container=sec_lists.idm_root_container_name
#     old_container=sec_lists.idm_container_name
#     # http_future = sec_lists.bravado_service_operations.listInstance(container=sec_lists.idm_user_container_name)
#     # http_future = sec_lists.bravado_service_operations.listInstance(container=sec_lists.idm_container_name)
#     # http_future = sec_lists.bravado_service_operations.listSecRule(container=container)
#     http_future = sec_lists.service_operations.list_sec_rule(container=container)
#     # http_future = sec_lists.service_operations.discover_root_instance()
#     request_url = http_future.future.request.url
#     service_response = http_future.response()
#     result = service_response.result
#     result_json = service_response.incoming_response.json()
#     assert service_response.metadata.status_code==200
#     assert len(result_json['result']) > 0
#     assert 'src_list' in result_json['result'][0]
#     assert isinstance(result_json['result'][0]['dst_is_ip'], bool)
#
#
#
# def test_get_all_sec_lists_data_types_correct():
#     service = 'SecLists'
#     idm_domain = 'gc30003'
#     gc3_config = GC3Config(atoml_config_dir=config_dir)
#     service_cfg = gc3_config.iaas_classic.services.compute[service]
#     idm_cfg = gc3_config.idm.domains[idm_domain]
#     # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
#     assert service==service_cfg.name
#     assert idm_domain==idm_cfg.name
#     assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
#     sec_lists = SecLists(service_cfg=service_cfg, idm_cfg=idm_cfg)
#     result_json = sec_lists.get_all_sec_lists()
#     assert len(result_json['result']) > 0
#     assert 'src_list' in result_json['result'][0]
#     assert isinstance(result_json['result'][0]['dst_is_ip'], bool)
#
#
# def test_get_all_sec_lists():
#     service = 'SecLists'
#     idm_domain = 'gc30003'
#     spec_file_name = 'SecLists_string_type.json'
#     spec_file = spec_files_dir.joinpath(spec_file_name)
#     assert spec_file.exists()
#     gc3_config = GC3Config(atoml_config_dir=config_dir)
#     service_cfg = gc3_config.iaas_classic.services.compute[service]
#     idm_cfg = gc3_config.idm.domains[idm_domain]
#     with spec_file.open() as fd:
#         spec_dict = json.load(fp=fd)
#     assert spec_dict
#     bravado_config = BRAVADO_CONFIG
#     assert 'json_bool' in [f.format for f in bravado_config['formats']]
#     swagger_spec = Spec.from_dict(spec_dict=spec_dict, origin_url=idm_cfg.rest_endpoint, config=bravado_config)
#     # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
#     assert service==service_cfg.name
#     assert idm_domain==idm_cfg.name
#     assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
#     sec_lists = SecLists(service_cfg=service_cfg, idm_cfg=idm_cfg, spec_dict=spec_dict, swagger_spec=swagger_spec)
#     assert 'json_bool' in [f.format for f in sec_lists.bravado_config['formats']]
#     result_json = sec_lists.get_all_sec_lists()
#     assert len(result_json['result']) > 0
#     assert 'src_list' in result_json['result'][0]

