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
import sys, os

################################################################################
## Third-Party Imports
from dataclasses import dataclass

from mongoengine import DynamicDocument, EmbeddedDocument

################################################################################
## Project Imports
from gc3_query.lib import *
from gc3_query.lib.storage_adapters.mongodb import storage_adapter_init


class IaaSServiceModelDynamicDocument(DynamicDocument):
    connection_config = storage_adapter_init()


class IaaSServiceModelEmbeddedDocument(EmbeddedDocument):
    pass

