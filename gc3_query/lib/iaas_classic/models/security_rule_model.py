# -*- coding: utf-8 -*-

"""
#@Filename : security_rules_model
#@Date : [8/8/2018 12:20 PM]
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


class SecurityRuleModel(DynamicDocument):
    """
data = {'name': '/Compute-587626604/manjunath.udupa@oracle.com/paas/JaaS/gc3oladdoam726/wls/ora_p2admin_ahttps',
        'uri': 'https://compute.uscom-central-1.oraclecloud.com:443/network/v1/secrule/Compute-587626604/manjunath.udupa@oracle.com/paas/JaaS/gc3oladdoam726/wls/ora_p2admin_ahttps',
        'description': None,
        'tags': [],
        'acl': '/Compute-587626604/manjunath.udupa@oracle.com/paas/JaaS/gc3oladdoam726/wls/ora_acl_default',
        'flowDirection': 'ingress',
        'srcVnicSet': None,
        'dstVnicSet': '/Compute-587626604/manjunath.udupa@oracle.com/paas/JaaS/gc3oladdoam726/wls/ora_admin',
        'srcIpAddressPrefixSets': [],
        'dstIpAddressPrefixSets': [],
        'secProtocols': ['/Compute-587626604/manjunath.udupa@oracle.com/paas/JaaS/gc3oladdoam726/wls/ahttps'],
        'enabledFlag': False}
    """
    name = StringField()
    uri = URLField()
    description = StringField()
    tags = ListField()
    acl = StringField()
    flowDirection = StringField()
    srcVnicSet = StringField()
    dstVnicSet = StringField()
    srcIpAddressPrefixSets = ListField(field=StringField)
    dstIpAddressPrefixSets = ListField(field=StringField)
    secProtocols = ListField()
    enabledFlag = BooleanField()






    placement_requirements = mongoengine.ListField()
    ip = mongoengine.StringField()
    fingerprint = mongoengine.StringField()
    image_metadata_bag = mongoengine.StringField()
    site = mongoengine.StringField()
    shape = mongoengine.StringField()
    image_format = mongoengine.StringField()
    relationships = mongoengine.ListField()
    availability_domain = mongoengine.StringField()
    hostname = mongoengine.StringField()
    disk_attach = mongoengine.StringField()
    label = mongoengine.StringField()
    priority = mongoengine.StringField()
    platform = mongoengine.StringField()
    state = mongoengine.StringField()
    vnc = mongoengine.StringField()
    desired_state = mongoengine.StringField()
    tags = mongoengine.ListField()
    start_time = mongoengine.DateTimeField()
    quota = mongoengine.StringField()
    error_reason = mongoengine.StringField()
    sshkeys = mongoengine.ListField()
    account = mongoengine.StringField()
    name = mongoengine.StringField()
    vcable_id = mongoengine.StringField()
    uri = mongoengine.StringField()
    reverse_dns = mongoengine.BooleanField()
    boot_order = mongoengine.ListField(mongoengine.IntField())
    # attributes = mongoengine.DictField(mongoengine.StringField())
    # metadata = mongoengine.DictField()

    meta = {
        "db_alias": gc3_cfg.mongodb.db_alias,
        "collection": "SecurityRules",
        "indexes": [
            "account",
            "name",
            "ip",
            'fingerprint',
            "start_time",
            "sshkeys",
            "tags",
        ],
    }


    def __init__(self, data: DictStrAny, metadata: DictStrAny, embedded_data: DictStrAny, **kwargs):
        # kwargs['sec_rule_id'] = kwargs.pop('id')
        self.data = data
        self.metadata = metadata
        self.embedded_data = embedded_data
        super().__init__(**data)
        _debug(f"{self.__class__.__name__} created")

    # def __init__(self, *args, **kwargs):
    #     _debug(f"{self.__class__.__name__}: created")
    #     _fields = ['domain',
    #                'placement_requirements',
    #                'ip',
    #                'fingerprint',
    #                'image_metadata_bag',
    #                'site',
    #                'shape',
    #                'imagelist',
    #                'image_format',
    #                'relationships',
    #                'availability_domain',
    #                'storage_attachments',
    #                'hostname',
    #                'quota_reservation',
    #                'disk_attach',
    #                'label',
    #                'priority',
    #                'platform',
    #                'state',
    #                'virtio',
    #                'vnc',
    #                'desired_state',
    #                'tags',
    #                'start_time',
    #                'quota',
    #                'entry',
    #                'error_reason',
    #                'sshkeys',
    #                'resolvers',
    #                'account',
    #                'vcable_id',
    #                'uri',
    #                'reverse_dns',
    #                # 'attributes',
    #                #    'networking',
    #                # 'metadata',
    #                #    'hypervisor',
    #                'boot_order',
    #                'name'
    #                ]
    #
    #     data = {k: v for k, v in kwargs.items() if k in _fields}
    #     _debug(f'data={data}')
    #     super().__init__(**data)
    #     _debug('asdf')
    #
    #
