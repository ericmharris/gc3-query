from pathlib import Path

import pytest

from gc3_query.lib import *
from gc3_query.lib.gc3_config import GC3Config
from gc3_query.lib.iaas_classic.instances import Instances
from gc3_query.lib.iaas_classic.sec_rules import SecRules
from gc3_query.lib.open_api.open_api_spec import OpenApiSpec
from gc3_query.lib.base_collections import NestedOrderedDictAttrListBase

BASE_DIR = gc3_cfg.BASE_DIR

TEST_BASE_DIR: Path = Path(__file__).parent
# config_dir = TEST_BASE_DIR.joinpath("config")
config_dir = gc3_cfg.BASE_DIR.joinpath("etc/config")
output_dir = TEST_BASE_DIR.joinpath('output')
spec_files_dir = TEST_BASE_DIR.joinpath('spec_files')


def test_setup():
    assert TEST_BASE_DIR.exists()
    assert gc3_cfg.OPEN_API_CATALOG_DIR.exists()
    assert gc3_cfg.OPEN_API_SPEC_BASE.exists()
    if not config_dir.exists():
        config_dir.mkdir()
    if not output_dir.exists():
        output_dir.mkdir()
    if not spec_files_dir.exists():
        spec_files_dir.mkdir()


def test_init():
    service = 'Instances'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    open_api_specs_cfg = gc3_config.iaas_classic.open_api_specs
    idm_cfg = gc3_config.idm.domains.gc30003
    # oapi_spec = OpenApiSpec(service_cfg=service_cfg, open_api_specs_cfg=api_catalog_config)
    oapi_spec = OpenApiSpec(service_cfg=service_cfg, open_api_specs_cfg=open_api_specs_cfg, idm_cfg=idm_cfg)
    assert oapi_spec.name == service

def test_build():
    service = 'Instances'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    open_api_specs_cfg = gc3_config.iaas_classic.open_api_specs
    idm_cfg = gc3_config.idm.domains.gc30003
    # oapi_spec = OpenApiSpec(service_cfg=service_cfg, open_api_specs_cfg=api_catalog_config)
    oapi_spec = OpenApiSpec(service_cfg=service_cfg, open_api_specs_cfg=open_api_specs_cfg, idm_cfg=idm_cfg)
    assert oapi_spec.name == service
    is_built = oapi_spec.build()
    assert is_built

def test_validate():
    service = 'Instances'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    open_api_specs_cfg = gc3_config.iaas_classic.open_api_specs
    idm_cfg = gc3_config.idm.domains.gc30003
    # oapi_spec = OpenApiSpec(service_cfg=service_cfg, open_api_specs_cfg=api_catalog_config)
    oapi_spec = OpenApiSpec(service_cfg=service_cfg, open_api_specs_cfg=open_api_specs_cfg, idm_cfg=idm_cfg)
    assert oapi_spec.name == service
    is_valid = oapi_spec.validate()
    assert is_valid

def test_str_repr():
    service = 'Instances'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    open_api_specs_cfg = gc3_config.iaas_classic.open_api_specs
    idm_cfg = gc3_config.idm.domains.gc30003
    oapi_spec = OpenApiSpec(service_cfg=service_cfg, open_api_specs_cfg=open_api_specs_cfg, idm_cfg=idm_cfg)
    s = str(oapi_spec)
    r = repr(oapi_spec)
    assert s
    assert r
    assert s==r
    assert service in s
    assert 'OpenApiSpec' in r

def test_init_properties():
    idm_domain = 'gc30003'
    service = 'Instances'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    idm_cfg = gc3_config.idm.domains[idm_domain]
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    open_api_specs_cfg = gc3_config.iaas_classic.open_api_specs
    api_catalog_config = gc3_config.iaas_classic.open_api_spec_catalog
    oapi_spec = OpenApiSpec(service_cfg=service_cfg, open_api_specs_cfg=open_api_specs_cfg, idm_cfg=idm_cfg)
    assert oapi_spec.name == service
    assert oapi_spec._spec_data['schemes'] == ['https']
    assert oapi_spec.spec_file.exists()
    assert oapi_spec.spec_file.suffix=='.yaml'
    assert oapi_spec.spec_export_dir.exists()
    assert isinstance(oapi_spec._spec_dict, dict)
    assert isinstance(oapi_spec._spec_data, NestedOrderedDictAttrListBase)



