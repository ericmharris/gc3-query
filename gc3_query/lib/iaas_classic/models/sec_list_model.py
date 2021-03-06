# -*- coding: utf-8 -*-

"""
gc3-query.sec_list_model    [9/7/2018 3:24 PM]
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

################################################################################
## Third-Party Imports

################################################################################
## Project Imports
# from gc3_query.lib.gc3logging import get_logging
import mongoengine
from mongoengine import *
from gc3_query.lib.open_api.swagger_formats.models.three_part_name_model import ThreePartNameModel
from gc3_query.lib.open_api.swagger_formats.three_part_name_formats import ThreePartNameFormat

class SecListModel(DynamicDocument):
    """



res = {
    'account': '/Compute-587626604/default',
    'description': 'Security list for admin host of OTD component',
    'name': '/Compute-587626604/eric.harris@oracle.com/paas/JaaS/NAAC-CDMT-D03-JCS/lb/ora_otd_infraadmin',
    'outbound_cidr_policy': 'PERMIT',
    'policy': 'DENY',
    'uri': 'https://compute.uscom-central-1.oraclecloud.com/seclist/Compute-587626604/eric.harris%40oracle.com/paas/JaaS/NAAC-CDMT-D03-JCS/lb/ora_otd_infraadmin',
    'group_id': 22606,
    'id': 'af82692e-72d7-44d7-8394-fdbd6a612d2c'
}



{
    "result": [
    {
        "account": "/Compute-587626604/default",
        "description": "Security list for admin host of OTD component",
        "uri": "https://compute.uscom-central-1.oraclecloud.com/seclist/Compute-587626604/eric.harris%40oracle.com/paas/JaaS/NAAC-CDMT-D03-JCS/lb/ora_otd_infraadmin",
        "outbound_cidr_policy": "PERMIT",
        "policy": "DENY",
        "group_id": "22606",
        "id": "af82692e-72d7-44d7-8394-fdbd6a612d2c",
        "name": "/Compute-587626604/eric.harris@oracle.com/paas/JaaS/NAAC-CDMT-D03-JCS/lb/ora_otd_infraadmin"
    },
    {
        "account": "/Compute-587626604/default",
        "description": "PeopleSoft related SL",
        "uri": "https://compute.uscom-central-1.oraclecloud.com/seclist/Compute-587626604/eric.harris%40oracle.com/GC3NAACCDMT_PSFT",
        "outbound_cidr_policy": "PERMIT",
        "policy": "DENY",
        "group_id": "44529",
        "id": "8f423b75-5ebc-4536-b5e1-9926e0dd61c3",
        "name": "/Compute-587626604/eric.harris@oracle.com/GC3NAACCDMT_PSFT"
    },


SecList = dict(
    account='/Compute-587626604/default',
    description='Security list for admin host of OTD component',
    group_id=22606,
    id='af82692e-72d7-44d7-8394-fdbd6a612d2c',
    name=
    '/Compute-587626604/eric.harris@oracle.com/paas/JaaS/NAAC-CDMT-D03-JCS/lb/ora_otd_infraadmin',
    outbound_cidr_policy='PERMIT',
    policy='DENY',
    uri=
    'https://compute.uscom-central-1.oraclecloud.com/seclist/Compute-587626604/eric.harris%40oracle.com/paas/JaaS/NAAC-CDMT-D03-JCS/lb/ora_otd_infraadmin'
)


    """
    account = StringField()
    description = StringField()
    group_id = IntField()
    id = UUIDField(primary_key=True)
    name = EmbeddedDocumentField(ThreePartNameModel)
    outbound_cidr_policy = StringField()
    policy = StringField()
    uri = URLField()

    # meta = {'db_alias': 'iaas'}

    meta = {
        "db_alias": gc3_cfg.iaas_classic.mongodb.alias,
        "collection": "SecLists",
        "indexes": [
            "name",
            "group_id",
        ],
    }

    def __init__(self, *args, **values):
        values['name'] = ThreePartNameModel.from_result(values)
        super().__init__(*args, **values)
        _debug(f"{self.__class__.__name__}.__init__(args={args}, values={values}):")
