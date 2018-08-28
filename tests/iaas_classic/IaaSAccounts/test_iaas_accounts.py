# -*- coding: utf-8 -*-

"""
gc3-query.test_iaas_accounts    [8/27/2018 9:34 AM]
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
import pytest

################################################################################
## Project Imports
from gc3_query.lib import *

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

import json
from pathlib import Path

from bravado_core.spec import Spec

from gc3_query.lib import gc3_cfg
from gc3_query.lib import *
from gc3_query.lib.gc3_config import GC3Config
from gc3_query.lib.iaas_classic import BRAVADO_CONFIG
from gc3_query.lib.iaas_classic import IaaSRequestsHTTPClient
from gc3_query.lib.iaas_classic.accounts import Accounts
# from gc3_query.lib.open_api import gc3_cfg.OPEN_API_CATALOG_DIR

# from pprint import pprint, pformat

TEST_BASE_DIR: Path = Path(__file__).parent
# config_dir = TEST_BASE_DIR.joinpath("config")
config_dir = gc3_cfg.BASE_DIR.joinpath("etc/config")
output_dir = TEST_BASE_DIR.joinpath('output')
spec_files_dir = TEST_BASE_DIR.joinpath('spec_files')


def test_setup():
    assert TEST_BASE_DIR.exists()
    assert gc3_cfg.OPEN_API_CATALOG_DIR.exists()
    if not config_dir.exists():
        config_dir.mkdir()
    if not output_dir.exists():
        output_dir.mkdir()
    if not spec_files_dir.exists():
        spec_files_dir.mkdir()



def test_get_spec():
    idm_domain = 'gc30003'
    service = 'Accounts'
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


@pytest.fixture()
def setup_gc30003():
    service = 'Accounts'
    idm_domain = 'gc30003'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    idm_cfg = gc3_config.idm.domains[idm_domain]
    http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    assert service==service_cfg.name
    assert idm_domain==idm_cfg.name
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    yield service_cfg, idm_cfg, http_client


def test_init(setup_gc30003):
    service_cfg, idm_cfg, http_client = setup_gc30003
    accounts = Accounts(service_cfg=service_cfg, idm_cfg=idm_cfg, http_client=http_client)
    assert accounts.http_client.skip_authentication==False
    assert accounts.http_client.idm_domain_name==idm_cfg.name
    assert accounts.http_client.auth_cookie_header is not None
    assert 'nimbula' in accounts.http_client.auth_cookie_header['Cookie']
    

def test_list_all_accounts(setup_gc30003):
    service_cfg, idm_cfg, http_client = setup_gc30003
    accounts = Accounts(service_cfg=service_cfg, idm_cfg=idm_cfg, http_client=http_client)
    assert 'nimbula' in accounts.http_client.auth_cookie_header['Cookie']
    all_accounts = accounts.get_all_accounts()
    assert all_accounts

def test_get_all_account_data(setup_gc30003):
    service_cfg, idm_cfg, http_client = setup_gc30003
    accounts = Accounts(service_cfg=service_cfg, idm_cfg=idm_cfg, http_client=http_client)
    assert 'nimbula' in accounts.http_client.auth_cookie_header['Cookie']
    all_accounts = accounts.get_all_account_data()
    assert all_accounts
