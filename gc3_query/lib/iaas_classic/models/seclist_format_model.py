# -*- coding: utf-8 -*-

"""
gc3-query.seclist_format_model    [9/8/2018 1:16 PM]
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

################################################################################
## Standard Library Imports
import sys, os

################################################################################
## Third-Party Imports
from dataclasses import dataclass

################################################################################
## Project Imports
from gc3_query.lib import *
from gc3_query.lib import *
# from gc3_query.lib.gc3logging import get_logging
from . import *

from gc3_query.lib import get_logging

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


class SecListFormatModel(EmbeddedDocument):
    """
    seclist:/Compute-586297329/siva.subramani@oracle.com/paas/ANALYTICS/gc3emeaaadw603/BI/ora_BISecList
    """
    name = StringField()
    idm_service_instance_id = StringField()
    object_owner = StringField()
    object_name = StringField()
    idm_domain_name = StringField()

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        _debug(f"{self.__class__.__name__}.__init__(args={args}, values={values}):")

