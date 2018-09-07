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
#from gc3_query.lib.gc3logging import get_logging
import mongoengine
from mongoengine import *




class SecListModel(DynamicDocument):
    """
    SecList = dict(
        account='/Compute-587626604/default',
        description='Security list for admin host of OTD component',
        group_id='22606',
        id='af82692e-72d7-44d7-8394-fdbd6a612d2c',
        name='/Compute-587626604/eric.harris@oracle.com/paas/JaaS/NAAC-CDMT-D03-JCS/lb/ora_otd_infraadmin',
        outbound_cidr_policy='PERMIT',
        policy='DENY',
        uri='https://compute.uscom-central-1.oraclecloud.com/seclist/Compute-587626604/eric.harris%40oracle.com/paas/JaaS/NAAC-CDMT-D03-JCS/lb/ora_otd_infraadmin')


       {'result': [
  {'account': '/Compute-587626604/default',
   'description': 'Security list for admin host of OTD component',
   'uri': 'https://compute.uscom-central-1.oraclecloud.com/seclist/Compute-587626604/eric.harris%40oracle.com/paas/JaaS/NAAC-CDMT-D03-JCS/lb/ora_otd_infraadmin',
   'outbound_cidr_policy': 'PERMIT',
   'policy': 'DENY',
   'group_id': '22606',
   'id': 'af82692e-72d7-44d7-8394-fdbd6a612d2c',
   'name': '/Compute-587626604/eric.harris@oracle.com/paas/JaaS/NAAC-CDMT-D03-JCS/lb/ora_otd_infraadmin'},
  {'account': '/Compute-587626604/default',
   'description': 'PeopleSoft related SL',
   'uri': 'https://compute.uscom-central-1.oraclecloud.com/seclist/Compute-587626604/eric.harris%40oracle.com/GC3NAACCDMT_PSFT',
   'outbound_cidr_policy': 'PERMIT',
   'policy': 'DENY',
   'group_id': '44529',
   'id': '8f423b75-5ebc-4536-b5e1-9926e0dd61c3',
   'name': '/Compute-587626604/eric.harris@oracle.com/GC3NAACCDMT_PSFT'},
     {'account': '/Compute-587626604/default',
   'description': 'Security list of OTD vms',
   'uri': 'https://compute.uscom-central-1.oraclecloud.com/seclist/Compute-587626604/manjunath.udupa%40oracle.com/paas/JaaS/gc3gc3hsamp502/lb/ora_otd',
   'outbound_cidr_policy': 'PERMIT',
   'policy': 'DENY',
   'group_id': '6128',
   'id': '9a6704f4-90a6-4594-870b-d0af44d66d42',
   'name': '/Compute-587626604/manjunath.udupa@oracle.com/paas/JaaS/gc3gc3hsamp502/lb/ora_otd'}]}





    """

    id=StringField(primary_key=True)
    account=StringField()
    description=StringField()

    application=StringField()
    disabled=BooleanField()
    dst_is_ip=BooleanField()
    dst_list=StringField()
    name=StringField()
    src_is_ip=BooleanField()
    src_list=StringField()
    uri=StringField()

    # meta = {'db_alias': 'iaas'}

    meta = {
    "db_alias": gc3_cfg.iaas_classic.mongodb.alias,
    "collection": "SecLists",
    "indexes": [
        "name",
        "application",
        "action",
        "dst_is_ip",
        "src_is_ip",
        'disabled',
    ],
    }

