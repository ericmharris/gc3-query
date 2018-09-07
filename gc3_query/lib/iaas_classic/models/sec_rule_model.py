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
# from mongoengine import *
import mongoengine

from gc3_query.lib import get_logging
_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

# sec_rule_example = dict(
#     action='PERMIT',
#     application='/oracle/public/ssh',
#     description='DO NOT MODIFY: Permit PSM to ssh to admin host',
#     disabled=False,
#     dst_is_ip=False,
#     dst_list='seclist:/Compute-587626604/mayurnath.gokare@oracle.com/paas/SOA/gc3ntagrogr605/lb/ora_otd_infraadmin',
#     id='bfc39682-3929-4635-9834-e95b8ba7c2c2',
#     name='/Compute-587626604/mayurnath.gokare@oracle.com/paas/SOA/gc3ntagrogr605/lb/sys_infra2otd_admin_ssh',
#     src_is_ip=True,
#     src_list='seciplist:/oracle/public/paas-infra',
#     uri='https://compute.uscom-central-1.oraclecloud.com/secrule/Compute-587626604/mayurnath.gokare%40oracle.com/paas/SOA/gc3ntagrogr605/lb/sys_infra2otd_admin_ssh')

class SecRuleModel(mongoengine.DynamicDocument):
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

first_result_dict = {
    'action': 'PERMIT',
    'application': '/oracle/public/ssh',
    'description': 'DO NOT MODIFY: Permit PSM to ssh to admin host',
    'disabled': False,
    'dst_list': 'seclist:/Compute-587626604/mayurnath.gokare@oracle.com/paas/SOA/gc3ntagrogr605/lb/ora_otd_infraadmin',
    'name': '/Compute-587626604/mayurnath.gokare@oracle.com/paas/SOA/gc3ntagrogr605/lb/sys_infra2otd_admin_ssh',
    'src_list': 'seciplist:/oracle/public/paas-infra',
    'uri': 'https://compute.uscom-central-1.oraclecloud.com/secrule/Compute-587626604/mayurnath.gokare%40oracle.com/paas/SOA/gc3ntagrogr605/lb/sys_infra2otd_admin_ssh',
    'id': 'bfc39682-3929-4635-9834-e95b8ba7c2c2',
    'dst_is_ip': False,
    'src_is_ip': True
}
    """

    action=mongoengine.fields.StringField()
    application=mongoengine.StringField()
    description=mongoengine.StringField()
    disabled=mongoengine.BooleanField()
    dst_is_ip=mongoengine.BooleanField()
    dst_list=mongoengine.StringField()
    id=mongoengine.StringField(primary_key=True)
    name=mongoengine.StringField()
    src_is_ip=mongoengine.BooleanField()
    src_list=mongoengine.StringField()
    uri=mongoengine.StringField()

    # meta = {'db_alias': 'iaas'}

    meta = {
    "db_alias": gc3_cfg.iaas_classic.mongodb.alias,
    "collection": "SecRules",
    "indexes": [
        "name",
        "application",
        "action",
        "dst_is_ip",
        "src_is_ip",
        'disabled',
    ],
    }

    # def __init__(self, *args, **values):
    #     super().__init__(*args, **values)
    #     _debug(f"{self.__class__.__name__}.__init__(args={args}, values={values}):")
