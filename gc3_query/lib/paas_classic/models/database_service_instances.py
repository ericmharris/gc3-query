# -*- coding: utf-8 -*-

"""
gc3-query.database_service_instances    [8/24/2018 12:00 PM]
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
from . import *

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

"""
    view-all-instances-services-array-item:
        title: services Array Item
        x-model: DBInstance
        type: object
        properties:
            backup_supported_version:
                type: string
                description: The version of cloud tooling for backup and recovery
                    supported by the service instance.
            created_by:
                type: string
                description: The user name of the Oracle Cloud user who created the
                    service instance.
            creation_time:
                type: string
                format: paas-date-time
                description: The date-and-time stamp when the service instance was
                    created.
            description:
                type: string
                description: The description of the service instance, if one was provided
                    when the instance was created.
            identity_domain:
                type: string
                description: The identity domain housing the service instance.
            last_modified_time:
                type: string
                format: paas-date-time
                description: The date-and-time stamp when the service instance was
                    last modified.
            service_name:
                type: string
                description: The name of the service instance.
            service_uri:
                type: string
                description: The REST endpoint URI of the service instance.
            sm_plugin_version:
                type: string
                description: The version of the cloud tooling service manager plugin
                    supported by the service instance.
            status:
                type: string
                description: 'The status of the service instance:<ul><li><code>Configured</code>:
                    the service instance has been configured.</li><li><code>In Progress</code>:
                    the service instance is being created.</li><li><code>Maintenance</code>:
                    the service instance is being stopped, started, restarted or scaled.</li><li><code>Running</code>:
                    the service instance is running.</li><li><code>Stopped</code>:
                    the service instance is stopped.</li><li><code>Terminating</code>:
                    the service instance is being deleted.</li></ul>'
            version:
                type: string
                description: The Oracle Database version on the service instance.
"""

data = {'backup_supported_version': '16.2.3',
        'created_by': 'dhiru.vallabhbhai@oracle.com',
        'creation_time': '2018-02-13T18:52:10.094+0000',
        'description': 'NA-TAG OCS Demo',
        'identity_domain': 'gc30003',
        'last_modified_time': '2018-02-13T19:19:29.713+0000',
        'legacy': True,
        'service_name': 'gc3ntagocsd801',
        'service_uri': 'https://dbaas.oraclecloud.com:443/paas/service/dbcs/api/v1.1/instances/gc30003/gc3ntagocsd801',
        'service_uuid': 'AC1008FB65E7401DB45237D2677BED15',
        'sm_plugin_version': '18.1.2-556',
        'status': 'Running',
        'version':'11.2.0.4',
        "items":'[],"totalResults":0,"hasMore":false}',   # Missing from spec
        'tools_version': '18.1.2-556',                  # Missing from spec
        }

class DatabaseServiceInstancesModel(DynamicDocument):
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
    # dst_is_ip = StringField()
    # src_is_ip = StringField()
    # dst_list = StringField()
    # name = StringField()
    # src_list = StringField()
    # uri = URLField()
    # disabled = BooleanField()
    # application = StringField()
    # action = StringField()
    # sec_rule_id = StringField()
    # description = StringField()
    backup_supported_version = StringField()
    created_by = StringField()
    creation_time = DateTimeField()
    description = StringField()
    identity_domain = StringField()
    last_modified_time = DateTimeField()
    legacy = BooleanField()
    service_name = StringField()
    service_uri = URLField()
    # service_uuid = StringField()
    service_uuid = UUIDField()
    sm_plugin_version = StringField()
    status = StringField()
    version = StringField()
    items = ListField(StringField())
    tools_version = StringField()
    legacy =  BooleanField()


    meta = {
    "db_alias": gc3_cfg.paas_classic.mongodb.db_alias,
    "collection": "DatabaseServiceInstances",
    "indexes": [
        "created_by",
        "service_name",
        "service_uuid",
        "creation_time",
        "identity_domain",
        "legacy",
        'version',
    ],
    }


    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        _debug(f"{self.__class__.__name__}.__init__(args={args}, values={values}):")