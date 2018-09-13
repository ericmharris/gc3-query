# -*- coding: utf-8 -*-

"""
gc3-query.test_three_part_name_model    [9/12/2018 12:10 PM]
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
from gc3_query.lib.open_api.swagger_formats.models.three_part_name_model import ThreePartNameModel
from gc3_query.lib.iaas_classic.models.instance_model import InstanceModel

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
def setup_gc30003_model():
    service = 'Instances'
    idm_domain = 'gc30003'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    idm_cfg = gc3_config.idm.domains[idm_domain]
    mongodb_connection: MongoClient = storage_adapter_init(mongodb_config=gc3_cfg.iaas_classic.mongodb.as_dict())
    iaas_service = Instances(service_cfg=service_cfg, idm_cfg=idm_cfg)
    assert service==service_cfg.name
    assert idm_domain==idm_cfg.name
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    yield service_cfg, idm_cfg, iaas_service, mongodb_connection


def test_dump(setup_gc30003_model):
    service_cfg, idm_cfg, iaas_service, mongodb_connection = setup_gc30003_model
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    service_response = iaas_service.dump()
    assert service_response.result
    result = service_response.result



def test_query_objects(setup_gc30003_model):
    service_cfg, idm_cfg, iaas_service, mongodb_connection = setup_gc30003_model
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    instance_models = InstanceModel.objects()
    assert instance_models
    instance_model = instance_models.first()
    assert instance_model
    owner =  instance_model.name.object_owner
    assert 'oracle.com' in owner
    assert  instance_model.name.full_name.startswith('/Compute')


def test_from_result_constructor(setup_gc30003_model):
    service_cfg, idm_cfg, iaas_service, mongodb_connection = setup_gc30003_model
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    instance_models = InstanceModel.objects()
    assert instance_models
    instance_model = instance_models.first()
    assert instance_model
    owner =  instance_model.name.object_owner
    assert 'oracle.com' in owner
    assert  instance_model.name.full_name.startswith('/Compute')
