import ssl

import mongoengine

from gc3_query.lib.gc3logging import get_logging

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

MONGODB_DB_NAME = "gc3_query"
MONGODB_PORT = 7117
MONGODB_SERVER = "127.0.0.1"
MONGODB_USE_SSL = False
MONGODB_USE_AUTH = False


def global_init(
    user=None,
    password=None,
    port=MONGODB_PORT,
    server=MONGODB_SERVER,
    use_ssl=MONGODB_USE_SSL,
    use_auth=MONGODB_USE_AUTH,
):

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

    print(" --> Registering connection: {}".format(db_config))
    mongoengine.register_connection(alias="core", name=MONGODB_DB_NAME, **db_config)
