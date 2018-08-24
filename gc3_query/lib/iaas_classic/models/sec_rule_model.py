# -*- coding: utf-8 -*-

"""
#@Filename : sec_rule_model
#@Date : [8/8/2018 1:00 PM]
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

################################################################################
## Project Imports
from gc3_query.lib import *
#from gc3_query.lib.gc3logging import get_logging
from . import *

from gc3_query.lib import get_logging
_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

data = dict(
    dst_is_ip='false',
    src_is_ip='true',
    dst_list='seclist:/Compute-587626604/mayurnath.gokare@oracle.com/paas/SOA/gc3ntagrogr605/lb/ora_otd_infraadmin',
    name='/Compute-587626604/mayurnath.gokare@oracle.com/paas/SOA/gc3ntagrogr605/lb/sys_infra2otd_admin_ssh',
    src_list='seciplist:/oracle/public/paas-infra',
    uri='https://compute.uscom-central-1.oraclecloud.com/secrule/Compute-587626604/mayurnath.gokare%40oracle.com/paas/SOA/gc3ntagrogr605/lb/sys_infra2otd_admin_ssh',
    disabled=False,
    application='/oracle/public/ssh',
    action='PERMIT',
    id='bfc39682-3929-4635-9834-e95b8ba7c2c2',
    description='DO NOT MODIFY: Permit PSM to ssh to admin host')

class SecRuleModel(DynamicDocument):
    """
    dst_is_ip   = 'false',
    src_is_ip   = 'true',
    dst_list    = 'seclist:/Compute-587626604/mayurnath.gokare@oracle.com/paas/SOA/gc3ntagrogr605/lb/ora_otd_infraadmin',
    name        = '/Compute-587626604/mayurnath.gokare@oracle.com/paas/SOA/gc3ntagrogr605/lb/sys_infra2otd_admin_ssh',
    src_list    = 'seciplist:/oracle/public/paas-infra',
    uri         = 'https://compute.uscom-central-1.oraclecloud.com/secrule/Compute-587626604/mayurnath.gokare%40oracle.com/paas/SOA/gc3ntagrogr605/lb/sys_infra2otd_admin_ssh',
    disabled    = False,
    application = '/oracle/public/ssh',
    action      = 'PERMIT',
    id          = 'bfc39682-3929-4635-9834-e95b8ba7c2c2',
    description = 'DO NOT MODIFY: Permit PSM to ssh to admin host'
    """
    dst_is_ip = StringField()
    src_is_ip = StringField()
    dst_list = StringField()
    name = StringField()
    src_list = StringField()
    uri = URLField()
    disabled = BooleanField()
    application = StringField()
    action = StringField()
    sec_rule_id = StringField()
    description = StringField()

    meta = {
        "db_alias": gc3_cfg.mongodb.db_alias,
        "collection": "SecRules",
        "indexes": [
            "sec_rule_id",
            "name",
            "src_list",
            'disabled',
            "action",
        ],
    }


    def __init__(self, data: DictStrAny, metadata: DictStrAny, embedded_data: DictStrAny, **kwargs):
        # kwargs['sec_rule_id'] = kwargs.pop('id')
        self.data = data
        self.metadata = metadata
        self.embedded_data = embedded_data
        super().__init__(**data)
        _debug(f"{self.__class__.__name__} created")

