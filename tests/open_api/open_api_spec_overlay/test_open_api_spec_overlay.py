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
from gc3_query.lib.open_api.open_api_spec_overlay import OpenApiSpecOverlay

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
    idm_domain = 'gc30003'
    service = 'Instances'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    idm_cfg = gc3_config.idm.domains[idm_domain]
    service_cfg = gc3_config.iaas_classic.services[service]
    api_catalog_config = gc3_config.iaas_classic.open_api_spec_catalog
    oapi_spec = OpenApiSpec(api_catalog_config=api_catalog_config, service_cfg=service_cfg, from_url=True)
    oapi_spec_overlay = OpenApiSpecOverlay(open_api_spec=oapi_spec)
    assert oapi_spec.name == service
    assert oapi_spec_overlay.name == service
    assert 'schemes' in oapi_spec_overlay.overlays

# def test_save_spec_overlay_to_catalog():
#     idm_domain = 'gc30003'
#     service = 'Instances'
#     gc3_config = GC3Config(atoml_config_dir=config_dir)
#     idm_cfg = gc3_config.idm.domains[idm_domain]
#     service_cfg = gc3_config.iaas_classic.services[service]
#     api_catalog_config = gc3_config.iaas_classic.open_api_spec_catalog
#     oapi_spec = OpenApiSpec(api_catalog_config=api_catalog_config, service_cfg=service_cfg, from_url=True)
#     assert oapi_spec.name == service
#     assert oapi_spec.api_spec['schemes'] == ['https']
#     assert oapi_spec.from_url==True
#     spec_overlay_path = oapi_spec.spec_overlay_path
#
#     if spec_overlay_path.exists():
#         spec_overlay_path.unlink()
#     assert not spec_overlay_path.exists()
#     saved_path = oapi_spec.save_spec_overlay(overwrite=False)
#     assert spec_overlay_path.exists()
#     assert saved_path==spec_overlay_path
#
#     fd = spec_overlay_path.open('w')
#     fd.close()
#
#     saved_spec_overlay_path_stat = spec_overlay_path.stat()
#     spec_overlay_path.touch()
#
#     saved_path = oapi_spec.save_spec_overlay(overwrite=True)
#     new_saved_spec_overlay_path_stat =  saved_path.stat()
#     assert saved_spec_overlay_path_stat!=new_saved_spec_overlay_path_stat












