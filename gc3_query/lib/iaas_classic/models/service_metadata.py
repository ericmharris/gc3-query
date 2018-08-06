# -*- coding: utf-8 -*-

"""
#@Filename : service_metadata
#@Date : [8/6/2018 11:29 AM]
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
import mongoengine

################################################################################
## Project Imports
from gc3_query.lib import *
from gc3_query.lib.iaas_classic.iaas_responses import IaaSServiceResponse
from gc3_query.lib.models.gc3_meta_data import GC3MetaData
from gc3_query.lib.gc3logging import get_logging

from . import IaaSServiceModelDynamicDocument, IaaSServiceModelEmbeddedDocument

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

class ServiceMetadata(mongoengine.DynamicEmbeddedDocument):
    username = mongoengine.StringField(default=cfg.username)
    identity_domain = mongoengine.StringField(default=cfg.identity_domain)
    region = mongoengine.StringField(default=cfg.region)
    rest_endpoint = mongoengine.StringField(default=cfg.rest_endpoint)

    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        _debug(f"{self.__class__.__name__}.__init__(args={args}, values={values}):")
        self.username: str = "eric.harris@oracle.com"
        self.identity_domain: str = "gc30003"
        self.region: str = "us2"
        self.rest_endpoint: str = "gc30003"