def test_get_spec():
    idm_domain = 'gc30003'
    service = 'Instances'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    idm_cfg = gc3_config.idm.domains[idm_domain]
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    open_api_specs_cfg = gc3_config.iaas_classic.open_api_specs
    api_catalog_config = gc3_config.iaas_classic.open_api_spec_catalog
    oapi_spec = OpenApiSpec(service_cfg=service_cfg, open_api_specs_cfg=open_api_specs_cfg, idm_cfg=idm_cfg)
    assert oapi_spec.name == service
    assert oapi_spec._spec_data['schemes'] == ['https']
    bravado_core_spec = oapi_spec.get_swagger_spec(rest_endpoint=idm_cfg.rest_endpoint)
    assert bravado_core_spec.origin_url == idm_cfg.rest_endpoint
    # assert bravado_core_spec.spec_dict['info']['title'] == service
    assert bravado_core_spec.spec_dict['info']['title'] == service_cfg.title


def test_get_spec_from_kwargs():
    idm_domain = 'gc30003'
    service = 'Instances'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    idm_cfg = gc3_config.idm.domains[idm_domain]
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    open_api_specs_cfg = gc3_config.iaas_classic.open_api_specs
    api_catalog_config = gc3_config.iaas_classic.open_api_spec_catalog
    # oapi_spec = OpenApiSpec(service_cfg=service_cfg, open_api_specs_cfg=api_catalog_config, rest_endpoint=idm_cfg.rest_endpoint)
    oapi_spec = OpenApiSpec(service_cfg=service_cfg, open_api_specs_cfg=open_api_specs_cfg, idm_cfg=idm_cfg, rest_endpoint=idm_cfg.rest_endpoint)
    assert oapi_spec.name == service
    assert oapi_spec._spec_data['schemes'] == ['https']
    bravado_core_spec = oapi_spec.get_swagger_spec()
    assert bravado_core_spec.origin_url == idm_cfg.rest_endpoint
    assert oapi_spec.rest_endpoint == idm_cfg.rest_endpoint

#
# def test_from_url():
#     idm_domain = 'gc30003'
#     service = 'Instances'
#     gc3_config = GC3Config(atoml_config_dir=config_dir)
#     idm_cfg = gc3_config.idm.domains[idm_domain]
#     service_cfg = gc3_config.iaas_classic.services.compute[service]
#     open_api_specs_cfg = gc3_config.iaas_classic.open_api_specs
#     api_catalog_config = gc3_config.iaas_classic.open_api_spec_catalog
#     oapi_spec = OpenApiSpec(service_cfg=service_cfg, open_api_specs_cfg=open_api_specs_cfg, idm_cfg=idm_cfg)
#     assert oapi_spec.name == service
#     assert oapi_spec._spec_data['schemes'] == ['https']
#     assert oapi_spec.from_url == True
#
#     bravado_core_spec = oapi_spec.get_swagger_spec(rest_endpoint=idm_cfg.rest_endpoint)
#     assert bravado_core_spec.origin_url == idm_cfg.rest_endpoint
#     assert bravado_core_spec.spec_dict['info']['title'] == service


def test_check_spec_properties():
    idm_domain = 'gc30003'
    service: str = 'Instances'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    idm_cfg = gc3_config.idm.domains[idm_domain]
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    open_api_specs_cfg = gc3_config.iaas_classic.open_api_specs
    oapi_spec = OpenApiSpec(service_cfg=service_cfg, open_api_specs_cfg=open_api_specs_cfg, idm_cfg=idm_cfg)
    assert oapi_spec.name == service
    assert oapi_spec._spec_data['schemes'] == ['https']
    assert oapi_spec.title == service_cfg.title
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




