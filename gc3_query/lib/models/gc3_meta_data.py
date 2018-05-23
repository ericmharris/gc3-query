import uuid
import mongoengine

from gc3_query.lib import *
from gc3_query.lib.config import cfg
from gc3_query.lib.logging import get_logging

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


class GC3MetaData(mongoengine.DynamicEmbeddedDocument):
    username = mongoengine.StringField(default=cfg.username)
    identity_domain = mongoengine.StringField(default=cfg.identity_domain)
    region = mongoengine.StringField(default=cfg.region)
    rest_endpoint = mongoengine.StringField(default=cfg.rest_endpoint)

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        _debug(f"{self.__class__.__name__}.__init__(args={args}, values={values}):")
        self.username: str = "eric.harris@oracle.com"
        self.identity_domain: str = "gc30003"
        self.region: str = "us2"
        self.rest_endpoint: str = "gc30003"
