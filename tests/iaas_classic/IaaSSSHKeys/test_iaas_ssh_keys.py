# -*- coding: utf-8 -*-

"""
gc3-query.test_iaas_ssh_keys    [8/27/2018 9:34 AM]
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
from gc3_query.lib.iaas_classic import IaaSRequestsHTTPClient
from gc3_query.lib.iaas_classic.ssh_keys import SSHKeys
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


@pytest.fixture()
def setup_gc30003():
    service = 'SSHKeys'
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
    ssh_keys = SSHKeys(service_cfg=service_cfg, idm_cfg=idm_cfg, http_client=http_client)
    assert ssh_keys.http_client.skip_authentication==False
    assert ssh_keys.http_client.idm_domain_name==idm_cfg.name
    assert ssh_keys.http_client.auth_cookie_header is not None
    assert 'nimbula' in ssh_keys.http_client.auth_cookie_header['Cookie']
    

def test_list_all_ssh_keys(setup_gc30003):
    service_cfg, idm_cfg, http_client = setup_gc30003
    ssh_keys = SSHKeys(service_cfg=service_cfg, idm_cfg=idm_cfg, http_client=http_client)
    assert 'nimbula' in ssh_keys.http_client.auth_cookie_header['Cookie']
    all_ssh_keys = ssh_keys.get_all_ssh_keys()
    assert all_ssh_keys