def test_get_paas_spec():
    idm_domain = 'gc30003'
    service = 'ServiceInstances'
    paas_type = 'database'
    service_cfg = gc3_cfg.paas_classic.services.get(paas_type)[service]
    idm_cfg = gc3_cfg.idm.domains[idm_domain]
    open_api_specs_cfg = gc3_cfg.paas_classic.open_api_specs
    oapi_spec = OpenApiSpec(service_cfg=service_cfg, open_api_specs_cfg=open_api_specs_cfg, idm_cfg=idm_cfg)
    assert oapi_spec.name == service
    assert oapi_spec._spec_data['schemes'] == ['https']
    bravado_core_spec = oapi_spec.get_swagger_spec(rest_endpoint=idm_cfg.rest_endpoint)
    assert bravado_core_spec.origin_url == idm_cfg.rest_endpoint
    assert bravado_core_spec.spec_dict['info']['title'] == service_cfg.title



def test_paas_rest_endpoint_dbcs():
    idm_domain = 'gc30003'
    service = 'ServiceInstances'
    paas_type = 'database'
    service_cfg = gc3_cfg.paas_classic.services.get(paas_type)[service]
    idm_cfg = gc3_cfg.idm.domains[idm_domain]
    open_api_specs_cfg = gc3_cfg.paas_classic.open_api_specs
    oapi_spec = OpenApiSpec(service_cfg=service_cfg, open_api_specs_cfg=open_api_specs_cfg, idm_cfg=idm_cfg)
    assert oapi_spec.name == service
    assert oapi_spec._spec_data['schemes'] == ['https']
    bravado_core_spec = oapi_spec.get_swagger_spec(rest_endpoint=idm_cfg.rest_endpoint)
    assert oapi_spec.rest_endpoint=='https://dbaas.oraclecloud.com/'
    assert oapi_spec._spec_data['schemes'] == ['https']
    assert oapi_spec.spec_dict['schemes'] == ['https']
    assert oapi_spec.spec_dict['host'] == 'dbaas.oraclecloud.com'


def test_paas_rest_endpoint_jaas():
    idm_domain = 'gc30003'
    service = 'ServiceInstances'
    paas_type = 'java'
    service_cfg = gc3_cfg.paas_classic.services.get(paas_type)[service]
    idm_cfg = gc3_cfg.idm.domains[idm_domain]
    open_api_specs_cfg = gc3_cfg.paas_classic.open_api_specs
    oapi_spec = OpenApiSpec(service_cfg=service_cfg, open_api_specs_cfg=open_api_specs_cfg, idm_cfg=idm_cfg)
    assert oapi_spec.name == service
    assert oapi_spec._spec_data['schemes'] == ['https']
    bravado_core_spec = oapi_spec.get_swagger_spec(rest_endpoint=idm_cfg.rest_endpoint)
    assert oapi_spec.rest_endpoint=='https://jaas.oraclecloud.com/'
    assert oapi_spec._spec_data['schemes'] == ['https']
    assert oapi_spec.spec_dict['host'] == 'jaas.oraclecloud.com'


def test_get_rest_endpoint_iaas():
    idm_domain = 'gc30003'
    service: str = 'Instances'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    idm_cfg = gc3_config.idm.domains[idm_domain]
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    open_api_specs_cfg = gc3_config.iaas_classic.open_api_specs
    oapi_spec = OpenApiSpec(service_cfg=service_cfg, open_api_specs_cfg=open_api_specs_cfg, idm_cfg=idm_cfg)
    assert oapi_spec.name == service
    assert oapi_spec._spec_data['schemes'] == ['https']
    assert oapi_spec.rest_endpoint=='https://compute.uscom-central-1.oraclecloud.com'
    assert oapi_spec.title == service_cfg.title
    assert oapi_spec.spec_dict['host'] == 'compute.uscom-central-1.oraclecloud.com'






