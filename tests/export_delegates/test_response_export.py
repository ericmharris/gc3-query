# -*- coding: utf-8 -*-

"""
gc3-query.test_response_export    [8/23/2018 5:39 PM]
~~~~~~~~~~~~~~~~

<DESCR SHORT>

<DESCR>
"""

################################################################################
## Standard Library Imports
import sys, os

################################################################################
## Third-Party Imports
from dataclasses import dataclass

################################################################################
## Project Imports
from gc3_query.lib import *

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

from gc3_query.lib.export_delegates.response_export import  ResponseExport
import json
from pathlib import Path

import pytest
from bravado_core.spec import Spec

from gc3_query.lib import gc3_cfg
from gc3_query.lib import *
from gc3_query.lib import gc3_cfg
from gc3_query.lib.gc3_config import GC3Config
from gc3_query.lib.iaas_classic import BRAVADO_CONFIG
from gc3_query.lib.iaas_classic import IaaSServiceBase
from gc3_query.lib.iaas_classic.iaas_requests_http_client import IaaSRequestsHTTPClient
from gc3_query.lib.iaas_classic.sec_rules import SecRules
# # fixme? from gc3_query.lib.open_api import API_SPECS_DIR

from gc3_query.lib.gc3_config import GC3Config
from gc3_query.lib.iaas_classic import IaaSRequestsHTTPClient
from gc3_query.lib.iaas_classic.instances import Instances

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



# @pytest.fixture()
# def setup_gc30003() -> Tuple[Dict[str, Any]]:
#     service = 'Instances'
#     idm_domain = 'gc30003'
#     gc3_config = GC3Config(atoml_config_dir=config_dir)
#     service_cfg = gc3_config.iaas_classic.services.compute[service]
#     idm_cfg = gc3_config.idm.domains[idm_domain]
#     assert service==service_cfg.name
#     assert idm_domain==idm_cfg.name
#     assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
#     yield service_cfg, idm_cfg
#
#
# def test_init_no_auth(setup_gc30003):
#     service_cfg, idm_cfg = setup_gc30003
#     iaas_service_base = IaaSServiceBase(service_cfg=service_cfg, idm_cfg=idm_cfg, skip_authentication=True)
#     assert iaas_service_base.http_client.skip_authentication==True
#     assert iaas_service_base.http_client.idm_domain_name==idm_cfg.name
#
#
# def test_authentication(setup_gc30003):
#     service_cfg, idm_cfg = setup_gc30003
#     iaas_service_base = IaaSServiceBase(service_cfg=service_cfg, idm_cfg=idm_cfg)
#     assert iaas_service_base.http_client.skip_authentication==False
#     assert iaas_service_base.http_client.idm_domain_name==idm_cfg.name
#     assert iaas_service_base.http_client.auth_cookie_header is not None
#     assert 'nimbula' in iaas_service_base.http_client.auth_cookie_header['Cookie']

def test_export_list_instances():
    service = 'Instances'
    idm_domain = 'gc30003'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    idm_cfg = gc3_config.idm.domains[idm_domain]
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    assert service==service_cfg.name
    assert idm_domain==idm_cfg.name
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    instances = Instances(service_cfg=service_cfg, idm_cfg=idm_cfg, from_url=True)
    container=instances.idm_container_name.replace('/', '')
    old_container=instances.idm_container_name
    # http_future = instances.bravado_service_operations.listInstance(container=instances.idm_user_container_name)
    # http_future = instances.bravado_service_operations.listInstance(container=instances.idm_container_name)
    # http_future = instances.bravado_service_operations.listInstance(container=container)
    http_future = instances.service_operations.list_instance(container=container)
    # http_future = instances.service_operations.discover_root_instance()
    request_url = http_future.future.request.url
    service_response = http_future.response()
    result = service_response.result
    result_json = service_response.incoming_response.json()
    assert service_response.metadata.status_code==200
    resp_exp = ResponseExport(dsaf)
