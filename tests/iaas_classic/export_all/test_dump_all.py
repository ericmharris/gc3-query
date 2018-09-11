# -*- coding: utf-8 -*-

"""
gc3-query.test_export_all    [9/11/2018 2:28 PM]
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

##################
from pathlib import Path

import pytest
from mongoengine import connect

from gc3_query.lib import gc3_cfg
from gc3_query.lib.gc3_config import GC3Config
from gc3_query.lib.iaas_classic.models.sec_rule_model import SecRuleModel
from gc3_query.lib.iaas_classic.sec_rules import SecRules
from gc3_query.lib.base_collections import NestedOrderedDictAttrListBase
# fixme? from gc3_query.lib.open_api import API_SPECS_DIR
import json
from pathlib import Path
import pytest
from bravado_core.spec import Spec
from bravado.response import  BravadoResponse, BravadoResponseMetadata
import mongoengine

from pymongo import MongoClient
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

##################



from gc3_query.lib.iaas_classic.xxxxxs import XXXXXs
from gc3_query.lib.iaas_classic.models.xxxxx_model import XXXXXModel

@pytest.fixture()
def setup_XXXXXs():
    service = 'XXXXXs'
    # idm_domain = 'gc30003'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    mongodb_connection: MongoClient = storage_adapter_init(mongodb_config=gc3_config.iaas_classic.mongodb.as_dict())
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    idm_domains = [idm_domain for idm_domain in gc3_config.idm.domains.values() if idm_domain.active]
    # idm_cfg = gc3_config.idm.domains[idm_domain]
    # iaas_service = XXXXXs(service_cfg=service_cfg, idm_cfg=idm_cfg)
    iaas_services = [XXXXXs(service_cfg=service_cfg, idm_cfg=idm_cfg) for idm_cfg in idm_domains]
    assert service==service_cfg.name
    yield service_cfg, idm_domains, iaas_services, mongodb_connection



def test_save_all_XXXXXs(setup_XXXXXs):
    service_cfg, idm_domains, iaas_services, mongodb_connection = setup_XXXXXs
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    for iaas_service in iaas_services:
        try:
            service_response = iaas_service.dump()
        except Exception as e:
            _warning(f"Exception during iaas_service.dump() for {iaas_service.service_name} on IDM Domain {iaas_service.idm_cfg.name}\nRetrying ...")
            _warning(f"Exception: {e}")
            _warning(f"Retrying ...")
            service_response = iaas_service.dump()
        assert service_response.result
        results = service_response.result.result
        for result in results:
            result_dict = result._as_dict()
            model = XXXXXModel(**result_dict)
            saved = model.save()













@pytest.fixture()
def setup_gc30003_model():
    service = 'SecRules'
    idm_domain = 'gc30003'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    idm_cfg = gc3_config.idm.domains[idm_domain]
    mongodb_connection: MongoClient = storage_adapter_init(mongodb_config=gc3_cfg.iaas_classic.mongodb.as_dict())
    iaas_service = SecRules(service_cfg=service_cfg, idm_cfg=idm_cfg)
    assert service==service_cfg.name
    assert idm_domain==idm_cfg.name
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    yield service_cfg, idm_cfg, iaas_service, mongodb_connection


def test_dump_gc30003(setup_gc30003_model):
    service_cfg, idm_cfg, iaas_service, mongodb_connection = setup_gc30003_model
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    service_response = iaas_service.dump()
    assert service_response.result
    result_json = service_response.incoming_response.json()
    result = service_response.result


def test_save_all_gc30003(setup_gc30003_model):
    service_cfg, idm_cfg, iaas_service, mongodb_connection = setup_gc30003_model
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    service_response = iaas_service.dump()
    assert service_response.result
    results = service_response.result.result
    for result in results:
        result_dict = result._as_dict()
        sec_rule_model = SecRuleModel(**result_dict)
        saved = sec_rule_model.save()



@pytest.fixture()
def setup_gc35000_model():
    service = 'SecRules'
    idm_domain = 'gc35000'
    gc3_config = GC3Config()
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    idm_cfg = gc3_config.idm.domains[idm_domain]
    mongodb_connection: MongoClient = storage_adapter_init(mongodb_config=gc3_cfg.iaas_classic.mongodb.as_dict())
    iaas_service = SecRules(service_cfg=service_cfg, idm_cfg=idm_cfg)
    assert service==service_cfg.name
    assert idm_domain==idm_cfg.name
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    yield service_cfg, idm_cfg, iaas_service, mongodb_connection


def test_dump_gc35000(setup_gc35000_model):
    service_cfg, idm_cfg, iaas_service, mongodb_connection = setup_gc35000_model
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    service_response = iaas_service.dump()
    assert service_response.result
    result_json = service_response.incoming_response.json()
    result = service_response.result


def test_save_all_gc35000(setup_gc35000_model):
    service_cfg, idm_cfg, iaas_service, mongodb_connection = setup_gc35000_model
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    service_response = iaas_service.dump()
    assert service_response.result
    results = service_response.result.result
    for result in results:
        result_dict = result._as_dict()
        sec_rule_model = SecRuleModel(**result_dict)
        saved = sec_rule_model.save()


@pytest.fixture()
def setup_gc35001_model():
    service = 'SecRules'
    idm_domain = 'gc35001'
    gc3_config = GC3Config()
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    idm_cfg = gc3_config.idm.domains[idm_domain]
    mongodb_connection: MongoClient = storage_adapter_init(mongodb_config=gc3_cfg.iaas_classic.mongodb.as_dict())
    iaas_service = SecRules(service_cfg=service_cfg, idm_cfg=idm_cfg)
    assert service==service_cfg.name
    assert idm_domain==idm_cfg.name
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    yield service_cfg, idm_cfg, iaas_service, mongodb_connection


def test_dump_gc35001(setup_gc35001_model):
    service_cfg, idm_cfg, iaas_service, mongodb_connection = setup_gc35001_model
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    service_response = iaas_service.dump()
    assert service_response.result
    result_json = service_response.incoming_response.json()
    result = service_response.result



def test_save_all_gc35001(setup_gc35001_model):
    service_cfg, idm_cfg, iaas_service, mongodb_connection = setup_gc35001_model
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    service_response = iaas_service.dump()
    assert service_response.result
    results = service_response.result.result
    for result in results:
        result_dict = result._as_dict()
        sec_rule_model = SecRuleModel(**result_dict)
        saved = sec_rule_model.save()




@pytest.fixture()
def setup_gc30002_model():
    service = 'SecRules'
    idm_domain = 'gc30002'
    gc3_config = GC3Config()
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    idm_cfg = gc3_config.idm.domains[idm_domain]
    mongodb_connection: MongoClient = storage_adapter_init(mongodb_config=gc3_cfg.iaas_classic.mongodb.as_dict())
    iaas_service = SecRules(service_cfg=service_cfg, idm_cfg=idm_cfg)
    assert service==service_cfg.name
    assert idm_domain==idm_cfg.name
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    yield service_cfg, idm_cfg, iaas_service, mongodb_connection


def test_dump_gc30002(setup_gc30002_model):
    service_cfg, idm_cfg, iaas_service, mongodb_connection = setup_gc30002_model
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    service_response = iaas_service.dump()
    assert service_response.result
    result_json = service_response.incoming_response.json()
    result = service_response.result



def test_save_all_gc30002(setup_gc30002_model):
    service_cfg, idm_cfg, iaas_service, mongodb_connection = setup_gc30002_model
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    service_response = iaas_service.dump()
    assert service_response.result
    results = service_response.result.result
    for result in results:
        result_dict = result._as_dict()
        sec_rule_model = SecRuleModel(**result_dict)
        saved = sec_rule_model.save()









@pytest.fixture()
def setup_gc3pilot_model():
    service = 'SecRules'
    idm_domain = 'gc3pilot'
    gc3_config = GC3Config()
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    idm_cfg = gc3_config.idm.domains[idm_domain]
    mongodb_connection: MongoClient = storage_adapter_init(mongodb_config=gc3_cfg.iaas_classic.mongodb.as_dict())
    iaas_service = SecRules(service_cfg=service_cfg, idm_cfg=idm_cfg)
    assert service==service_cfg.name
    assert idm_domain==idm_cfg.name
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    yield service_cfg, idm_cfg, iaas_service, mongodb_connection


def test_dump_gc3pilot(setup_gc3pilot_model):
    service_cfg, idm_cfg, iaas_service, mongodb_connection = setup_gc3pilot_model
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    service_response = iaas_service.dump()
    assert service_response.result
    result_json = service_response.incoming_response.json()
    result = service_response.result



def test_save_all_gc3pilot(setup_gc3pilot_model):
    service_cfg, idm_cfg, iaas_service, mongodb_connection = setup_gc3pilot_model
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    service_response = iaas_service.dump()
    assert service_response.result
    results = service_response.result.result
    for result in results:
        result_dict = result._as_dict()
        sec_rule_model = SecRuleModel(**result_dict)
        saved = sec_rule_model.save()






