# -*- coding: utf-8 -*-

"""
gc3-query.test_multi_part_name_formats    [9/12/2018 9:48 AM]
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


import datetime
from pathlib import Path

import pytest
from dateutil.tz import tzutc
from pymongo import MongoClient

from gc3_query.lib import gc3_cfg
from gc3_query.lib.export_delegates.mongodb import storage_adapter_init
from gc3_query.lib.gc3_config import GC3Config
from gc3_query.lib.iaas_classic import IaaSRequestsHTTPClient
from gc3_query.lib.iaas_classic.instances import Instances
from gc3_query.lib.open_api.swagger_formats.three_part_name_formats import ThreePartNameFormat

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



@pytest.fixture()
def setup_fixture():
    s = """
        /Compute-586297329/dhiru.vallabhbhai@oracle.com/paas/BDCSCE/gc3apacasbx500/bdcsce/vm-1/8aa0ae10-35f3-4b21-aac1-a4a6328edf1e
        /Compute-605519274/siva.subramani@oracle.com/dbaas/gc3ossitcmf103DBAAS/db_1/vm-1/04db581d-cb17-497e-8a6a-0e74cf4cbf5d
        /Compute-604700914/mayurnath.gokare@oracle.com/paas/OEHPCS/gc3mayurtst100/kafka/vm-1/0e86f68b-422c-4ed6-b62d-b2f1dd1cf28b
        /Compute-gc3pilot/eric.harris@oracle.com/psft-cldmgr-v501/8ee914dc-70c2-49b2-af2c-af1941af94f8
        /Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-soar-d05-dbcs/db_1/vm-1/57cced1d-c74f-41da-9c24-e86666eee4b2
        /Compute-587626604/ramesh.dadhania@oracle.com/paas/BDCSCE/rdbdcstest/1/bdcsce/vm-3/00da5312-040f-4677-b69a-3f5d9f6be575
        /Compute-gc3pilot/seetharaman.nandyal@oracle.com/dbaas/ocrltest/db_1/ora_http
        /Compute-gc3pilot/seetharaman.nandyal@oracle.com/dbaas/sn-test-inst/db_1/ora_dblistener
    """
    names = [l.strip() for l in s.splitlines() if '/Compute-' in l]
    yield names


def test_init(setup_fixture):
    names = setup_fixture

    for name in names:
        tpn = ThreePartNameFormat(name=name)
        assert tpn
        assert 'Compute-' in  tpn['name']
        assert 'oracle.com' in  tpn['object_owner']
        assert tpn['idm_domain_name'] in gc3_cfg.idm.domains

def test_attribute_access(setup_fixture):
    names = setup_fixture

    for name in names:
        tpn = ThreePartNameFormat(name=name)
        assert tpn
        assert 'Compute-' in  tpn.name
        assert 'oracle.com' in  tpn.object_owner
        assert tpn.idm_domain_name in gc3_cfg.idm.domains