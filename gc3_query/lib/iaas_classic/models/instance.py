# -*- coding: utf-8 -*-

"""
#@Filename : instances
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
import mongoengine

################################################################################
## Project Imports
from gc3_query.lib import *
from gc3_query.lib.iaas_classic import IaaSServiceResult
from gc3_query.lib.models.gc3_meta_data import GC3MetaData
from gc3_query.lib.gc3logging import get_logging

from . import IaaSServiceModelDynamicDocument, IaaSServiceModelEmbeddedDocument

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


class Instance(IaaSServiceModelDynamicDocument):
    # gc3_meta_data = mongoengine.EmbeddedDocumentField(GC3MetaData, required=True)
    # make = mongoengine.StringField(required=True)
    # year = mongoengine.IntField(required=True)
    # mileage = mongoengine.IntField(default=0)
    # vi_number = mongoengine.StringField(default=lambda: str(uuid.uuid4()).replace("-", ''))
    #
    # engine = mongoengine.EmbeddedDocumentField(Engine, required=True)
    # service_history = mongoengine.EmbeddedDocumentListField(ServiceRecord)
    #
    # # no need to reference owners here, that is entirely contained in owner class
    domain = mongoengine.StringField()
    placement_requirements = ["/system/compute/placement/default", "/oracle/compute/dedicated/fcbaed9f-242b-42ce-ac77-dd727f9710eb",
                              "/system/compute/allow_instances", ]
    ip = mongoengine.StringField()
    fingerprint = mongoengine.StringField()
    image_metadata_bag = mongoengine.StringField()
    site = mongoengine.StringField()
    shape = mongoengine.StringField()
    image_format = mongoengine.StringField()
    relationships = []
    availability_domain = mongoengine.StringField()
    hostname = mongoengine.StringField()
    disk_attach = mongoengine.StringField()
    label = mongoengine.StringField()
    priority = mongoengine.StringField()
    platform = mongoengine.StringField()
    state = mongoengine.StringField()
    vnc = mongoengine.StringField()
    desired_state = mongoengine.StringField()
    # tags = ["naac", "soar", "EBS", "EBS 12.2.6", ]
    tags = mongoengine.ListField()
    start_time = mongoengine.DateTimeField()
    quota = mongoengine.StringField()
    error_reason = mongoengine.StringField()
    # sshkeys = ["/Compute-587626604/eric.harris@oracle.com/gc3_naac_soar",
    #            "/Compute-587626604/eric.harris@oracle.com/eric_harris-cloud-01", ]
    sshkeys = mongoengine.ListField()
    account = mongoengine.StringField()
    name = mongoengine.StringField()
    vcable_id = mongoengine.StringField()
    uri = mongoengine.StringField()
    reverse_dns = mongoengine.BooleanField()
    boot_order = mongoengine.ListField()

    meta = {
        "db_alias": IaaSServiceModelDynamicDocument.connection_config["name"],
        "collection": __name__,
        "indexes": [
            "account",
            "name",
            "ip",
            "start_time",
            "sshkeys",
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

    def __init__(self, instance_details: IaaSServiceResult,  *args, **values):
        super().__init__(*args, **values)
        _debug(f"{self.__class__.__name__}.__init__(args={args}, values={values}):")
