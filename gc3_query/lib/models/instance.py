import mongoengine

#from gc3_query.lib.gc3logging import get_logging
from gc3_query.lib.models.gc3_meta_data import GC3MetaData

from gc3_query.lib import get_logging
_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


class Instance(mongoengine.DynamicDocument):
    account = mongoengine.StringField()
    gc3_meta_data = mongoengine.EmbeddedDocumentField(GC3MetaData, required=True)
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
            "account",
            "identity_domain",
            "region",
            "rest_endpoint",
            "service_history.price",
            "service_history.customer_rating",
            "service_history.description",
            {"fields": ["service_history.price", "service_history.description"]},
            {"fields": ["service_history.price", "service_history.customer_rating"]},
        ],
    }
    # meta = {
    #     'db_alias': 'core',
    #     'collection': 'cars',
    #     'indexes': [
    #         'mileage',
    #         'year',
    #         'service_history.price',
    #         'service_history.customer_rating',
    #         'service_history.description',
    #         {'fields': ['service_history.price', 'service_history.description']},
    #         {'fields': ['service_history.price', 'service_history.customer_rating']},
    #     ]
    # }

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        _debug(f"{self.__class__.__name__}.__init__(args={args}, values={values}):")
