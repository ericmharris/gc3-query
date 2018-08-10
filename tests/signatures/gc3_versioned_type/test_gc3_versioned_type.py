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
from gc3_query.lib.open_api.open_api_spec import OpenApiSpec
from gc3_query.lib.signatures import GC3Type, GC3VersionedType
from gc3_query.lib.iaas_classic.sec_rules import SecRules
from gc3_query.lib.iaas_classic.instances import Instances

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
    gc3type = GC3Type(name='OpenApiSpec', descr="Some text", class_type=oapi_spec.__class__)
    gc3_ver_type = GC3VersionedType(name='OpenApiSpec', descr="Some text", class_type=oapi_spec.__class__, version="18.1.2-20180126.052521")
    assert gc3type
    assert gc3_ver_type


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
    yield sec_rules, instances, idm_cfg, idm_domain, gc3_config


def test_eqality(test_equality_setup):
    sec_rules, instances, idm_cfg, idm_domain, gc3_config = test_equality_setup
    api_catalog_config = gc3_config.iaas_classic.api_catalog
    version = "18.1.2-20180126.052521"


    instances_service: str = 'Instances'
    instances_service_cfg = gc3_config.iaas_classic.services[instances_service]
    instances_oapi_spec = OpenApiSpec(api_catalog_config=api_catalog_config, service_cfg=instances_service_cfg, idm_cfg=idm_cfg)
    assert instances_oapi_spec.name == instances_service
    instances_oapi_spec_type = GC3Type(name='OpenApiSpec', descr="Some text", class_type=instances_oapi_spec.__class__)
    instances_oapi_spec_ver_type = GC3VersionedType(name='OpenApiSpec', descr="Some text", class_type=instances_oapi_spec.__class__,
                                                    version=version)
    instances_oapi_spec_type_2 = GC3Type(name='OpenApiSpec', descr="Some text", class_type=instances_oapi_spec.__class__)
    instances_oapi_spec_ver_type_2 = GC3VersionedType(name='OpenApiSpec', descr="Some text", class_type=instances_oapi_spec.__class__,
                                                    version=version)
    assert instances_oapi_spec_type==instances_oapi_spec_type
    assert instances_oapi_spec_type==instances_oapi_spec_type_2
    assert instances_oapi_spec_ver_type==instances_oapi_spec_ver_type
    assert instances_oapi_spec_ver_type==instances_oapi_spec_ver_type_2

    secrules_service: str = 'SecRules'
    secrules_service_cfg = gc3_config.iaas_classic.services[secrules_service]
    secrules_oapi_spec = OpenApiSpec(api_catalog_config=api_catalog_config, service_cfg=secrules_service_cfg, idm_cfg=idm_cfg)
    secrules_oapi_spec_2 = OpenApiSpec(api_catalog_config=api_catalog_config, service_cfg=secrules_service_cfg, idm_cfg=idm_cfg)
    assert secrules_oapi_spec.name == secrules_service
    secrules_oapi_spec_type = GC3Type(name='OpenApiSpec', descr="Some text", class_type=secrules_oapi_spec.__class__)
    secrules_oapi_spec_ver_type = GC3VersionedType(name='OpenApiSpec', descr="Some text", class_type=secrules_oapi_spec.__class__,
                                                   version=version)

    secrules_oapi_spec_type_2 = GC3Type(name='OpenApiSpec', descr="Some text", class_type=secrules_oapi_spec_2.__class__)
    secrules_oapi_spec_ver_type_2 = GC3VersionedType(name='OpenApiSpec', descr="Some text", class_type=secrules_oapi_spec.__class__,
                                                     version=version)

    assert secrules_oapi_spec_type
    assert secrules_oapi_spec_type==secrules_oapi_spec_type
    assert secrules_oapi_spec_type==secrules_oapi_spec_type_2
    assert secrules_oapi_spec_type==instances_oapi_spec_type

    assert secrules_oapi_spec_ver_type==secrules_oapi_spec_ver_type
    assert secrules_oapi_spec_ver_type==secrules_oapi_spec_ver_type_2
    assert secrules_oapi_spec_ver_type==instances_oapi_spec_ver_type



    sec_rules_type = GC3Type(name='SecRules', descr="SecRules text", class_type=sec_rules.__class__)
    sec_rules_ver_type = GC3VersionedType(name='SecRules', descr="SecRules text", class_type=sec_rules.__class__, version=version)

    instances_type = GC3Type(name='Instances', descr="Instances text", class_type=instances.__class__)
    instances_ver_type = GC3VersionedType(name='Instances', descr="Instances text", class_type=instances.__class__, version=version)

    assert sec_rules_type!=secrules_oapi_spec_type
    assert sec_rules_type!=instances_type
    assert sec_rules_ver_type!=secrules_oapi_spec_ver_type
    assert sec_rules_type!=instances_ver_type
    assert sec_rules_ver_type!=instances_ver_type



