# -*- coding: utf-8 -*-

"""
gc3-query.test_sec_list_format    [9/9/2018 1:12 PM]
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


###############################################################################
## Standard Library Imports
import sys, os

################################################################################
## Third-Party Imports
from dataclasses import dataclass

################################################################################
## Project Imports
from gc3_query.lib import *
from gc3_query.lib.iaas_classic.models.sec_list_model import SecListModel

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


from pathlib import Path

import pytest
from mongoengine import connect

from gc3_query.lib import gc3_cfg
from gc3_query.lib.gc3_config import GC3Config
from gc3_query.lib.iaas_classic.models.sec_list_model import SecListModel
from gc3_query.lib.iaas_classic.sec_lists import SecLists
from gc3_query.lib.base_collections import NestedOrderedDictAttrListBase
# fixme? from gc3_query.lib.open_api import API_SPECS_DIR
import json
from pathlib import Path
from pymongo import MongoClient
import pytest
from bravado_core.spec import Spec
from bravado.response import  BravadoResponse, BravadoResponseMetadata
import mongoengine
from mongoengine.connection import get_connection, register_connection
from gc3_query.lib import *
from gc3_query.lib import gc3_cfg
from gc3_query.lib.export_delegates.mongodb import storage_adapter_init

# from gc3_query.lib.export_delegates.mongodb import storage_adapter_init
# # fixme? from gc3_query.lib.open_api import API_SPECS_DIR
from pathlib import Path
from gc3_query.lib import *
import pytest
# from pprint import pprint, pformat

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

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


inputs = """
        seclist:/Compute-586297329/siva.subramani@oracle.com/paas/JaaS/gc3emacmma804/lb/ora_otd_infraadmin
        seclist:/Compute-586297329/siva.subramani@oracle.com/paas/JaaS/gc3emacmma804/wls/ora_wls_infraadmin
        seclist:/Compute-586297329/mayurnath.gokare@oracle.com/paas/JaaS/gc3apacasbx546/lb/ora_otd
        seclist:/Compute-586297329/dhiru.vallabhbhai@oracle.com/dbaas/gc3emeacetr001/db_1/ora_db
        seclist:/Compute-586297329/ramesh.dadhania@oracle.com/paas/ANALYTICS/gc3emeatfde102/BI/ora_BISecList
        seclist:/Compute-586297329/seetharaman.nandyal@oracle.com/paas/JaaS/gc3apacasbx529/wls/ora_ms
        seclist:/Compute-586297329/seetharaman.nandyal@oracle.com/paas/JaaS/gc3apacasbx529/lb/ora_otd
        seclist:/Compute-586297329/sharad.salian@oracle.com/dbaas/gc3emeaczsi201/db_1/ora_db
        seclist:/Compute-586297329/sharad.salian@oracle.com/paas/SOA/gc3emeaoics106/lb/ora_otd_infraadmin
                seciplist:/oracle/public/paas-infra
"""

@pytest.fixture()
def setup_gc30003_format():
    service = 'SecLists'
    idm_domain = 'gc30003'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    idm_cfg = gc3_config.idm.domains[idm_domain]
    mongodb_connection: MongoClient = storage_adapter_init(mongodb_config=gc3_cfg.iaas_classic.mongodb.as_dict())
    iaas_service = SecLists(service_cfg=service_cfg, idm_cfg=idm_cfg)
    assert service==service_cfg.name
    assert idm_domain==idm_cfg.name
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    yield service_cfg, idm_cfg, iaas_service, mongodb_connection


def test_dump(setup_gc30003_format):
    service_cfg, idm_cfg, iaas_service, mongodb_connection = setup_gc30003_format
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    service_response = iaas_service.dump()
    assert service_response.result
    result = service_response.result


def test_save_one(setup_gc30003_format):
    service_cfg, idm_cfg, iaas_service, mongodb_connection = setup_gc30003_format
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    service_response = iaas_service.dump()
    assert service_response.result
    result = service_response.result
    results = service_response.result.result
    result_dict = service_response.incoming_response.json()
    first_result = results[0]
    first_result_dict = first_result._as_dict()
    sec_list_model = SecListModel(**first_result_dict)
    saved = sec_list_model.save()
    assert saved


def test_save_all(setup_gc30003_format):
    service_cfg, idm_cfg, iaas_service, mongodb_connection = setup_gc30003_format
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    service_response = iaas_service.dump()
    assert service_response.result
    results = service_response.result.result
    for result in results:
        result_dict = result._as_dict()
        sec_list_model = SecListModel(**result_dict)
        saved = sec_list_model.save()