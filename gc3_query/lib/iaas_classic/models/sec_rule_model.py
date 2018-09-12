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
# from gc3_query.lib.gc3logging import get_logging
import mongoengine
from mongoengine import *
from gc3_query.lib.open_api.swagger_formats.models.three_part_name_model import ThreePartNameModel
from gc3_query.lib.open_api.swagger_formats.three_part_name_formats import ThreePartNameFormat
from gc3_query.lib import get_logging

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


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

    action = StringField()
    application = StringField()
    description = StringField()
    disabled = BooleanField()
    dst_is_ip = BooleanField()
    # dst_list = StringField()
    # dst_list = DynamicField()
    dst_list = DictField()
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

    src_is_ip = BooleanField()
    # src_list = StringField()
    # src_list = DynamicField()
    src_list = DictField()
    uri = URLField()

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

    def __init__(self, *args, **values):
        _name: ThreePartNameFormat = values['name']
        values['name'] = ThreePartNameModel(name=_name.name,
                                            idm_service_instance_id=_name.idm_service_instance_id,
                                            object_owner=_name.object_owner,
                                            object_name=_name.object_name,
                                            idm_domain_name=_name.idm_domain_name)
        values['dst_list'] = values['dst_list'].__dict__
        values['src_list'] = values['src_list'].__dict__
        super().__init__(*args, **values)
        _debug(f"{self.__class__.__name__}.__init__(args={args}, values={values}):")
