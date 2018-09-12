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
import click
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



from gc3_query.lib.iaas_classic.instances import Instances
from gc3_query.lib.iaas_classic.models.instance_model import InstanceModel

@pytest.fixture()
def setup_Instances():
    service = 'Instances'
    # idm_domain = 'gc30003'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    mongodb_connection: MongoClient = storage_adapter_init(mongodb_config=gc3_config.iaas_classic.mongodb.as_dict())
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    idm_domains = [idm_domain for idm_domain in gc3_config.idm.domains.values() if idm_domain.active]
    # idm_cfg = gc3_config.idm.domains[idm_domain]
    # iaas_service = Instances(service_cfg=service_cfg, idm_cfg=idm_cfg)
    iaas_services = [Instances(service_cfg=service_cfg, idm_cfg=idm_cfg) for idm_cfg in idm_domains]
    assert service==service_cfg.name
    yield service_cfg, idm_domains, iaas_services, mongodb_connection



def test_save_all_Instances(setup_Instances):
    service_cfg, idm_domains, iaas_services, mongodb_connection = setup_Instances
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    total_results = 0
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
        total_results = total_results + len(results)
        for result in results:
            result_dict = result._as_dict()
            model = InstanceModel(**result_dict)
            saved = model.save()
    print(f"\nPRINT: {iaas_service.service_name} exported: {total_results}")
    # click.echo(click.style(f"\n{iaas_service.service_name} instances exported: {total_results}", fg="green"))



from gc3_query.lib.iaas_classic.sec_applications import SecApplications
from gc3_query.lib.iaas_classic.models.sec_applications_model import SecApplicationModel

@pytest.fixture()
def setup_SecApplications():
    service = 'SecApplications'
    # idm_domain = 'gc30003'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    mongodb_connection: MongoClient = storage_adapter_init(mongodb_config=gc3_config.iaas_classic.mongodb.as_dict())
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    idm_domains = [idm_domain for idm_domain in gc3_config.idm.domains.values() if idm_domain.active]
    # idm_cfg = gc3_config.idm.domains[idm_domain]
    # iaas_service = SecApplications(service_cfg=service_cfg, idm_cfg=idm_cfg)
    iaas_services = [SecApplications(service_cfg=service_cfg, idm_cfg=idm_cfg) for idm_cfg in idm_domains]
    assert service==service_cfg.name
    yield service_cfg, idm_domains, iaas_services, mongodb_connection



def test_save_all_SecApplications(setup_SecApplications):
    service_cfg, idm_domains, iaas_services, mongodb_connection = setup_SecApplications
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    total_results = 0
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
        total_results = total_results + len(results)
        for result in results:
            result_dict = result._as_dict()
            model = SecApplicationModel(**result_dict)
            saved = model.save()
    print(f"\nPRINT: {iaas_service.service_name} exported: {total_results}")









from gc3_query.lib.iaas_classic.sec_ip_lists import SecIPLists
from gc3_query.lib.iaas_classic.models.sec_ip_lists_model import SecIPListsModel

@pytest.fixture()
def setup_SecIPLists():
    service = 'SecIPLists'
    # idm_domain = 'gc30003'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    mongodb_connection: MongoClient = storage_adapter_init(mongodb_config=gc3_config.iaas_classic.mongodb.as_dict())
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    idm_domains = [idm_domain for idm_domain in gc3_config.idm.domains.values() if idm_domain.active]
    # idm_cfg = gc3_config.idm.domains[idm_domain]
    # iaas_service = SecIPLists(service_cfg=service_cfg, idm_cfg=idm_cfg)
    iaas_services = [SecIPLists(service_cfg=service_cfg, idm_cfg=idm_cfg) for idm_cfg in idm_domains]
    assert service==service_cfg.name
    yield service_cfg, idm_domains, iaas_services, mongodb_connection



def test_save_all_SecIPLists(setup_SecIPLists):
    service_cfg, idm_domains, iaas_services, mongodb_connection = setup_SecIPLists
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    total_results = 0
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
        total_results = total_results + len(results)
        for result in results:
            result_dict = result._as_dict()
            model = SecIPListsModel(**result_dict)
            saved = model.save()
    print(f"\nPRINT: {iaas_service.service_name} exported: {total_results}")





from gc3_query.lib.iaas_classic.sec_lists import SecLists
from gc3_query.lib.iaas_classic.models.sec_list_model import SecListModel

@pytest.fixture()
def setup_SecLists():
    service = 'SecLists'
    # idm_domain = 'gc30003'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    mongodb_connection: MongoClient = storage_adapter_init(mongodb_config=gc3_config.iaas_classic.mongodb.as_dict())
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    idm_domains = [idm_domain for idm_domain in gc3_config.idm.domains.values() if idm_domain.active]
    # idm_cfg = gc3_config.idm.domains[idm_domain]
    # iaas_service = SecLists(service_cfg=service_cfg, idm_cfg=idm_cfg)
    iaas_services = [SecLists(service_cfg=service_cfg, idm_cfg=idm_cfg) for idm_cfg in idm_domains]
    assert service==service_cfg.name
    yield service_cfg, idm_domains, iaas_services, mongodb_connection


def test_save_all_SecLists(setup_SecLists):
    service_cfg, idm_domains, iaas_services, mongodb_connection = setup_SecLists
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    total_results = 0
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
        total_results = total_results + len(results)
        for result in results:
            result_dict = result._as_dict()
            model = SecListModel(**result_dict)
            saved = model.save()
    print(f"\nPRINT: {iaas_service.service_name} exported: {total_results}")

@pytest.fixture()
def setup_SecRules():
    service = 'SecRules'
    # idm_domain = 'gc30003'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    mongodb_connection: MongoClient = storage_adapter_init(mongodb_config=gc3_config.iaas_classic.mongodb.as_dict())
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    idm_domains = [idm_domain for idm_domain in gc3_config.idm.domains.values() if idm_domain.active]
    # idm_cfg = gc3_config.idm.domains[idm_domain]
    # iaas_service = SecRules(service_cfg=service_cfg, idm_cfg=idm_cfg)
    iaas_services = [SecRules(service_cfg=service_cfg, idm_cfg=idm_cfg) for idm_cfg in idm_domains]
    assert service == service_cfg.name
    yield service_cfg, idm_domains, iaas_services, mongodb_connection

def test_save_all_SecRules(setup_SecRules):
    service_cfg, idm_domains, iaas_services, mongodb_connection = setup_SecRules
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    total_results = 0
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
        total_results = total_results + len(results)
        for result in results:
            result_dict = result._as_dict()
            model = SecRuleModel(**result_dict)
            saved = model.save()
    print(f"\nPRINT: {iaas_service.service_name} exported: {total_results}")
