# -*- coding: utf-8 -*-

"""
gc3-query.sec_ip_lists_model.py    [9/8/2018 1:24 PM]
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
from gc3_query.lib.open_api.swagger_formats.three_part_name_formats import ThreePartNameFormat
from gc3_query.lib.open_api.swagger_formats.models.three_part_name_model import ThreePartNameModel

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

import mongoengine
from mongoengine import *

SecIPList_response = dict(
    description='DO NOT MODIFY: A secrule to allow specific IPs to connect to this db',
    group_id='20103',
    id='80c4cd5d-ffb7-4c11-bd50-574b3627e32f',
    name='/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-ntag-pod1-d03-soacsdb/db_1/ora_trusted_hosts_dblistener',
    secipentries=['127.0.0.1/32'],
    uri='https://compute.uscom-central-1.oraclecloud.com/seciplist/Compute-587626604/eric.harris%40oracle.com/dbaas/gc3-ntag-pod1-d03-soacsdb/db_1/ora_trusted_hosts_dblistener')




first_result_dict = {
    'description': 'DO NOT MODIFY: A secrule to allow specific IPs to connect to this db',
    'name': '/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-ntag-pod1-d03-soacsdb/db_1/ora_trusted_hosts_dblistener',
    'secipentries': ['127.0.0.1/32'],
    'uri': 'https://compute.uscom-central-1.oraclecloud.com/seciplist/Compute-587626604/eric.harris%40oracle.com/dbaas/gc3-ntag-pod1-d03-soacsdb/db_1/ora_trusted_hosts_dblistener',
    'id': '80c4cd5d-ffb7-4c11-bd50-574b3627e32f',
    'group_id': '20103'
}

class SecIPListsModel(DynamicDocument):
    """
{
    "result": [
        {
            "name": "/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-ntag-pod1-d03-soacsdb/db_1/ora_trusted_hosts_dblistener",
            "uri": "https://compute.uscom-central-1.oraclecloud.com/seciplist/Compute-587626604/eric.harris%40oracle.com/dbaas/gc3-ntag-pod1-d03-soacsdb/db_1/ora_trusted_hosts_dblistener",
            "secipentries": [
                "127.0.0.1/32"
            ],
            "group_id": "20103",
            "id": "80c4cd5d-ffb7-4c11-bd50-574b3627e32f",
            "description": "DO NOT MODIFY: A secrule to allow specific IPs to connect to this db"
        },
        {
            "name": "/Compute-587626604/seetharaman.nandyal@oracle.com/dbaas/GC3NAACNTSB003/db_1/ora_trusted_hosts_dblistener",
            "uri": "https://compute.uscom-central-1.oraclecloud.com/seciplist/Compute-587626604/seetharaman.nandyal%40oracle.com/dbaas/GC3NAACNTSB003/db_1/ora_trusted_hosts_dblistener",
            "secipentries": [
                "127.0.0.1/32"
            ],
            "group_id": "9813",
            "id": "6c746e92-2780-44c6-9b23-3de00f9ff994",
            "description": "DO NOT MODIFY: A secrule to allow specific IPs to connect to this db"
        },
        ]
        }


SecIPList_fixed = dict(
    description='DO NOT MODIFY: A secrule to allow specific IPs to connect to this db',
    group_id=20103,
    id='80c4cd5d-ffb7-4c11-bd50-574b3627e32f',
    name='/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-ntag-pod1-d03-soacsdb/db_1/ora_trusted_hosts_dblistener',
    secipentries=['127.0.0.1/32'],
    uri='https://compute.uscom-central-1.oraclecloud.com/seciplist/Compute-587626604/eric.harris%40oracle.com/dbaas/gc3-ntag-pod1-d03-soacsdb/db_1/ora_trusted_hosts_dblistener')

    """
    description = StringField()
    group_id = IntField()
    id = UUIDField(primary_key=True)

    # swagger_formats.multi_part_name_formats.ThreePartNameFormat converts name to
    # name =  {
    #     "name" : "/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-soar-d05-dbcs/db_1/vm-1/57cced1d-c74f-41da-9c24-e86666eee4b2",
    #     "idm_service_instance_id" : "587626604",
    #     "username" : "eric.harris@oracle.com",
    #     "object_name" : "/dbaas/gc3-naac-soar-d05-dbcs/db_1/vm-1/57cced1d-c74f-41da-9c24-e86666eee4b2",
    #     "idm_domain_name" : "gc30003" }
    # name = StringField()
    # name = DictField()
    name = EmbeddedDocumentField(ThreePartNameModel)
    multi_part_name = DictField()

    secipentries=ListField(StringField())
    uri = URLField()


    meta = {
        "db_alias": gc3_cfg.iaas_classic.mongodb.alias,
        "collection": "SecIPLists",
        "indexes": [
            "name",
            "group_id",
        ],
    }

    def __init__(self, *args, **values):
        _name: ThreePartNameFormat = values['name']
        values['name'] = ThreePartNameModel(full_name=_name.full_name,
                                            idm_service_instance_id=_name.idm_service_instance_id,
                                            object_owner=_name.object_owner,
                                            object_name=_name.object_name,
                                            idm_domain_name=_name.idm_domain_name)
        super().__init__(*args, **values)
        _debug(f"{self.__class__.__name__}.__init__(args={args}, values={values}):")