# @pytest.fixture()
# def test_equality_setup():
#     idm_domain = 'gc30003'
#     gc3_config = GC3Config(atoml_config_dir=config_dir)
#     idm_cfg = gc3_config.idm.domains[idm_domain]
#     api_catalog_config = gc3_config.iaas_classic.open_api_spec_catalog
#
#     instances_service: str = 'Instances'
#     instances_service_cfg = gc3_config.iaas_classic.services[instances_service]
#     instances_oapi_spec = OpenApiSpec(service_cfg=instances_service_cfg, open_api_specs_cfg=api_catalog_config, idm_cfg=idm_cfg)
#     open_api_specs_cfg = gc3_config.iaas_classic.open_api_specs
#     assert instances_oapi_spec.name == instances_service
#
#     secrules_service: str = 'SecRules'
#     secrules_service_cfg = gc3_config.iaas_classic.services[secrules_service]
#
#     sec_rules = SecRules(service_cfg=secrules_service_cfg, idm_cfg=idm_cfg, from_url=True)
#     instances = Instances(service_cfg=instances_service_cfg, idm_cfg=idm_cfg, from_url=True)
#     yield sec_rules, instances, idm_cfg, idm_domain
#
#
# def test_equality(test_equality_setup):
#     sec_rules, instances, idm_cfg, idm_domain = test_equality_setup
#     idm_domain = 'gc30003'
#
#     instances_service: str = 'Instances'
#     gc3_config = GC3Config(atoml_config_dir=config_dir)
#     idm_cfg = gc3_config.idm.domains[idm_domain]
#     instances_service_cfg = gc3_config.iaas_classic.services[instances_service]
#     api_catalog_config = gc3_config.iaas_classic.open_api_spec_catalog
#     instances_oapi_spec = OpenApiSpec(service_cfg=instances_service_cfg, open_api_specs_cfg=api_catalog_config, idm_cfg=idm_cfg)
#     instances_oapi_spec_2 = OpenApiSpec(service_cfg=instances_service_cfg, open_api_specs_cfg=api_catalog_config, idm_cfg=idm_cfg)
#     assert instances_oapi_spec.name == instances_service
#     assert instances_oapi_spec._spec_data['schemes'] == ['https']
#     assert instances_oapi_spec.title == instances_service
#
#     secrules_service: str = 'SecRules'
#     gc3_config = GC3Config(atoml_config_dir=config_dir)
#     idm_cfg = gc3_config.idm.domains[idm_domain]
#     sec_rules_service_cfg = gc3_config.iaas_classic.services[secrules_service]
#     api_catalog_config = gc3_config.iaas_classic.open_api_spec_catalog
#     sec_rules_oapi_spec = OpenApiSpec(service_cfg=sec_rules_service_cfg, open_api_specs_cfg=api_catalog_config, idm_cfg=idm_cfg)
#     assert sec_rules_oapi_spec.name == secrules_service
#     assert sec_rules_oapi_spec._spec_data['schemes'] == ['https']
#     assert sec_rules_oapi_spec.title == secrules_service
#
#     assert instances_oapi_spec == instances_oapi_spec_2
#     assert sec_rules_oapi_spec != instances_oapi_spec
#     assert sec_rules_oapi_spec != instances_oapi_spec_2
#
#
# def test_export():
#     idm_domain = 'gc30003'
#     service = 'Instances'
#     gc3_config = GC3Config(atoml_config_dir=config_dir)
#     idm_cfg = gc3_config.idm.domains[idm_domain]
#     service_cfg = gc3_config.iaas_classic.services.compute[service]
#     api_catalog_config = gc3_config.iaas_classic.open_api_spec_catalog
#     oapi_spec = OpenApiSpec(service_cfg=service_cfg, open_api_specs_cfg=open_api_specs_cfg, idm_cfg=idm_cfg)
#     assert oapi_spec.name == service
#     assert oapi_spec._spec_data['schemes'] == ['https']
#     bravado_core_spec = oapi_spec.get_swagger_spec(rest_endpoint=idm_cfg.rest_endpoint)
#     exported_file_paths = oapi_spec.export()
#     for exported_file_path in exported_file_paths:
#         assert exported_file_path.exists()
#

