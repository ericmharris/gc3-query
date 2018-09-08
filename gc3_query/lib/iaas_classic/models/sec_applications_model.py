# -*- coding: utf-8 -*-

"""
gc3-query.sec_applications_model    [9/7/2018 9:52 PM]
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

import mongoengine
from mongoengine import *

SecApplication = dict(
    description='Permit public access to https administration port',
    dport='8989',
    icmpcode='',
    icmptype='',
    id='5fe5214b-66e5-4ef6-8295-90fe853a3728',
    name='/Compute-587626604/mayurnath.gokare@oracle.com/paas/JaaS/gc3ntagrogr604/lb/ora_ahttps-587626604/mayurnath.gokare@oracle.com/paas/JaaS/gc3ntagrogr604/lb/tresources',
    protocol='tcp',
    uri='https://compute.uscom-central-1.oraclecloud.com/secapplication/Compute-587626604/mayurnath.gokare%40oracle.com/paas/JaaS/gc3ntagrogr604/lb/ora_ahttps-587626604/mayurnath.gokare%40oracle.com/paas/JaaS/gc3ntagrogr604/lb/tresources',
    value1=8989,
    value2=-1)
sec_application_dict = {
    'description': 'Permit public access to https administration port',
    'dport': '8989',
    'icmpcode': '',
    'icmptype': '',
    'name': '/Compute-587626604/mayurnath.gokare@oracle.com/paas/JaaS/gc3ntagrogr604/lb/ora_ahttps-587626604/mayurnath.gokare@oracle.com/paas/JaaS/gc3ntagrogr604/lb/tresources',
    'protocol': 'tcp',
    'uri': 'https://compute.uscom-central-1.oraclecloud.com/secapplication/Compute-587626604/mayurnath.gokare%40oracle.com/paas/JaaS/gc3ntagrogr604/lb/ora_ahttps-587626604/mayurnath.gokare%40oracle.com/paas/JaaS/gc3ntagrogr604/lb/tresources',
    'value1': 8989,
    'value2': -1,
    'id': '5fe5214b-66e5-4ef6-8295-90fe853a3728'
}


class SecApplicationModel(DynamicDocument):
    """


{
    "result": [
        {
            "protocol": "tcp",
            "description": "Permit public access to https administration port",
            "uri": "https://compute.uscom-central-1.oraclecloud.com/secapplication/Compute-587626604/mayurnath.gokare%40oracle.com/paas/JaaS/gc3ntagrogr604/lb/ora_ahttps-587626604/mayurnath.gokare%40oracle.com/paas/JaaS/gc3ntagrogr604/lb/tresources",
            "icmptype": "",
            "value2": -1,
            "value1": 8989,
            "dport": "8989",
            "icmpcode": "",
            "id": "5fe5214b-66e5-4ef6-8295-90fe853a3728",
            "name": "/Compute-587626604/mayurnath.gokare@oracle.com/paas/JaaS/gc3ntagrogr604/lb/ora_ahttps-587626604/mayurnath.gokare@oracle.com/paas/JaaS/gc3ntagrogr604/lb/tresources"
        },
        {
            "protocol": "tcp",
            "description": "NGINX Proxy",
            "uri": "https://compute.uscom-central-1.oraclecloud.com/secapplication/Compute-587626604/ramesh.dadhania%40oracle.com/paas/BDCSCE/rdbdcstest/1/bdcsce/ora_nginx-587626604/ramesh.dadhania%40oracle.com/paas/BDCSCE/rdbdcstest/1/bdcsce/tresources",
            "icmptype": "",
            "value2": -1,
            "value1": 1080,
            "dport": "1080",
            "icmpcode": "",
            "id": "5a6568ed-2240-46fd-969b-9d5555b036f2",
            "name": "/Compute-587626604/ramesh.dadhania@oracle.com/paas/BDCSCE/rdbdcstest/1/bdcsce/ora_nginx-587626604/ramesh.dadhania@oracle.com/paas/BDCSCE/rdbdcstest/1/bdcsce/tresources"
        },
    ]
}



    """

    id = StringField(primary_key=True)
    account = StringField()
    description = StringField()

    application = StringField()
    disabled = BooleanField()
    dst_is_ip = BooleanField()
    dst_list = StringField()
    name = StringField()
    src_is_ip = BooleanField()
    src_list = StringField()
    uri = StringField()

    # meta = {'db_alias': 'iaas'}

    meta = {
        "db_alias": gc3_cfg.iaas_classic.mongodb.alias,
        "collection": "SecApplications",
        "indexes": [
            "name",
            "application",
            "action",
            "dst_is_ip",
            "src_is_ip",
            'disabled',
        ],
    }
