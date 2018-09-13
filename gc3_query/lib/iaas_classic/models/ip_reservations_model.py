# -*- coding: utf-8 -*-

"""
gc3-query.ip_reservations_model    [9/13/2018 10:39 AM]
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


from gc3_query.lib import *
# from gc3_query.lib.gc3logging import get_logging
import mongoengine
from mongoengine import *
from gc3_query.lib.open_api.swagger_formats.three_part_name_formats import ThreePartNameFormat
from gc3_query.lib.open_api.swagger_formats.sec_lists_formats import SecIPListFormat, SecListFormat
from gc3_query.lib.open_api.swagger_formats.models.three_part_name_model import ThreePartNameModel
from gc3_query.lib.open_api.swagger_formats.models.sec_ip_list_model import SecIPListFormatModel
from gc3_query.lib.open_api.swagger_formats.models.sec_list_model import SecListFormatModel
from gc3_query.lib import get_logging

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


class IPReservationModel(DynamicDocument):
    """
ip_reservation = dict(
   account='/Compute-587626604/default',
   ip='129.150.219.3',
   name=ThreePartNameFormat('/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-soar-d02-dbcs/db_1/vm-1/ipreservation'),
   parentpool='/oracle/public/ippool',
   permanent=True,
   quota=None,
   tags=[],
   uri='https://compute.uscom-central-1.oraclecloud.com/ip/reservation/Compute-587626604/eric.harris%40oracle.com/dbaas/gc3-naac-soar-d02-dbcs/db_1/vm-1/ipreservation',
   used=True)
{
   "result": [
       {
           "account": "/Compute-587626604/default",
           "used": true,
           "name": "/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-soar-d02-dbcs/db_1/vm-1/ipreservation",
           "tags": [],
           "ip": "129.150.219.3",
           "uri": "https://compute.uscom-central-1.oraclecloud.com/ip/reservation/Compute-587626604/eric.harris%40oracle.com/dbaas/gc3-naac-soar-d02-dbcs/db_1/vm-1/ipreservation",
           "quota": null,
           "parentpool": "/oracle/public/ippool",
           "permanent": true
       },
       {
           "account": "/Compute-587626604/default",
           "used": true,
           "name": "/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-ntag-pod1-d01-jcsdb/db_1/vm-1/ipreservation",
           "tags": [],
           "ip": "129.150.194.191",
           "uri": "https://compute.uscom-central-1.oraclecloud.com/ip/reservation/Compute-587626604/eric.harris%40oracle.com/dbaas/gc3-ntag-pod1-d01-jcsdb/db_1/vm-1/ipreservation",
           "quota": null,
           "parentpool": "/oracle/public/ippool",
           "permanent": true
       },
    """
    account = StringField()
    ip = StringField()
    name = EmbeddedDocumentField(ThreePartNameModel)
    parentpool=StringField()
    permanent=BooleanField()
    quota = StringField()
    tags = ListField(StringField())
    uri = URLField()
    used=BooleanField()

    meta = {
        "db_alias": gc3_cfg.iaas_classic.mongodb.alias,
        "collection": "IPReservations",
        "indexes": [
            "name",
            "ip",
            'used',
        ],
    }

    def __init__(self, *args, **values):
        values['name'] = ThreePartNameModel.from_result(values)
        super().__init__(*args, **values)
        _debug(f"{self.__class__.__name__}.__init__(args={args}, values={values}):")