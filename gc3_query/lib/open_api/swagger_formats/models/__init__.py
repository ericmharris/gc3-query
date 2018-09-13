# -*- coding: utf-8 -*-

"""
gc3-query.__init__.py    [9/12/2018 10:39 AM]
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
from mongoengine import DynamicDocument, EmbeddedDocument, DynamicEmbeddedDocument
from mongoengine import StringField, URLField, BooleanField, ListField, DictField, DateTimeField, IntField, UUIDField, EmbeddedDocumentField
################################################################################
## Project Imports
from gc3_query.lib import *

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)