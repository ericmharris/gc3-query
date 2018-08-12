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
import sys, os

################################################################################
## Third-Party Imports
from dataclasses import dataclass
import mongoengine
from mongoengine import DynamicDocument, Document, DynamicEmbeddedDocument, EmbeddedDocument

################################################################################
## Project Imports
from gc3_query.lib import *
from gc3_query.lib.iaas_classic.iaas_responses import IaaSServiceResponse
from gc3_query.lib.models.gc3_meta_data import GC3MetaData
from gc3_query.lib.gc3logging import get_logging
from . import IaaSServiceModelDynamicDocument, IaaSServiceModelEmbeddedDocument
from . import *

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


class InstanceModel(DynamicDocument):
    """
    domain = "compute-587626604.oraclecloud.internal."
    placement_requirements = [ "/system/compute/placement/default", "/oracle/compute/dedicated/fcbaed9f-242b-42ce-ac77-dd727f9710eb", "/system/compute/allow_instances",]
    ip = "10.19.6.118"
    fingerprint = "5c:80:b0:fb:bc:c5:bb:13:7c:a5:92:1b:53:96:b2:cc"
    image_metadata_bag = "/oracle/machineimage_metadata/40fd26b4106b48e989a2ca1b1f90e923"
    site = ""
    shape = "oc4"
    image_format = "raw"
    relationships = []
    availability_domain = "/uscom-central-1a"
    hostname = "gc3-naac-soar-ebs1226-demo-01.compute-587626604.oraclecloud.internal."
    disk_attach = ""
    label = "OPC_OL6_8_EBS_1226_VISION_SINGLE_20180615175635"
    priority = "/oracle/public/default"
    platform = "linux"
    state = "running"
    vnc = "10.19.6.117:5900"
    desired_state = "running"
    tags = [ "naac", "soar", "EBS", "EBS 12.2.6",]
    start_time = "2018-06-16T01:00:17Z"
    quota = "/Compute-587626604"
    error_reason = ""
    sshkeys = [ "/Compute-587626604/eric.harris@oracle.com/gc3_naac_soar", "/Compute-587626604/eric.harris@oracle.com/eric_harris-cloud-01",]
    account = "/Compute-587626604/default"
    name = "/Compute-587626604/eric.harris@oracle.com/gc3_naac_soar_ebs1226_demo_01/8706cea9-6f49-428f-b354-a3748478d1c2"
    vcable_id = "/Compute-587626604/eric.harris@oracle.com/48e894f3-2984-4089-99b2-237da9775e9f"
    uri = "https://compute.uscom-central-1.oraclecloud.com/instance/Compute-587626604/eric.harris%40oracle.com/gc3_naac_soar_ebs1226_demo_01/8706cea9-6f49-428f-b354-a3748478d1c2"
    reverse_dns = true
    boot_order = [ 1,]
    [[storage_attachments]]
    index = 1
    storage_volume_name = "/Compute-587626604/eric.harris@oracle.com/gc3_naac_soar_ebs1226_demo_01_storage"
    name = "/Compute-587626604/eric.harris@oracle.com/gc3_naac_soar_ebs1226_demo_01/8706cea9-6f49-428f-b354-a3748478d1c2/5b499dc8-2b5f-4f7f-9779-c0c52a6059cd"

    [hypervisor]
    mode = "hvm"

    [attributes]
    sshkeys = [ "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDkl16+TS1DB5jFwxr8tRMfztjLCHK2+wpfqy2eKeUzDJx8oGlasmBTAdwPX9cH3bfPRLJzru6SG2fJWsow4sU0d2clcwLRtqVdFMAdA3MSpIqayQMQJJ7NE5omkucF0pf0RG2p5cT3mBZDw/9IrSKnIAzaescUi72QOtcVSVgOiBcvJeQVn75GFQ0+JVKnVooh4pL2xDwTUj4EeSn5aLSA4ycqpBqvFFzrGsfDjDn55HiL0Dwwo9uM6VasAPHatqVIRA4EXGMu+QU6iw0m75e5n5CzEoL5ut4D2Og6MqrAVHTmtwf3WhPlDIzLu5OZbILydPq3/u58g6IVUHeB/wBd", "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDMvQhtNg2BmrGoKZVtChz6TFyy53KuB09L5SsmnbQxzM6C0PNfH1TwsG7p/emWOhc6jB2KFxdkuM/Q4BD9PreuFPN37FU5D1cIWKB8yPub3kTVJf1g5PkF1HsoG5vjf3tbUdB6I+pclMiV8tXPXBWA64wtfXc9g6dZSNvg4JDYh8J5eOul5Jct4QK9juA9pZNI7fOeYcT2z4PdmwYDkj517Ei47wX2xSM6++wM2+AkOPP2f6EZYaOQdex68in3R1g5T0rBfqPF1+7KRdPaP5c+s/ASqeFmitf7+/BQZa+9Em/F6EOoDwWbhAAFzJBidjzwWv+E+fsEbUjrWrBFB5Bkd3j2s3ojfTxDoLo+GzGrZtxuL4CcwWVTe98gRvRj7vRwTX8JIJfvKiJCkDPUZlW0Kxwysn6wZVXWLHnjf7c4NcMXJc5mdihtGTxGyZDyR4NLyoLGatN5ZAdYpiztkYxqxyWRrLT8DANZeWi0w+EdE0JAuvVyyBajV+FczHkViGY0xVm4SjcfFDz8KrByaEn/3ioZd6tK6ahFy/aT+N+cqu0xeFjPDOyxfQ7qtufbq/yJ0XktISBumVvBMOv7MbDXiUmqHlqP2pbw6V1XXqSIw6/Jsi4/9NeRPSjLbNvem3RFzAbxXIOiNlQKl+e03jCkDZ3pNFQ81RQhgegmhOtQqw==",]
    nimbula_orchestration = "/Compute-587626604/eric.harris@oracle.com/gc3_naac_soar_ebs1226_demo_01"

    [metadata]
    elapsed_time = 1.343999999999141
    is_fallback_result = false
    processing_end_time = 11023.078
    request_elapsed_time = 1.343999999999141
    request_end_time = 11023.078
    start_time = 11021.734
    status_code = 200
    username = "eric.harris@oracle.com"

    [networking.eth0]
    model = ""
    seclists = [ "/Compute-587626604/eric.harris@oracle.com/gc3_naac_soar_seclist_01",]
    dns = [ "gc3-naac-soar-ebs1226-demo-01.compute-587626604.oraclecloud.internal.",]
    vethernet = "/oracle/public/default"
    nat = "ipreservation:/Compute-587626604/eric.harris@oracle.com/gc3_naac_soar_ip02"

    [attributes.dns]
    domain = "compute-587626604.oraclecloud.internal."
    hostname = "gc3-naac-soar-ebs1226-demo-01.compute-587626604.oraclecloud.internal."
    nimbula_vcable-eth0 = "gc3-naac-soar-ebs1226-demo-01.compute-587626604.oraclecloud.internal."

    [attributes.oracle_metadata.v1]
    object = "/Compute-587626604/eric.harris@oracle.com/gc3_naac_soar_ebs1226_demo_01/instance"
    orchestration = "/Compute-587626604/eric.harris@oracle.com/gc3_naac_soar_ebs1226_demo_01"

    [attributes.network.nimbula_vcable-eth0]
    vethernet_id = "0"
    vethernet = "/oracle/public/default"
    address = [ "c6:b0:24:5b:b3:4a", "10.19.6.118",]
    model = ""
    vethernet_type = "vlan"
    id = "/Compute-587626604/eric.harris@oracle.com/48e894f3-2984-4089-99b2-237da9775e9f"
    dhcp_options = []

    """
    domain = StringField()
    placement_requirements = ListField()
    ip = StringField()
    fingerprint = StringField()
    image_metadata_bag = StringField()
    site = StringField()
    shape = StringField()
    imagelist = StringField()  # seems to come back None
    image_format = StringField()
    relationships = ListField()
    availability_domain = StringField()
    networking = DictField()
    storage_attachments = ListField()

    hostname = StringField()

    disk_attach = StringField()
    label = StringField()
    priority = StringField()
    platform = StringField()
    state = StringField()
    # virtio = StringField()    #  Its returned as a None, nothing in the spec about it
    vnc = StringField()
    desired_state = StringField()
    tags = ListField()
    start_time = DateTimeField()
    quota = StringField()
    # quota_reservation = StringField()     #  Its returned as a None, nothing in the spec about it
    entry = IntField()
    error_reason = StringField()
    sshkeys = ListField()
    resolvers = ListField()
    account = StringField()
    name = StringField()
    vcable_id = StringField()
    hypervisor = DictField()
    uri = StringField()
    reverse_dns = BooleanField()
    attributes = DictField()
    boot_order = ListField(IntField())
    metadata = DictField()

    meta = {
        "db_alias": gc3_cfg.mongodb.db_alias,
        "collection": "Instances",
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
