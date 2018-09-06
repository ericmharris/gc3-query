# -*- coding: utf-8 -*-

"""
#@Filename : __init__.py
#@Date : [7/30/2018 10:50 AM]
#@Poject: gc3-query
#@AUTHOR : emharris

~~~~~~~~~~~~~~~~

<DESCR SHORT>

<DESCR>
"""

################################################################################
## Standard Library Imports

################################################################################
## Third-Party Imports

from dataclasses import dataclass
from mongoengine import DynamicDocument, EmbeddedDocument
from mongoengine import StringField, URLField, BooleanField, ListField, DictField, DateTimeField, IntField
from mongoengine import DynamicDocument, EmbeddedDocument
from mongoengine import StringField, URLField, BooleanField, ListField, DictField, DateTimeField, IntField, UUIDField

################################################################################
################################################################################
## Project Imports
from gc3_query.lib.export_delegates.mongodb import storage_adapter_init
from gc3_query.lib.open_api.service_responses import IaaSServiceResponse


class IaaSServiceModelDynamicDocument(DynamicDocument):
    connection_config = storage_adapter_init()


class IaaSServiceModelEmbeddedDocument(EmbeddedDocument):
    pass

