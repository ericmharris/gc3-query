import json
from pathlib import Path

import pytest
from bravado_core.spec import Spec
from bravado.response import  BravadoResponse, BravadoResponseMetadata

from gc3_query.lib import gc3_cfg
from gc3_query.lib import *
from gc3_query.lib import gc3_cfg
from gc3_query.lib.paas_classic import PaaSServiceBase
from gc3_query.lib.paas_classic.database_service_instances import DatabaseServiceInstances
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
    paas_type = 'database'
    service_cfg = gc3_cfg.paas_classic.services.get(paas_type)[service]
    idm_cfg = gc3_cfg.idm.domains[idm_domain]
    assert service==service_cfg.name
    assert idm_domain==idm_cfg.name
    assert gc3_cfg.user.cloud_username == 'eric.harris@oracle.com'
    yield service_cfg, idm_cfg


def test_init(setup_gc30003):
    service_cfg, idm_cfg = setup_gc30003
    dbcs_service_instances: DatabaseServiceInstances = DatabaseServiceInstances(service_cfg=service_cfg, idm_cfg=idm_cfg)
    assert dbcs_service_instances.http_client.skip_authentication==False
    assert dbcs_service_instances.http_client.authenticated
    assert dbcs_service_instances.http_client.idm_domain_name==idm_cfg.name

def test_get_rest_endpoint(setup_gc30003):
    service_cfg, idm_cfg = setup_gc30003
    dbcs_service_instances: DatabaseServiceInstances = DatabaseServiceInstances(service_cfg=service_cfg, idm_cfg=idm_cfg)
    assert dbcs_service_instances.rest_endpoint=='https://dbaas.oraclecloud.com/'
    assert dbcs_service_instances.http_client.authenticated



def test_bravado_service_call(setup_gc30003):
    service_cfg, idm_cfg = setup_gc30003
    dbcs_service_instances: DatabaseServiceInstances = DatabaseServiceInstances(service_cfg=service_cfg, idm_cfg=idm_cfg)
    assert dbcs_service_instances.http_client.authenticated
    http_future = dbcs_service_instances.bravado_service_operations.getDomain(identityDomainId=idm_cfg.name,
                                                                         _request_options={"headers":dbcs_service_instances.http_client.authentication_headers})
    service_response: BravadoResponse = http_future.response()
    assert service_response
    result = service_response.result
    metadata: BravadoResponseMetadata = service_response.metadata
    assert metadata.status_code==200
    assert len(result.services) > 0

def test_service_call(setup_gc30003):
    service_cfg, idm_cfg = setup_gc30003
    dbcs_service_instances = DatabaseServiceInstances(service_cfg=service_cfg, idm_cfg=idm_cfg)
    assert dbcs_service_instances.http_client.authenticated
    http_future = dbcs_service_instances.service_operations.get_domain(identityDomainId=idm_cfg.name)
    service_response: BravadoResponse = http_future.response()
    assert service_response
    result = service_response.result
    metadata: BravadoResponseMetadata = service_response.metadata
    assert metadata.status_code==200
    assert len(result.services) > 0



def test_get_all_domain_data(setup_gc30003):
    service_cfg, idm_cfg = setup_gc30003
    dbcs_service_instances: DatabaseServiceInstances = DatabaseServiceInstances(service_cfg=service_cfg, idm_cfg=idm_cfg)
    assert dbcs_service_instances.http_client.authenticated
    pass_service_response = dbcs_service_instances.get_all_domain_data()
    assert len(pass_service_response) > 0
    db_data = pass_service_response.results[0]
    assert db_data
    assert 'identity_domain' in db_data
    assert db_data['identity_domain']==idm_cfg.name






