# -*- coding: utf-8 -*-

"""
#@Filename : instances
#@Date : [7/30/2018 10:50 AM]
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
import datetime

from dateutil.tz import tzutc

from gc3_query.lib import *
from gc3_query.lib.open_api.swagger_formats.three_part_name_formats import ThreePartNameFormat
from gc3_query.lib.open_api.swagger_formats.models.three_part_name_model import ThreePartNameModel
# from gc3_query.lib.gc3logging import get_logging
from . import *

from gc3_query.lib import get_logging

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


class InstanceModel(DynamicDocument):
    """


    """
    # quota_reservation = StringField()     #  Its returned as a None, nothing in the spec about it
    # virtio = StringField()    #  Its returned as a None, nothing in the spec about it
    account = StringField()
    attributes = DictField()
    availability_domain = StringField()
    boot_order = ListField(IntField())
    desired_state = StringField()
    disk_attach = StringField()
    domain = StringField()
    entry = IntField()
    error_reason = StringField()
    fingerprint = StringField()
    hostname = StringField()
    hypervisor = DictField()
    image_format = StringField()
    image_metadata_bag = StringField()
    imagelist = StringField()  # seems to come back None
    ip = StringField()
    label = StringField()
    metadata = DictField()

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
    id = StringField(primary_key=True)

    networking = DictField()
    placement_requirements = ListField(StringField())
    platform = StringField()
    priority = StringField()
    quota = StringField()
    relationships = ListField()
    resolvers = ListField()
    reverse_dns = BooleanField()
    shape = StringField()
    site = StringField()
    sshkeys = ListField(StringField())
    start_time = DateTimeField()
    state = StringField()
    storage_attachments = ListField(DictField())
    tags = ListField(StringField())
    uri = URLField()
    vcable_id = StringField()
    vnc = StringField()

    meta = {
        "db_alias": gc3_cfg.iaas_classic.mongodb.alias,
        "collection": "Instances",
        "indexes": [
            "hostname",
            "ip",
            'fingerprint',
            "start_time",
            "sshkeys",
            "platform",
            "uri",
            "tags",
        ],
    }

    def __init__(self, *args, **values):
        """
    name =  {
    "name" : "/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-soar-d05-dbcs/db_1/vm-1/57cced1d-c74f-41da-9c24-e86666eee4b2",
    "idm_service_instance_id" : "587626604",
    "username" : "eric.harris@oracle.com",
    "object_name" : "/dbaas/gc3-naac-soar-d05-dbcs/db_1/vm-1/57cced1d-c74f-41da-9c24-e86666eee4b2",
    "idm_domain_name" : "gc30003" }

        :param args:
        :param values:
        """
        values['name'] = ThreePartNameModel.from_result(values)
        values['id'] = values['name'].full_name
        super().__init__(*args, **values)
        _debug(f"{self.__class__.__name__}.__init__(args={args}, values={values}):")
