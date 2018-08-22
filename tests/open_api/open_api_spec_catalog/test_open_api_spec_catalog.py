from pathlib import Path

from gc3_query import BASE_DIR
from gc3_query.lib import *
from gc3_query.lib.gc3_config import GC3Config
from gc3_query.lib.open_api.open_api_spec_catalog import OpenApiSpecCatalog

# from pprint import pprint, pformat

TEST_BASE_DIR: Path = Path(__file__).parent
# config_dir = TEST_BASE_DIR.joinpath("config")
config_dir = BASE_DIR.joinpath("etc/config")
output_dir = TEST_BASE_DIR.joinpath('output')




def test_setup():
    assert TEST_BASE_DIR.exists()
    assert config_dir.exists()
    assert gc3_cfg.OPEN_API_CATALOG_DIR.exists()
    assert output_dir.exists()



def test_init():
    idm_domain = 'gc30003'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    idm_cfg = gc3_config.idm.domains[idm_domain]
    api_catalog_config = gc3_config.iaas_classic.open_api_spec_catalog
    services_config = gc3_config.iaas_classic.services
    # oapi_spec_catalog = OpenApiSpecCatalog(api_catalog_config=api_catalog_config, services_cfg=services_config)
    oapi_spec_catalog = OpenApiSpecCatalog(api_catalog_config=api_catalog_config, services_config=services_config, idm_cfg=idm_cfg)
    assert oapi_spec_catalog
    assert oapi_spec_catalog.api_catalog_name=='iaas_classic'
    assert 'Instances' in oapi_spec_catalog


# def test_schemes_updated():
#     service = 'Instances'
#     gc3_config = GC3Config(atoml_config_dir=config_dir)
#     service_cfg = gc3_config.iaas_classic.services[service]
#     api_catalog_config = gc3_config.iaas_classic.open_api_spec_catalog
#     oapi_spec = OpenApiSpec(api_catalog_config=api_catalog_config, service_cfg=service_cfg)
#     assert oapi_spec.name == service
#     assert oapi_spec.spec_dict['schemes'] == ['https']



#
# def test_save_spec_to_catalog():
#     idm_domain = 'gc30003'
#     service = 'Instances'
#     gc3_config = GC3Config(atoml_config_dir=config_dir)
#     idm_cfg = gc3_config.idm.domains[idm_domain]
#     service_cfg = gc3_config.iaas_classic.services[service]
#     api_catalog_config = gc3_config.iaas_classic.open_api_spec_catalog
#     oapi_spec = OpenApiSpec(service_cfg=service_cfg, open_api_specs_cfg=open_api_specs_cfg, idm_cfg=idm_cfg)
#     assert oapi_spec.name == service
#     assert oapi_spec._spec_data['schemes'] == ['https']
#     assert oapi_spec.from_url == True
#     spec_file_path = oapi_spec.spec_file
#     if spec_file_path.exists():
#         spec_file_path.unlink()
#     assert not spec_file_path.exists()
#     saved_path = oapi_spec.save_spec(overwrite=False)
#     assert saved_path == spec_file_path
#
#     fd = spec_file_path.open('w')
#     fd.close()
#     saved_path_stat = saved_path.stat()
#
#     saved_path = oapi_spec.save_spec(overwrite=True)
#     assert saved_path_stat != saved_path.stat()
#
#
#
#
#
# def test_spec_file_not_found():
#     idm_domain = 'gc30003'
#     service = 'Instances'
#     gc3_config = GC3Config(atoml_config_dir=config_dir)
#     idm_cfg = gc3_config.idm.domains[idm_domain]
#     service_cfg = gc3_config.iaas_classic.services[service]
#     api_catalog_config = gc3_config.iaas_classic.open_api_spec_catalog
#     oapi_spec = OpenApiSpec(service_cfg=service_cfg, open_api_specs_cfg=open_api_specs_cfg, idm_cfg=idm_cfg)
#     spec_file_path = oapi_spec.spec_file
#     if spec_file_path.exists():
#         spec_file_path.unlink()
#     assert not spec_file_path.exists()
#     del (oapi_spec)
#     oapi_spec = OpenApiSpec(service_cfg=service_cfg, open_api_specs_cfg=open_api_specs_cfg, idm_cfg=idm_cfg)
#     assert spec_file_path.exists()
#
#     assert oapi_spec.name == service
#     assert oapi_spec._spec_data['schemes'] == ['https']
#     core_spec = oapi_spec.get_swagger_spec(rest_endpoint=idm_cfg.rest_endpoint)
#     exported_file_paths = oapi_spec.export()
#     for exported_file_path in exported_file_paths:
#         assert exported_file_path.exists()
#
#
# def test_archive_spec_to_catalog():
#     idm_domain = 'gc30003'
#     service = 'Instances'
#     gc3_config = GC3Config(atoml_config_dir=config_dir)
#     idm_cfg = gc3_config.idm.domains[idm_domain]
#     service_cfg = gc3_config.iaas_classic.services[service]
#     api_catalog_config = gc3_config.iaas_classic.open_api_spec_catalog
#     oapi_spec = OpenApiSpec(service_cfg=service_cfg, open_api_specs_cfg=open_api_specs_cfg, idm_cfg=idm_cfg)
#     assert oapi_spec.name == service
#     assert oapi_spec._spec_data['schemes'] == ['https']
#     assert oapi_spec.from_url == True
#     spec_archive_file_path = oapi_spec.spec_archive_file
#     if spec_archive_file_path.exists():
#         spec_archive_file_path.unlink()
#     assert not spec_archive_file_path.exists()
#     archive_path = oapi_spec.archive_spec_to_catalog()
#     assert archive_path == spec_archive_file_path
#     archive_path_stat = archive_path.stat()
#     archive_path = oapi_spec.save_spec(overwrite=True)
#     assert archive_path_stat != archive_path.stat()