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
from gc3_query.lib.iaas_classic.sec_rules import SecRules

TEST_BASE_DIR: Path = Path(__file__).parent
# config_dir = TEST_BASE_DIR.joinpath("config")
config_dir = BASE_DIR.joinpath("etc/config")
output_dir = TEST_BASE_DIR.joinpath('output')


def test_setup():
    assert TEST_BASE_DIR.exists()
    assert API_SPECS_DIR.exists()
    if not config_dir.exists():
        config_dir.mkdir()
    if not output_dir.exists():
        output_dir.mkdir()

def test_list_sec_rules_from_url():
    service = 'SecRules'
    idm_domain = 'gc30003'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    service_cfg = gc3_config.iaas_classic.services[service]
    idm_cfg = gc3_config.idm.domains[idm_domain]
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    assert service==service_cfg.name
    assert idm_domain==idm_cfg.name
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    sec_rules = SecRules(service_cfg=service_cfg, idm_cfg=idm_cfg, from_url=True)
    # container=sec_rules.idm_container_name.replace('/', '')
    container=sec_rules.idm_root_container_name
    old_container=sec_rules.idm_container_name
    # http_future = sec_rules.bravado_service_operations.listInstance(container=sec_rules.idm_user_container_name)
    # http_future = sec_rules.bravado_service_operations.listInstance(container=sec_rules.idm_container_name)
    # http_future = sec_rules.bravado_service_operations.listSecRule(container=container)
    http_future = sec_rules.service_operations.list_sec_rule(container=container)
    # http_future = sec_rules.service_operations.discover_root_instance()
    request_url = http_future.future.request.url
    service_response = http_future.response()
    result = service_response.result
    result_json = service_response.incoming_response.json()
    assert service_response.metadata.status_code==200
    assert len(result_json['result']) > 0
    assert 'src_list' in result_json['result'][0]


def test_overlays_applied():
    service = 'SecRules'
    idm_domain = 'gc30003'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    service_cfg = gc3_config.iaas_classic.services[service]
    idm_cfg = gc3_config.idm.domains[idm_domain]
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    assert service==service_cfg.name
    assert idm_domain==idm_cfg.name
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    sec_rules = SecRules(service_cfg=service_cfg, idm_cfg=idm_cfg)
    # container=sec_rules.idm_container_name.replace('/', '')
    container=sec_rules.idm_root_container_name
    old_container=sec_rules.idm_container_name
    # http_future = sec_rules.bravado_service_operations.listInstance(container=sec_rules.idm_user_container_name)
    # http_future = sec_rules.bravado_service_operations.listInstance(container=sec_rules.idm_container_name)
    # http_future = sec_rules.bravado_service_operations.listSecRule(container=container)
    http_future = sec_rules.service_operations.list_sec_rule(container=container)
    # http_future = sec_rules.service_operations.discover_root_instance()
    request_url = http_future.future.request.url
    service_response = http_future.response()
    result = service_response.result
    result_json = service_response.incoming_response.json()
    assert service_response.metadata.status_code==200
    assert len(result_json['result']) > 0
    assert 'src_list' in result_json['result'][0]
    assert isinstance(result_json['result'][0]['dst_is_ip'], bool)


