# -*- coding: utf-8 -*-

"""
gc3-query.test_iaas_sec_ip_lists_model    [9/7/2018 3:22 PM]
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
from gc3_query.lib.iaas_classic.models.sec_ip_lists_model import SecIPListsModel

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


from pathlib import Path

import pytest
from mongoengine import connect

from gc3_query.lib import gc3_cfg
from gc3_query.lib.gc3_config import GC3Config
from gc3_query.lib.iaas_classic.sec_ip_lists import SecIPLists
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






def test_list_sec_ip_lists_model_from_url():
    service = 'SecIPLists'
    idm_domain = 'gc30003'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    idm_cfg = gc3_config.idm.domains[idm_domain]
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    assert service==service_cfg.name
    assert idm_domain==idm_cfg.name
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    sec_ip_lists = SecIPLists(service_cfg=service_cfg, idm_cfg=idm_cfg, from_url=True)
    # container=sec_ip_lists.idm_container_name.replace('/', '')
    container=sec_ip_lists.idm_root_container_name
    old_container=sec_ip_lists.idm_container_name
    # http_future = sec_ip_lists.bravado_service_operations.listInstance(container=sec_ip_lists.idm_user_container_name)
    # http_future = sec_ip_lists.bravado_service_operations.listInstance(container=sec_ip_lists.idm_container_name)
    # http_future = sec_ip_lists.bravado_service_operations.listSecRule(container=container)
    http_future = sec_ip_lists.service_operations.list_sec_ip_list(container=container)
    # http_future = sec_ip_lists.service_operations.discover_root_instance()
    request_url = http_future.future.request.url
    service_response = http_future.response()
    result = service_response.result
    result_json = service_response.incoming_response.json()
    assert service_response.metadata.status_code==200
    assert len(result_json['result']) > 0
    assert 'src_list' in result_json['result'][0]


def test_list_sec_ip_lists_model_save_from_url():
    service = 'SecIPLists'
    idm_domain = 'gc30003'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    idm_cfg = gc3_config.idm.domains[idm_domain]
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    assert service==service_cfg.name
    assert idm_domain==idm_cfg.name
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    sec_ip_lists = SecIPLists(service_cfg=service_cfg, idm_cfg=idm_cfg, from_url=True)
    # container=sec_ip_lists.idm_container_name.replace('/', '')
    container=sec_ip_lists.idm_root_container_name
    old_container=sec_ip_lists.idm_container_name
    # http_future = sec_ip_lists.bravado_service_operations.listInstance(container=sec_ip_lists.idm_user_container_name)
    # http_future = sec_ip_lists.bravado_service_operations.listInstance(container=sec_ip_lists.idm_container_name)

    # http_future = instances.bravado_service_operations.discoverRootInstance(_request_options={"headers": {"Accept": "application/oracle-compute-v3+directory+json"}})
    # operation_name = 'listSecRule'
    # callable_operation = getattr(sec_ip_lists.bravado_service_operations, operation_name)
    # operation_headers = {"Accept": ','.join(callable_operation.operation.produces),
    #                      "Content-Type": ','.join(callable_operation.operation.consumes)
    #                      }
    # sec_ip_lists.http_client.session.headers.update(operation_headers)
    # # http_future = callable_operation(container=container,  _request_options={"headers": {"Accept": ','.join(callable_operation.operation.produces)}})
    # http_future = callable_operation(container=container)

    # http_future = sec_ip_lists.bravado_service_operations.listSecRule(container=container, _request_options={"headers": {"Accept": ','.join(callable_operation.operation.produces)}})
    http_future = sec_ip_lists.service_operations.list_sec_ip_list(container=container)

    # http_future = sec_ip_lists.service_operations.discover_root_instance()
    request_url = http_future.future.request.url
    service_response = http_future.response()
    result = service_response.result
    assert service_response.metadata.status_code==200
    results_json = service_response.incoming_response.json()['result']
    assert len(results_json) > 0
    result_json = results_json[0]
    assert 'src_list' in result_json
    result_json['sec_ip_list_id'] = result_json.pop('id')
    sec_ip_list_model = SecIPListsModel(**result_json)
    saved = sec_ip_list_model.save()
    assert saved


# def storage_adapter_init():
#     alias = gc3_cfg.iaas_classic.mongodb.db_alias
#     name = gc3_cfg.iaas_classic.mongodb.db_name
#     server = gc3_cfg.iaas_classic.mongodb.net.listen_address
#     port = gc3_cfg.iaas_classic.mongodb.net.listen_port
#     db_config = dict(host=server, port=port, alias=alias, name=name)
#     db_config['register'] = mongoengine.register_connection(**db_config)
#     _info(f"connection registered: alias={alias}, name={name}, db_config={db_config})")
#     return db_config

# @pytest.fixture()
# def setup_gc30003_model() -> Tuple[Dict[str, Any]]:
#     service = 'ServiceInstances'
#     idm_domain = 'gc30003'
#     iaas_type = 'database'
#     service_cfg = gc3_cfg.iaas_classic.services.get(iaas_type)[service]
#     idm_cfg = gc3_cfg.idm.domains[idm_domain]
#     mongodb_config = storage_adapter_init()
#     assert service==service_cfg.name
#     assert idm_domain==idm_cfg.name
#     assert gc3_cfg.user.cloud_username == 'eric.harris@oracle.com'
#     yield service_cfg, idm_cfg, mongodb_config

def storage_adapter_init(mongodb_config: DictStrAny) -> MongoClient:
    """
    mongoengine.register_connection(alias, db=None, name=None, host=None, port=None, read_preference=Primary(), username=None, password=None, authentication_source=None, authentication_mechanism=None, **kwargs)

    Add a connection.

    Parameters:
    alias – the name that will be used to refer to this connection throughout MongoEngine
    name – the name of the specific database to use
    db – the name of the database to use, for compatibility with connect
    host – the host name of the mongod instance to connect to
    port – the port that the mongod instance is running on
    read_preference – The read preference for the collection ** Added pymongo 2.1
    username – username to authenticate with
    password – password to authenticate with
    authentication_source – database to authenticate against
    authentication_mechanism – database authentication mechanisms. By default, use SCRAM-SHA-1 with MongoDB 3.0 and later, MONGODB-CR (MongoDB Challenge Response protocol) for older servers.
    is_mock – explicitly use mongomock for this connection (can also be done by using mongomock:// as db host prefix)
    kwargs – ad-hoc parameters to be passed into the pymongo driver, for example maxpoolsize, tz_aware, etc. See the documentation for pymongo’s MongoClient for a full list.
        :return:
    """
    alias = mongodb_config["alias"]
    name = mongodb_config["name"]
    db = mongodb_config["db"]
    host = mongodb_config["net"]["host"]
    port = mongodb_config["net"]["port"]
    _ = register_connection(alias=alias, db=db, host=host, port=port)
    # _connection = connect(db=db, alias=alias)
    connection: MongoClient = get_connection(alias=alias)
    _info(f"connection registered: alias={alias}, name={name}, db={db}, host={host}, port={port}")
    return connection


@pytest.fixture()
def setup_gc30003_model():
    service = 'SecIPLists'
    idm_domain = 'gc30003'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    idm_cfg = gc3_config.idm.domains[idm_domain]
    mongodb_connection: MongoClient = storage_adapter_init(mongodb_config=gc3_cfg.iaas_classic.mongodb.as_dict())
    iaas_service = SecIPLists(service_cfg=service_cfg, idm_cfg=idm_cfg)
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


def test_save_one(setup_gc30003_model):
    service_cfg, idm_cfg, iaas_service, mongodb_connection = setup_gc30003_model
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    service_response = iaas_service.dump()
    assert service_response.result
    result = service_response.result
    results = service_response.result.result
    result_dict = service_response.incoming_response.json()
    first_result = results[0]
    first_result_dict = first_result._as_dict()
    sec_ip_list_model = SecIPListsModel(**first_result_dict)
    saved = sec_ip_list_model.save()
    assert saved


def test_save_all(setup_gc30003_model):
    service_cfg, idm_cfg, iaas_service, mongodb_connection = setup_gc30003_model
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    service_response = iaas_service.dump()
    assert service_response.result
    results = service_response.result.result
    for result in results:
        result_dict = result._as_dict()
        sec_ip_list_model = SecIPListsModel(**result_dict)
        saved = sec_ip_list_model.save()



def test_insert_all(setup_gc30003_model):
    service_cfg, idm_cfg, iaas_service, mongodb_connection = setup_gc30003_model
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    service_response = iaas_service.dump()
    assert service_response.result
    results = service_response.result.result
    sec_ip_lists = [SecIPListsModel(**result._as_dict()) for result in results]
    _ = SecIPListsModel.objects().insert(sec_ip_lists)
    assert sec_ip_lists





