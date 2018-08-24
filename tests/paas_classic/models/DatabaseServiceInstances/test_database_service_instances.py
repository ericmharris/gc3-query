# -*- coding: utf-8 -*-

"""
gc3-query.test_database_service_instances    [8/24/2018 12:29 PM]
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


import json
from pathlib import Path

import pytest
from bravado_core.spec import Spec
from bravado.response import  BravadoResponse, BravadoResponseMetadata
import mongoengine
from gc3_query.lib import *
from gc3_query.lib import gc3_cfg
from gc3_query.lib.paas_classic import PaaSServiceBase
from gc3_query.lib.paas_classic.database_service_instances import DatabaseServiceInstances
from gc3_query.lib.paas_classic.models.database_service_instances import DatabaseServiceInstancesModel
from gc3_query.lib.paas_classic.paas_requests_http_client import PaaSRequestsHTTPClient
# from gc3_query.lib.export_delegates.mongodb import storage_adapter_init
# # fixme? from gc3_query.lib.open_api import API_SPECS_DIR
from pathlib import Path

import pytest


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

def storage_adapter_init():
    alias = gc3_cfg.paas_classic.mongodb.db_alias
    name = gc3_cfg.paas_classic.mongodb.db_name
    server = gc3_cfg.paas_classic.mongodb.net.listen_address
    port = gc3_cfg.paas_classic.mongodb.net.listen_port
    db_config = dict(host=server, port=port, alias=alias, name=name)
    db_config['register'] = mongoengine.register_connection(**db_config)
    _info(f"connection registered: alias={alias}, name={name}, db_config={db_config})")
    return db_config

@pytest.fixture()
def setup_gc30003() -> Tuple[Dict[str, Any]]:
    service = 'ServiceInstances'
    idm_domain = 'gc30003'
    paas_type = 'database'
    service_cfg = gc3_cfg.paas_classic.services.get(paas_type)[service]
    idm_cfg = gc3_cfg.idm.domains[idm_domain]
    mongodb_config = storage_adapter_init()
    assert service==service_cfg.name
    assert idm_domain==idm_cfg.name
    assert gc3_cfg.user.cloud_username == 'eric.harris@oracle.com'
    yield service_cfg, idm_cfg, mongodb_config





def test_get_all_domain_data_save(setup_gc30003):
    service_cfg, idm_cfg, mongodb_config = setup_gc30003
    dbcs_service_instances: DatabaseServiceInstances = DatabaseServiceInstances(service_cfg=service_cfg, idm_cfg=idm_cfg)
    assert dbcs_service_instances.http_client.authenticated
    pass_service_response = dbcs_service_instances.get_all_domain_data()
    assert len(pass_service_response) > 0
    db_data = pass_service_response.results[0]
    json_db_data = pass_service_response.json_results[0]
    assert db_data
    assert 'identity_domain' in db_data
    assert db_data['identity_domain']==idm_cfg.name
    dbcs_service_instances_model = DatabaseServiceInstancesModel(**json_db_data)
    saved = dbcs_service_instances_model.save()
    assert saved







def test_get_all_domain_data_save_all(setup_gc30003):
    service_cfg, idm_cfg, mongodb_config = setup_gc30003
    dbcs_service_instances: DatabaseServiceInstances = DatabaseServiceInstances(service_cfg=service_cfg, idm_cfg=idm_cfg)
    assert dbcs_service_instances.http_client.authenticated
    pass_service_response = dbcs_service_instances.get_all_domain_data()
    assert len(pass_service_response) > 0
    db_data = pass_service_response.results[0]
    # json_db_data = pass_service_response.json_results[0]
    assert db_data
    assert 'identity_domain' in db_data
    assert db_data['identity_domain']==idm_cfg.name
    db_instances = [DatabaseServiceInstancesModel(**json_db_data) for json_db_data in pass_service_response.json_results]
    assert len(db_instances)==len(pass_service_response.json_results)
    saved = []
    for db_instance in db_instances:
        saved.append(db_instance.save())
    assert all(saved)