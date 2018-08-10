import pytest
import toml
from pathlib import Path
# from pprint import pprint, pformat
from prettyprinter import pprint, pformat

from gc3_query.lib import *
from gc3_query.lib import BASE_DIR, OPEN_API_CATALOG_DIR

from gc3_query.lib.gc3_config import GC3Config, IDMCredential
from gc3_query.lib.iaas_classic.iaas_requests_http_client import IaaSRequestsHTTPClient
from gc3_query.lib.iaas_classic import IaaSServiceBase, API_SPECS_DIR, IaaSRequestsHTTPClient
from gc3_query.lib.iaas_classic.instances import Instances
from gc3_query.lib.iaas_classic.sec_rules import SecRules
from gc3_query.lib.open_api.open_api_spec import OpenApiSpec

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



def test_init():
    service = 'Instances'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    service_cfg = gc3_config.iaas_classic.services[service]
    api_catalog_config = gc3_config.iaas_classic.api_catalog
    oapi_spec = OpenApiSpec(api_catalog_config=api_catalog_config, service_cfg=service_cfg)
    assert oapi_spec.name == service


def test_schemes_updated():
    idm_domain = 'gc30003'
    service = 'Instances'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    idm_cfg = gc3_config.idm.domains[idm_domain]
    service_cfg = gc3_config.iaas_classic.services[service]
    api_catalog_config = gc3_config.iaas_classic.api_catalog
    oapi_spec = OpenApiSpec(api_catalog_config=api_catalog_config, service_cfg=service_cfg)
    assert oapi_spec.name == service
    assert oapi_spec.api_spec['schemes'] == ['https']


def test_get_spec():
    idm_domain = 'gc30003'
    service = 'Instances'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    idm_cfg = gc3_config.idm.domains[idm_domain]
    service_cfg = gc3_config.iaas_classic.services[service]
    api_catalog_config = gc3_config.iaas_classic.api_catalog
    oapi_spec = OpenApiSpec(api_catalog_config=api_catalog_config, service_cfg=service_cfg)
    assert oapi_spec.name == service
    assert oapi_spec.api_spec['schemes'] == ['https']
    core_spec = oapi_spec.get_spec(rest_endpoint=idm_cfg.rest_endpoint)
    assert core_spec.origin_url==idm_cfg.rest_endpoint
    assert core_spec.spec_dict['info']['title']==service

def test_get_spec_from_kwargs():
    idm_domain = 'gc30003'
    service = 'Instances'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    idm_cfg = gc3_config.idm.domains[idm_domain]
    service_cfg = gc3_config.iaas_classic.services[service]
    api_catalog_config = gc3_config.iaas_classic.api_catalog
    oapi_spec = OpenApiSpec(api_catalog_config=api_catalog_config, service_cfg=service_cfg, rest_endpoint=idm_cfg.rest_endpoint)
    assert oapi_spec.name == service
    assert oapi_spec.api_spec['schemes'] == ['https']
    core_spec = oapi_spec.get_spec()
    assert core_spec.origin_url==idm_cfg.rest_endpoint
    assert oapi_spec.rest_endpoint==idm_cfg.rest_endpoint

def test_from_url():
    idm_domain = 'gc30003'
    service = 'Instances'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    idm_cfg = gc3_config.idm.domains[idm_domain]
    service_cfg = gc3_config.iaas_classic.services[service]
    api_catalog_config = gc3_config.iaas_classic.api_catalog
    oapi_spec = OpenApiSpec(api_catalog_config=api_catalog_config, service_cfg=service_cfg, from_url=True)
    assert oapi_spec.name == service
    assert oapi_spec.api_spec['schemes'] == ['https']
    assert oapi_spec.from_url==True

    core_spec = oapi_spec.get_spec(rest_endpoint=idm_cfg.rest_endpoint)
    assert core_spec.origin_url==idm_cfg.rest_endpoint
    assert core_spec.spec_dict['info']['title']==service

def test_check_spec_properties():
    idm_domain = 'gc30003'
    service: str = 'Instances'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    idm_cfg = gc3_config.idm.domains[idm_domain]
    service_cfg = gc3_config.iaas_classic.services[service]
    api_catalog_config = gc3_config.iaas_classic.api_catalog
    oapi_spec = OpenApiSpec(api_catalog_config=api_catalog_config, service_cfg=service_cfg, idm_cfg=idm_cfg)
    assert oapi_spec.name == service
    assert oapi_spec.api_spec['schemes'] == ['https']
    assert oapi_spec.title==service
    version_tupple = oapi_spec.version.split('.')
    assert version_tupple[0].isnumeric()
    assert service.lower() in oapi_spec.description
    service_paths = oapi_spec.paths
    in_paths = ['instance' in p for p in service_paths]
    assert all(in_paths)
    operation_ids = oapi_spec.operation_ids
    assert len(operation_ids) > 0
    assert 'discoverInstance' in operation_ids
    assert 'deleteInstance' in operation_ids
    operation_id_descrs = oapi_spec.operation_id_descrs
    assert operation_id_descrs
    assert 'deleteInstance' in operation_id_descrs




@pytest.fixture()
def test_equality_setup():
    idm_domain = 'gc30003'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    idm_cfg = gc3_config.idm.domains[idm_domain]
    api_catalog_config = gc3_config.iaas_classic.api_catalog

    instances_service: str = 'Instances'
    instances_service_cfg = gc3_config.iaas_classic.services[instances_service]
    instances_oapi_spec = OpenApiSpec(api_catalog_config=api_catalog_config, service_cfg=instances_service_cfg, idm_cfg=idm_cfg)
    assert instances_oapi_spec.name == instances_service

    secrules_service: str = 'SecRules'
    secrules_service_cfg = gc3_config.iaas_classic.services[secrules_service]

    sec_rules = SecRules(service_cfg=secrules_service_cfg, idm_cfg=idm_cfg, from_url=True)
    instances = Instances(service_cfg=instances_service_cfg, idm_cfg=idm_cfg, from_url=True)
    yield sec_rules, instances, idm_cfg, idm_domain

def test_equality(test_equality_setup):
    sec_rules, instances, idm_cfg, idm_domain = test_equality_setup
    idm_domain = 'gc30003'

    instances_service: str = 'Instances'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    idm_cfg = gc3_config.idm.domains[idm_domain]
    service_cfg = gc3_config.iaas_classic.services[instances_service]
    api_catalog_config = gc3_config.iaas_classic.api_catalog
    instances_oapi_spec = OpenApiSpec(api_catalog_config=api_catalog_config, service_cfg=service_cfg, idm_cfg=idm_cfg)
    assert instances_oapi_spec.name == instances_service
    assert instances_oapi_spec.api_spec['schemes'] == ['https']
    assert instances_oapi_spec.title==instances_service

    secrules_service: str = 'SecRules'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    idm_cfg = gc3_config.idm.domains[idm_domain]
    service_cfg = gc3_config.iaas_classic.services[secrules_service]
    api_catalog_config = gc3_config.iaas_classic.api_catalog
    instances_oapi_spec = OpenApiSpec(api_catalog_config=api_catalog_config, service_cfg=service_cfg, idm_cfg=idm_cfg)
    assert instances_oapi_spec.name == secrules_service
    assert instances_oapi_spec.api_spec['schemes'] == ['https']
    assert instances_oapi_spec.title==secrules_service
