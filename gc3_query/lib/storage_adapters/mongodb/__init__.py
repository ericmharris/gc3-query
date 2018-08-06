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
import sys, os
import ssl

################################################################################
## Third-Party Imports
from dataclasses import dataclass
import mongoengine

################################################################################
## Project Imports
from gc3_query.lib import *
from gc3_query.lib.gc3logging import get_logging
from gc3_query.lib import gc3_cfg, BASE_DIR

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

def storage_adapter_init(user: str = gc3_cfg.mongodb.security.username,
                         password: str = gc3_cfg.mongodb.security.password,
                         port: int = gc3_cfg.mongodb.net.listen_port,
                         server: str = gc3_cfg.mongodb.net.listen_address,
                         use_ssl: bool = gc3_cfg.mongodb.net.use_ssl,
                         use_auth: bool = gc3_cfg.mongodb.net.use_auth) -> bool:
    if use_auth:
        db_config = dict(
            username=user,
            password=password,
            host=server,
            port=port,
            authentication_source="admin",
            authentication_mechanism="SCRAM-SHA-1",
            ssl=use_ssl,
            ssl_cert_reqs=ssl.CERT_NONE,
        )
    else:
        db_config = dict(host=server, port=port)

    mongoengine.register_connection(alias=gc3_cfg.mongodb.db_alias, name=gc3_cfg.mongodb.db_name, **db_config)
    _info(f"mongodb.storage_adapter_init, connection registered: alias={gc3_cfg.mongodb.db_alias}, name={gc3_cfg.mongodb.db_name}, "
       f"db_config={db_config})")
    return True
