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
from gc3_query.lib import *
# from gc3_query.lib.gc3logging import get_logging
from . import *

from gc3_query.lib import get_logging

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

Instance_response = dict(
    account='/Compute-587626604/default',
    attributes={
        'nodelist':
            '',
        'cdb':
            'yes',
        'service_name':
            'DBCS_DEFAULT',
        'flashback_days':
            '1',
        'gg':
            'no',
        'tfa_autocollect':
            'no',
        'managed':
            'no',
        'net_security_integrity_checksum_level':
            'required',
        'automem':
            'yes',
        'fra_mnt':
            '/u03',
        'tmpl_sysauxsz':
            '2000MB',
        'demo_user':
            'oracle',
        'tmpl_logsz':
            '1000MB',
        'lsnr_port':
            '1521',
        'tde_ks_login':
            'auto',
        'pdbss':
            'no',
        'sshkeys': [
            'ssh-dss AAAAB3NzaC1kc3MAAACBAP1/U4EddRIpUt9KnC7s5Of2EbdSPO9EAMMeP4C2USZpRV1AIlH7WT2NWPq/xfW6MPbLm1Vs14E7gB00b/JmYLdrmVClpJ+f6AR7ECLCT7up1/63xhv4O1fnxqimFQ8E+4P208UewwI1VBNaFpEy9nXzrith1yrv8iIDGZ3RSAHHAAAAFQCXYFCPFSMLzLKSuYKi64QL8Fgc9QAAAIEA9+GghdabPd7LvKtcNrhXuXmUr7v6OuqC+VdMCz0HgmdRWVeOutRZT+ZxBxCBgLRJFnEj6EwoFhO3zwkyjMim4TwWeotUfI0o4KOuHiuzpnWRbqN/C/ohNWLx+2J6ASQ7zKTxvqhRkImog9/hWuWfBpKLZl6Ae1UlZAFMO/7PSSoAAACALlpBKkIhh8juIvyuuBMpheIzxS1HYNu+0kLp7xv0rHWgN4+tmOOZPkeD4SeJ5HAHpXzkFM5OdrTdbI0ote/SUVYupT4OBcilElIhJ6yUiLuCHJRC+9+y6T2+DKxaREmzoMoDmVxkY6QqGLyKjM9rRrNyt1O0FOObaQ56phYNYQA=',
            'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDMvQhtNg2BmrGoKZVtChz6TFyy53KuB09L5SsmnbQxzM6C0PNfH1TwsG7p/emWOhc6jB2KFxdkuM/Q4BD9PreuFPN37FU5D1cIWKB8yPub3kTVJf1g5PkF1HsoG5vjf3tbUdB6I+pclMiV8tXPXBWA64wtfXc9g6dZSNvg4JDYh8J5eOul5Jct4QK9juA9pZNI7fOeYcT2z4PdmwYDkj517Ei47wX2xSM6++wM2+AkOPP2f6EZYaOQdex68in3R1g5T0rBfqPF1+7KRdPaP5c+s/ASqeFmitf7+/BQZa+9Em/F6EOoDwWbhAAFzJBidjzwWv+E+fsEbUjrWrBFB5Bkd3j2s3ojfTxDoLo+GzGrZtxuL4CcwWVTe98gRvRj7vRwTX8JIJfvKiJCkDPUZlW0Kxwysn6wZVXWLHnjf7c4NcMXJc5mdihtGTxGyZDyR4NLyoLGatN5ZAdYpiztkYxqxyWRrLT8DANZeWi0w+EdE0JAuvVyyBajV+FczHkViGY0xVm4SjcfFDz8KrByaEn/3ioZd6tK6ahFy/aT+N+cqu0xeFjPDOyxfQ7qtufbq/yJ0XktISBumVvBMOv7MbDXiUmqHlqP2pbw6V1XXqSIw6/Jsi4/9NeRPSjLbNvem3RFzAbxXIOiNlQKl+e03jCkDZ3pNFQ81RQhgegmhOtQqw=='
        ],
        'dbdns':
            'gc3-naac-soar-d05-dbcs',
        'dg_vm_names':
            '',
        'init_params':
            '',
        'oidm_nbr_of_hash_prtn_prty':
            '4',
        'net_security_encryption_target':
            'server',
        'opc_datacenter':
            'usdc2',
        'bkup_cron_entry':
            'yes',
        'dv':
            'no',
        'bkup_disk':
            'yes',
        'dbname':
            'ORCL',
        'psu':
            'default',
        'gfish':
            'no',
        'oidm_nbr_of_hash_prtn_bsns_unt_key':
            '4',
        'managed_uri':
            'https://storage.us2.oraclecloud.com/v1/dbaastest-usoracle05695/dbaas_managed/dbaasm/configure_dbaasm.pl',
        'bkup_oss_recovery_window':
            '30',
        'shared_oh_dbname':
            '',
        'upgrade_apex':
            'no',
        'dbmac':
            'nonexa',
        'oidm_intvl_prtn_start_dt':
            '2013-01-01',
        'dg_observer':
            'no',
        'em':
            'yes',
        'domain':
            'DBCS_DEFAULT',
        'net_security_integrity_enable':
            'yes',
        'bkup_use_rcat':
            'no',
        'net_security_enable':
            'yes',
        'net_security_integrity_methods':
            'SHA1',
        'oidm_nbr_of_hash_prtn_accs_mthd':
            '4',
        'ohome_owner':
            'oracle',
        'libopc_mode':
            'prod',
        'flashback':
            'yes',
        'network': {
            'nimbula_vcable-eth0': {
                'vethernet_id':
                    '0',
                'vethernet':
                    '/oracle/public/default',
                'address': ['c6:b0:24:a4:f9:50', '10.19.11.70'],
                'model':
                    '',
                'vethernet_type':
                    'vlan',
                'id':
                    '/Compute-587626604/eric.harris@oracle.com/c5a88c6b-e036-4510-8a73-1e76e9c8c582',
                'dhcp_options': []
            }
        },
        'tmpl_systemsz':
            '2000MB',
        'dg_ssh_pub':
            '\n',
        'version':
            '12201',
        'dg_config':
            'no',
        'oidm_cl_nbr_yrs':
            '5',
        'bkup_oss':
            'yes',
        'redo_log_size':
            '1024M',
        'data_mnt':
            '/u02',
        'setupparams':
            ' -alist=prep sda dbda tde netcc bkup ords tfa',
        'pdb_name':
            'PDB1',
        'oidm_nbr_of_hash_prtn_sku_key':
            '4',
        'demo_uri':
            'https://storage.us2.oraclecloud.com/v1/dbcsswlibp-usoracle29538/pdb_demo/demo.pl',
        'dg_syncmode':
            'ASYNC',
        'bp':
            'default',
        'nid':
            'yes',
        'bp_url':
            '',
        'dg_scan_ips':
            '',
        'ore':
            'no',
        'nimbula_orchestration':
            '/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-soar-d05-dbcs/db_1/vm-1',
        'asm':
            'false',
        'dg_uniq_names':
            '',
        'ords_config':
            'yes',
        'tde_action':
            'config',
        'bkup_cfg_files':
            'yes',
        'oidm_nbr_of_hash_prtn_agrmnt':
            '4',
        'redo_mnt':
            '/u04',
        'dg_network':
            'nat',
        'bp_update':
            'no',
        'vols':
            '(bits:60gb data:100gb fra:170gb redo:25gb)',
        'oidm_nbr_of_hash_prtn_fnl_rdng':
            '4',
        'redo':
            '25G',
        'setupdb':
            'yes',
        'bkup_daily_time':
            '',
        'fra':
            '170G',
        'tmpl_blksz':
            '8K',
        'service':
            'dbcs',
        'dg_drsite':
            'no',
        'ncharset':
            'AL16UTF16',
        'oidm':
            'no',
        'oidm_nbr_of_hash_prtn_org':
            '4',
        'oidm_nbr_of_hash_prtn_srvc_qnty':
            '4',
        'setup_rcat':
            'no',
        'bits':
            '60G',
        'ibkp_config':
            'no',
        'dns': {
            'domain':
                'compute-587626604.oraclecloud.internal.',
            'hostname':
                'gc3-naac-soar-d05-dbcs.compute-587626604.oraclecloud.internal.',
            'nimbula_vcable-eth0':
                'gc3-naac-soar-d05-dbcs.compute-587626604.oraclecloud.internal.'
        },
        'tfa':
            'yes',
        'dg_ssh_priv':
            '\n',
        'net_security_encryption_methods':
            'AES256,AES192,AES128',
        'bkup_disk_recovery_window':
            '7',
        'bits_mnt':
            '/u01',
        'net_security_integrity_target':
            'server',
        'oidm_nbr_of_hash_prtn_cust':
            '4',
        'edition':
            'enterprise',
        'archlog':
            'yes',
        'hdg':
            'no',
        'dbca_vars':
            '-characterSet AL32UTF8 -initParams filesystemio_options=setall,db_files=500',
        'dg_observer_zone':
            'primary',
        'hpages':
            'no',
        'net_security_encryption_type':
            'required',
        'lvm':
            'yes',
        'byol':
            'no',
        'dborch_version':
            '5.0.23.17.02',
        'demo':
            'no',
        'dbkey':
            '',
        'bkup_cfg_recovery_window':
            '30',
        'opcm':
            'no',
        'timezone':
            'UTC',
        'tmpl_tempsz':
            '1000MB',
        'oidm_nbr_of_hash_prtn_mtr_rdng':
            '4',
        'vol_index':
            'no',
        'dbtype':
            'si',
        'charset':
            'AL32UTF8',
        'oidm_wk_strt_day':
            'MONDAY',
        'oidm_nbr_of_hash_prtn_acct':
            '4',
        'dg_observer_user':
            'oracle',
        'flashback_minutes':
            '1440',
        'build':
            'no',
        'sid':
            'ORCL',
        'psu_url':
            '',
        'clone':
            'no',
        'managed_user':
            'root',
        'bkup_nfs':
            'no',
        'bundle':
            'basic',
        'tmpl_dbrecoverydestsize':
            '',
        'oidm_user':
            'oracle',
        'psm_oss_url':
            '',
        'ohome_name':
            '',
        'data':
            '100G',
        'reduced_volumes':
            'no',
        'oidm_uri':
            'https://storage.us2.oraclecloud.com/v1/dbcsswlibd-usoracle13098/OIDM/oidm_install.sh',
        'dg_connect_aliases':
            '',
        'dg_observer_exists':
            'no',
        'oidm_nbr_of_hash_prtn_init_rdng':
            '4',
        'oidm_cl_strt_dt':
            '2013-01-01',
        'net_security_encryption_enable':
            'yes',
        'sm':
            'yes',
        'bkup_nfs_recovery_window':
            '30'
    },
    availability_domain='/uscom-central-1a',
    boot_order=[1],
    desired_state='running',
    disk_attach='',
    domain='compute-587626604.oraclecloud.internal.',
    entry=None,
    error_reason='',
    fingerprint='cf:55:af:7a:c1:3c:af:13:b5:79:e7:b8:19:61:f2:ec',
    hostname='gc3-naac-soar-d05-dbcs.compute-587626604.oraclecloud.internal.',
    hypervisor={'mode': 'hvm'},
    image_format='raw',
    image_metadata_bag=
    '/oracle/machineimage_metadata/c256ea3f213c4ff18f3a831414d99f4b',
    imagelist=None,
    ip='10.19.11.70',
    label='gc3-naac-soar-d05-dbcs db_1 1',
    name=
    '/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-soar-d05-dbcs/db_1/vm-1/57cced1d-c74f-41da-9c24-e86666eee4b2',
    networking={
        'eth0': {
            'model':
                '',
            'seclists': [
                '/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-soar-d05-dbcs/db_1/ora_db',
                '/Compute-587626604/eric.harris@oracle.com/gc3_naac_soar_seclist_01'
            ],
            'dns':
                ['gc3-naac-soar-d05-dbcs.compute-587626604.oraclecloud.internal.'],
            'vethernet':
                '/oracle/public/default',
            'nat':
                'ipreservation:/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-soar-d05-dbcs/db_1/vm-1/ipreservation'
        }
    },
    placement_requirements=[
        '/system/compute/placement/default',
        '/oracle/compute/dedicated/fcbaed9f-242b-42ce-ac77-dd727f9710eb',
        '/system/compute/allow_instances'
    ],
    platform='linux',
    priority='/oracle/public/default',
    quota='/Compute-587626604',
    quota_reservation=None,
    relationships=[],
    resolvers=None,
    reverse_dns=True,
    shape='oc4',
    site='',
    sshkeys=[
        '/Compute-587626604/eric.harris@oracle.com/dbaas.gc3-naac-soar-d05-dbcs.DB.ora_user',
        '/Compute-587626604/eric.harris@oracle.com/dbaas.gc3-naac-soar-d05-dbcs.DB.ora_tools'
    ],
    start_time="<MayaDT epoch=1531344546.0>",
    state='running',
    storage_attachments=[{
        'index':
            1,
        'storage_volume_name':
            '/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-soar-d05-dbcs/db_1/vm-1/boot',
        'name':
            '/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-soar-d05-dbcs/db_1/vm-1/57cced1d-c74f-41da-9c24-e86666eee4b2/2bdf7705-4dc9-48ad-a703-9e5afb4edf86'
    }, {
        'index':
            2,
        'storage_volume_name':
            '/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-soar-d05-dbcs/db_1/vm-1/redo',
        'name':
            '/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-soar-d05-dbcs/db_1/vm-1/57cced1d-c74f-41da-9c24-e86666eee4b2/2cf31d8b-2f86-4898-a62e-7c69ffb8a5ee'
    }, {
        'index':
            3,
        'storage_volume_name':
            '/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-soar-d05-dbcs/db_1/vm-1/fra',
        'name':
            '/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-soar-d05-dbcs/db_1/vm-1/57cced1d-c74f-41da-9c24-e86666eee4b2/36a98b4a-1e85-449c-aac1-b3b423baff6b'
    }, {
        'index':
            4,
        'storage_volume_name':
            '/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-soar-d05-dbcs/db_1/vm-1/bits',
        'name':
            '/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-soar-d05-dbcs/db_1/vm-1/57cced1d-c74f-41da-9c24-e86666eee4b2/31890970-9e74-4a2a-bc8c-20af59179e23'
    }, {
        'index':
            5,
        'storage_volume_name':
            '/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-soar-d05-dbcs/db_1/vm-1/data',
        'name':
            '/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-soar-d05-dbcs/db_1/vm-1/57cced1d-c74f-41da-9c24-e86666eee4b2/1f819ae4-e28c-42ac-9818-8c8fc1c6092a'
    }],
    tags=[
        'ORA.DCS', 'ORA.DB', 'ORA.DCS.PAAS.EE.HOURLY',
        '/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-soar-d05-dbcs/db_1/vm-1',
        '078783786aa35e455be7f3c4085f72f9'
    ],
    uri=
    'https://compute.uscom-central-1.oraclecloud.com/instance/Compute-587626604/eric.harris%40oracle.com/dbaas/gc3-naac-soar-d05-dbcs/db_1/vm-1/57cced1d-c74f-41da-9c24-e86666eee4b2',
    vcable_id=
    r'/Compute-587626604/eric.harris@oracle.com/c5a88c6b-e036-4510-8a73-1e76e9c8c582',
    virtio=None,
    vnc='10.19.11.69:5900')


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
