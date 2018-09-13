# -*- coding: utf-8 -*-

"""
gc3-query.sec_list_model    [9/12/2018 12:24 PM]
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
from . import *
_debug, _info, _warning, _error, _critical = get_logging(name=__name__)





class SecListFormatModel(DynamicEmbeddedDocument):
    """
    """

    name = StringField()
    idm_service_instance_id = StringField()
    object_owner = StringField()
    object_name = StringField()
    object_type = StringField()
    idm_domain_name = StringField()

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        _debug(f"{self.__class__.__name__}.__init__(args={args}, values={values}):")


    @classmethod
    def from_result(cls, result, key: Optional[str] = 'name') -> 'SecListFormatModel':
        """Return a SecListFormatModel using the values in result['key']

        :param result:
        :param key:
        :return:
        """
        _value = result[key]
        model = SecListFormatModel(full_name=_value .full_name,
                                            idm_service_instance_id=_value .idm_service_instance_id,
                                            object_owner=_value .object_owner,
                                            object_name=_value .object_name,
                                            idm_domain_name=_value .idm_domain_name)
        return model