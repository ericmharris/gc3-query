# -*- coding: utf-8 -*-

"""
#@Filename : __init__.py
#@Date : [8/5/2018 2:51 PM]
#@Poject: gc3-query
#@AUTHOR : emharris

~~~~~~~~~~~~~~~~

<DESCR SHORT>

<DESCR>
"""

################################################################################
## Standard Library Imports
import ssl

################################################################################
## Third-Party Imports
import mongoengine
from pymongo import MongoClient
from mongoengine.connection import get_connection, register_connection

################################################################################
## Project Imports
from gc3_query.lib import *
from gc3_query.lib import gc3_cfg
#from gc3_query.lib.gc3logging import get_logging
# from lib import BASE_DIR

from gc3_query.lib import get_logging
_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

# MONGODB_DB_NAME = "gc3_query"
# MONGODB_PORT = 7117
# MONGODB_SERVER = "127.0.0.1"
# MONGODB_USE_SSL = False
# MONGODB_USE_AUTH = False


# def storage_adapter_init(
#     user=None,
#     password=None,
#     port=MONGODB_PORT,
#     server=MONGODB_SERVER,
#     use_ssl=MONGODB_USE_SSL,
#     use_auth=MONGODB_USE_AUTH,
# ):


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


MONGODB_MODELS_DIR = gc3_cfg.BASE_DIR.joinpath('lib/iaas_classic/models')