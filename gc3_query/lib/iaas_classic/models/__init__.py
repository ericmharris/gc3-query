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

from mongoengine import DynamicDocument, EmbeddedDocument

################################################################################
## Project Imports
from gc3_query.lib.export_delegates.mongodb import storage_adapter_init


class IaaSServiceModelDynamicDocument(DynamicDocument):
    connection_config = storage_adapter_init()


class IaaSServiceModelEmbeddedDocument(EmbeddedDocument):
    pass

