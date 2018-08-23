from pathlib import Path

from gc3_query.lib import gc3_cfg
from gc3_query.lib.gc3_config import GC3Config
from gc3_query.lib.iaas_classic.security_rules import SecurityRules
# fixme? from gc3_query.lib.open_api import API_SPECS_DIR

# from pprint import pprint, pformat

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


def test_list_security_rules_from_url():
    service = 'SecurityRules'
    idm_domain = 'gc30003'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    service_cfg = gc3_config.iaas_classic.services[service]
    idm_cfg = gc3_config.idm.domains[idm_domain]
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    assert service==service_cfg.name
    assert idm_domain==idm_cfg.name
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    security_rules = SecurityRules(service_cfg=service_cfg, idm_cfg=idm_cfg, from_url=True)
    container=security_rules.idm_container_name.replace('/', '')
    old_container=security_rules.idm_container_name
    # http_future = security_rules.bravado_service_operations.listInstance(container=security_rules.idm_user_container_name)
    # http_future = security_rules.bravado_service_operations.listInstance(container=security_rules.idm_container_name)
    # http_future = security_rules.bravado_service_operations.listSecurityRule(container=container)
    http_future = security_rules.service_operations.list_security_rule(container=container)
    # http_future = security_rules.service_operations.discover_root_instance()
    request_url = http_future.future.request.url
    service_response = http_future.response()
    result = service_response.result
    result_json = service_response.incoming_response.json()
    assert service_response.metadata.status_code==200



