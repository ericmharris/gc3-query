# -*- coding: utf-8 -*-

"""
gc3-query.__init__.py    [8/24/2018 11:58 AM]
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
from mongoengine import DynamicDocument, EmbeddedDocument
from mongoengine import StringField, URLField, BooleanField, ListField, DictField, DateTimeField, IntField, UUIDField

################################################################################
## Project Imports
from gc3_query.lib import *
from gc3_query.lib.open_api.service_responses import PaaSServiceResponse
from gc3_query.lib.export_delegates.mongodb import storage_adapter_init

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)