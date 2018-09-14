# -*- coding: utf-8 -*-

"""
gc3-query.test_open_ports_policy_violations    [9/13/2018 4:03 PM]
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

from pathlib import Path

import pytest
from mongoengine import connect

from gc3_query.lib import gc3_cfg
from gc3_query.lib.gc3_config import GC3Config
from gc3_query.lib.iaas_classic.sec_rules import SecRules
from gc3_query.lib.base_collections import NestedOrderedDictAttrListBase
# fixme? from gc3_query.lib.open_api import API_SPECS_DIR
import json
from pathlib import Path
import pytest
from bravado_core.spec import Spec
from bravado.response import  BravadoResponse, BravadoResponseMetadata

from pymongo import MongoClient
import mongoengine
from mongoengine.connection import get_connection, register_connection
from mongoengine import QuerySet

from gc3_query.lib import *
from gc3_query.lib import gc3_cfg
from gc3_query.lib.export_delegates.mongodb import storage_adapter_init
# from gc3_query.lib.export_delegates.mongodb import storage_adapter_init
# # fixme? from gc3_query.lib.open_api import API_SPECS_DIR
from pathlib import Path
from gc3_query.lib import *
import pytest
# from pprint import pprint, pformat

from gc3_query.lib.iaas_classic.models.sec_list_model import SecListModel
from gc3_query.lib.iaas_classic.models.sec_rule_model import SecRuleModel
from gc3_query.lib.iaas_classic.models.sec_ip_lists_model import SecIPListsModel
from gc3_query.lib.iaas_classic.models.sec_applications_model import SecApplicationModel
from gc3_query.lib.iaas_classic.models.ip_reservations_model import IPReservationModel
from gc3_query.lib.iaas_classic.models.instance_model import InstanceModel

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
def setup_gc30003_model_query():
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




def test_query_sec_rules(setup_gc30003_model_query):
    service_cfg, idm_cfg, iaas_service, mongodb_connection = setup_gc30003_model_query
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    sec_rules: QuerySet = SecRuleModel.objects()
    sec_rule: SecRuleModel = sec_rules.first()
    sec_lists: QuerySet = SecListModel.objects()
    sec_list = sec_lists.first()
    sec_ip_lists: QuerySet = SecIPListsModel.objects()
    sec_ip_list = sec_ip_lists.first()
    sec_applications: QuerySet = SecApplicationModel.objects()
    sec_application = sec_applications.first()
    ip_reservations: QuerySet = IPReservationModel.objects()
    ip_reservation = ip_reservations.first()
    instances: QuerySet = InstanceModel.objects()
    instance = instances.first()


    enabled_secrules: QuerySet = SecRuleModel.objects(disabled=False)
    disabled_secrules: QuerySet = SecRuleModel.objects(disabled=True)
    assert len(enabled_secrules) > len(disabled_secrules)

    # db.getCollection('SecRules').find({"disabled": false,
    # "src_is_ip": true,
    # "src_list.object_type": "SecIPList",
    # "src_list.object_name": "/oracle/public/public-internet"})
    # enabled_public_internet_secrules: QuerySet = SecRuleModel.objects(disabled=False, src_is_ip=True)
    # enabled_public_internet_secrules_2: QuerySet = SecRuleModel.objects(disabled=False, src_is_ip=True, src_list__object_type="SecIPList")
    # enabled_public_internet_secrules_3: QuerySet = SecRuleModel.objects(disabled=False, src_is_ip=True,
    #                                                                     src_list__object_name="/oracle/public/public-internet")
    enabled_public_internet_secrules: QuerySet = SecRuleModel.objects(disabled=False, src_is_ip=True, src_list__object_type="SecIPList", src_list__full_name__contains="/oracle/public/public-internet")

    assert enabled_public_internet_secrules
    enabled_public_internet_applications = [s.application for s in enabled_public_internet_secrules]
    enabled_public_internet_applications_set = set([s.application for s in enabled_public_internet_secrules])
    assert enabled_public_internet_applications_set


    enabled_sec_applications: QuerySet = SecApplicationModel.objects(name__full_name__in=enabled_public_internet_applications)
    assert enabled_sec_applications



