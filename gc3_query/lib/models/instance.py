import uuid
import mongoengine

from gc3_query.lib import *
from gc3_query.lib.models.model_base import ModelBase
from gc3_query.lib.logging import get_logging

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


class Instance(ModelBase):
    model = mongoengine.StringField(required=True)
    # make = mongoengine.StringField(required=True)
    # year = mongoengine.IntField(required=True)
    # mileage = mongoengine.IntField(default=0)
    # vi_number = mongoengine.StringField(default=lambda: str(uuid.uuid4()).replace("-", ''))
    #
    # engine = mongoengine.EmbeddedDocumentField(Engine, required=True)
    # service_history = mongoengine.EmbeddedDocumentListField(ServiceRecord)
    #
    # # no need to reference owners here, that is entirely contained in owner class

    meta = {
        "db_alias": "core",
        "collection": "instances",
        "indexes": [
            "mileage",
            "year",
            "service_history.price",
            "service_history.customer_rating",
            "service_history.description",
            {"fields": ["service_history.price", "service_history.description"]},
            {"fields": ["service_history.price", "service_history.customer_rating"]},
        ],
    }

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        _debug(f"{self.__class__.__name__}.__init__(args={args}, values={values}):")
