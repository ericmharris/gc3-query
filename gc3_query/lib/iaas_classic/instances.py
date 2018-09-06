# -*- coding: utf-8 -*-

"""
#@Filename : instances
#@Date : [7/30/2018 9:25 AM]
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

from sortedcontainers import SortedDict
from bravado.response import  BravadoResponse, BravadoResponseMetadata

################################################################################
## Project Imports
from gc3_query.lib import *
from gc3_query.lib.iaas_classic.iaas_responses import IaaSServiceResponse
from . import IaaSServiceBase
from .iaas_requests_http_client import IaaSRequestsHTTPClient

from gc3_query.lib import get_logging

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


class Instances(IaaSServiceBase):

    def __init__(self, service_cfg: Dict[str, Any], idm_cfg: Dict[str, Any], http_client: IaaSRequestsHTTPClient = None,
                 from_url: bool = False, export_delegates: List[str] = None, **kwargs: Dict[str, Any]):
        super().__init__(service_cfg=service_cfg,
                         idm_cfg=idm_cfg,
                         http_client=http_client,
                         from_url=from_url,
                         export_delegates=export_delegates,
                         **kwargs)
        _debug(f"{self.service_name} created using service_cfg: {self.service_cfg}")

    def get_instance_details(self, name: str, swagger_client_config: DictStrAny = None) -> IaaSServiceResponse:
        """

        :return:
        """
        container = f"{self.idm_container_name}/"
        # http_future = self.bravado_service_operations.getInstance(name=name)
        # http_future = self.bravado_service_operations.getInstance(name=container)
        http_future = self.service_operations.list_instance(container=name)
        request_url = http_future.future.request.url
        service_response = http_future.response()
        result_json = service_response.incoming_response.json()
        r = SortedDict(result_json['result'][0])
        # result = service_response.result
        # http_response = service_response.incoming_response
        instance_details = IaaSServiceResponse(service_response=service_response)
        return instance_details




    def get_instance(self, name: str, swagger_client_config: DictStrAny = None) -> BravadoResponse:
        """

        :return:
        """
        http_future = self.service_operations.list_instance(container=name)
        request_url = http_future.future.request.url
        service_response = http_future.response()
        result_json = service_response.incoming_response.json()
        r = SortedDict(result_json['result'][0])
        # result = service_response.result
        # http_response = service_response.incoming_response
        return service_response










    def get_all_instances(self):
        """

        r = SortedDict({
            'account': '/Compute-587626604/default',
            'attributes': {
                'sshkeys': [
                    'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDkl16+TS1DB5jFwxr8tRMfztjLCHK2+wpfqy2eKeUzDJx8oGlasmBTAdwPX9cH3bfPRLJzru6SG2fJWsow4sU0d2clcwLRtqVdFMAdA3MSpIqayQMQJJ7NE5omkucF0pf0RG2p5cT3mBZDw/9IrSKnIAzaescUi72QOtcVSVgOiBcvJeQVn75GFQ0+JVKnVooh4pL2xDwTUj4EeSn5aLSA4ycqpBqvFFzrGsfDjDn55HiL0Dwwo9uM6VasAPHatqVIRA4EXGMu+QU6iw0m75e5n5CzEoL5ut4D2Og6MqrAVHTmtwf3WhPlDIzLu5OZbILydPq3/u58g6IVUHeB/wBd',
                    'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDMvQhtNg2BmrGoKZVtChz6TFyy53KuB09L5SsmnbQxzM6C0PNfH1TwsG7p/emWOhc6jB2KFxdkuM/Q4BD9PreuFPN37FU5D1cIWKB8yPub3kTVJf1g5PkF1HsoG5vjf3tbUdB6I+pclMiV8tXPXBWA64wtfXc9g6dZSNvg4JDYh8J5eOul5Jct4QK9juA9pZNI7fOeYcT2z4PdmwYDkj517Ei47wX2xSM6++wM2+AkOPP2f6EZYaOQdex68in3R1g5T0rBfqPF1+7KRdPaP5c+s/ASqeFmitf7+/BQZa+9Em/F6EOoDwWbhAAFzJBidjzwWv+E+fsEbUjrWrBFB5Bkd3j2s3ojfTxDoLo+GzGrZtxuL4CcwWVTe98gRvRj7vRwTX8JIJfvKiJCkDPUZlW0Kxwysn6wZVXWLHnjf7c4NcMXJc5mdihtGTxGyZDyR4NLyoLGatN5ZAdYpiztkYxqxyWRrLT8DANZeWi0w+EdE0JAuvVyyBajV+FczHkViGY0xVm4SjcfFDz8KrByaEn/3ioZd6tK6ahFy/aT+N+cqu0xeFjPDOyxfQ7qtufbq/yJ0XktISBumVvBMOv7MbDXiUmqHlqP2pbw6V1XXqSIw6/Jsi4/9NeRPSjLbNvem3RFzAbxXIOiNlQKl+e03jCkDZ3pNFQ81RQhgegmhOtQqw=='
                ],
                'oracle_metadata': {
                    'v1': {
                        'object':
                            '/Compute-587626604/eric.harris@oracle.com/gc3_naac_soar_ebs1226_demo_01/instance',
                        'orchestration':
                            '/Compute-587626604/eric.harris@oracle.com/gc3_naac_soar_ebs1226_demo_01'
                    }
                },
                'network': {
                    'nimbula_vcable-eth0': {
                        'vethernet_id':
                            '0',
                        'vethernet':
                            '/oracle/public/default',
                        'address': ['c6:b0:24:5b:b3:4a', '10.19.6.118'],
                        'model':
                            '',
                        'vethernet_type':
                            'vlan',
                        'id':
                            '/Compute-587626604/eric.harris@oracle.com/48e894f3-2984-4089-99b2-237da9775e9f',
                        'dhcp_options': []
                    }
                },
                'dns': {
                    'domain':
                        'compute-587626604.oraclecloud.internal.',
                    'hostname':
                        'gc3-naac-soar-ebs1226-demo-01.compute-587626604.oraclecloud.internal.',
                    'nimbula_vcable-eth0':
                        'gc3-naac-soar-ebs1226-demo-01.compute-587626604.oraclecloud.internal.'
                },
                'nimbula_orchestration':
                    '/Compute-587626604/eric.harris@oracle.com/gc3_naac_soar_ebs1226_demo_01'
            },
            'availability_domain': '/uscom-central-1a',
            'boot_order': [1], 'desired_state':
                'running',
            'disk_attach':
                '',
            'domain':
                'compute-587626604.oraclecloud.internal.',
            'entry':
                None,
            'error_reason':
                '',
            'fingerprint':
                '5c:80:b0:fb:bc:c5:bb:13:7c:a5:92:1b:53:96:b2:cc',
            'hostname':
                'gc3-naac-soar-ebs1226-demo-01.compute-587626604.oraclecloud.internal.',
            'hypervisor': {
                'mode': 'hvm'
            },
            'image_format':
                'raw',
            'image_metadata_bag':
                '/oracle/machineimage_metadata/40fd26b4106b48e989a2ca1b1f90e923',
            'imagelist':
                None,
            'ip':
                '10.19.6.118',
            'label':
                'OPC_OL6_8_EBS_1226_VISION_SINGLE_20180615175635',
            'name':
                '/Compute-587626604/eric.harris@oracle.com/gc3_naac_soar_ebs1226_demo_01/8706cea9-6f49-428f-b354-a3748478d1c2',
            'networking': {
                'eth0': {
                    'model':
                        '',
                    'seclists': [
                        '/Compute-587626604/eric.harris@oracle.com/gc3_naac_soar_seclist_01'
                    ],
                    'dns': [
                        'gc3-naac-soar-ebs1226-demo-01.compute-587626604.oraclecloud.internal.'
                    ],
                    'vethernet':
                        '/oracle/public/default',
                    'nat':
                        'ipreservation:/Compute-587626604/eric.harris@oracle.com/gc3_naac_soar_ip02'
                }
            },
            'placement_requirements': [
                '/system/compute/placement/default',
                '/oracle/compute/dedicated/fcbaed9f-242b-42ce-ac77-dd727f9710eb',
                '/system/compute/allow_instances'
            ],
            'platform':
                'linux',
            'priority':
                '/oracle/public/default',
            'quota':
                '/Compute-587626604',
            'quota_reservation':
                None,
            'relationships': [],
            'resolvers':
                None,
            'reverse_dns':
                True,
            'shape':
                'oc4',
            'site':
                '',
            'sshkeys': [
                '/Compute-587626604/eric.harris@oracle.com/gc3_naac_soar',
                '/Compute-587626604/eric.harris@oracle.com/eric_harris-cloud-01'
            ],
            'start_time':
                '2018-06-16T01:00:17Z',
            'state':
                'running',
            'storage_attachments': [{
                'index':
                    1,
                'storage_volume_name':
                    '/Compute-587626604/eric.harris@oracle.com/gc3_naac_soar_ebs1226_demo_01_storage',
                'name':
                    '/Compute-587626604/eric.harris@oracle.com/gc3_naac_soar_ebs1226_demo_01/8706cea9-6f49-428f-b354-a3748478d1c2/5b499dc8-2b5f-4f7f-9779-c0c52a6059cd'
            }],
            'tags': ['naac', 'soar', 'EBS', 'EBS 12.2.6'],
            'uri':
                'https://compute.uscom-central-1.oraclecloud.com/instance/Compute-587626604/eric.harris%40oracle.com/gc3_naac_soar_ebs1226_demo_01/8706cea9-6f49-428f-b354-a3748478d1c2',
            'vcable_id':
                '/Compute-587626604/eric.harris@oracle.com/48e894f3-2984-4089-99b2-237da9775e9f',
            'virtio':
                None,
            'vnc':
                '10.19.6.117:5900'
        })

        :return:
        """
        container = f"{self.idm_container_name}/"
        http_future = self.service_operations.list_instance(container=container)
        request_url = http_future.future.request.url
        service_response = http_future.response()
        result_json = service_response.incoming_response.json()
        r = SortedDict(result_json['result'][0])
        return service_response.result

    def dump(self):
        container = f"{self.idm_container_name}/"
        http_future = self.service_operations.list_instance(container=container)
        request_url = http_future.future.request.url
        service_response = http_future.response()
        return service_response