def test_gt_lt(test_equality_setup):
    sec_rules, instances, idm_cfg, idm_domain, gc3_config = test_equality_setup
    api_catalog_config = gc3_config.iaas_classic.api_catalog
    version = "18.1.2-20180126.052521"
    i_version = "18.1.2-20180126.052521"
    i_version_eq = "18.1.2-20180126.052521"
    i_version_gt_00 = "18.1.2-20180126.052521"
    i_version_gt_01 = "19.1.2-20180126.052521"
    i_version_gt_02 = "18.2.2-20180126.052521"
    i_version_gt_03 = "18.1.3-20180126.052521"
    i_version_gt_04 = "18.1.2-22180126.052521"
    i_version_gt_05 = "18.1.2-20180126.052529"

    instances_service: str = 'Instances'
    instances_service_cfg = gc3_config.iaas_classic.services[instances_service]
    instances_oapi_spec = OpenApiSpec(api_catalog_config=api_catalog_config, service_cfg=instances_service_cfg, idm_cfg=idm_cfg)
    assert instances_oapi_spec.name == instances_service
    i_ver_type = GC3VersionedType(name='OpenApiSpec', descr="Some text", class_type=instances_oapi_spec.__class__, version=version)
    i_ver_type_eq    = GC3VersionedType(name='OpenApiSpec', descr="Some text", class_type=instances_oapi_spec.__class__, version=i_version_eq)
    i_ver_type_gt_00 = GC3VersionedType(name='OpenApiSpec', descr="Some text", class_type=instances_oapi_spec.__class__, version=i_version_gt_00)
    i_ver_type_gt_01 = GC3VersionedType(name='OpenApiSpec', descr="Some text", class_type=instances_oapi_spec.__class__, version=i_version_gt_01)
    i_ver_type_gt_02 = GC3VersionedType(name='OpenApiSpec', descr="Some text", class_type=instances_oapi_spec.__class__, version=i_version_gt_02)
    i_ver_type_gt_03 = GC3VersionedType(name='OpenApiSpec', descr="Some text", class_type=instances_oapi_spec.__class__, version=i_version_gt_03)
    i_ver_type_gt_04 = GC3VersionedType(name='OpenApiSpec', descr="Some text", class_type=instances_oapi_spec.__class__, version=i_version_gt_04)
    i_ver_type_gt_05 = GC3VersionedType(name='OpenApiSpec', descr="Some text", class_type=instances_oapi_spec.__class__, version=i_version_gt_05)

    assert i_ver_type == i_ver_type_eq
    assert i_ver_type == i_ver_type_gt_00
    assert i_ver_type < i_ver_type_gt_01
    assert i_ver_type < i_ver_type_gt_02
    assert i_ver_type < i_ver_type_gt_03
    assert i_ver_type < i_ver_type_gt_04
    assert i_ver_type < i_ver_type_gt_05

