import uuid
import mongoengine

from gc3_query.lib import *
from gc3_query.lib.logging import get_logging
_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

class ModelBase(mongoengine.Document):

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        _debug(f'{self.__class__.__name__}.__init__(args={args}, values={values}):')

