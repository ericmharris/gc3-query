import datetime
from pathlib import Path

import pytest
from dateutil.tz import tzutc
from pymongo import MongoClient

from gc3_query.lib import gc3_cfg
from gc3_query.lib.export_delegates.mongodb import storage_adapter_init
from gc3_query.lib.gc3_config import GC3Config
from gc3_query.lib.iaas_classic import IaaSRequestsHTTPClient
from gc3_query.lib.iaas_classic.instances import Instances
from gc3_query.lib.iaas_classic.models.instance_model import InstanceModel
# fixme? from gc3_query.lib.open_api import API_SPECS_DIR
# from pprint import pprint, pformat

TEST_BASE_DIR: Path = Path(__file__).parent
# config_dir = TEST_BASE_DIR.joinpath("config")
config_dir = gc3_cfg.BASE_DIR.joinpath("etc/config")
output_dir = TEST_BASE_DIR.joinpath('output')


def test_setup():
    assert TEST_BASE_DIR.exists()
    # assert API_SPECS_DIR.exists()
    if not config_dir.exists():
        config_dir.mkdir()
    if not output_dir.exists():
        output_dir.mkdir()


@pytest.fixture()
def setup_gc30003():
    service = 'Instances'
    idm_domain = 'gc30003'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    idm_cfg = gc3_config.idm.domains[idm_domain]
    http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    connection_config = storage_adapter_init()
    assert service==service_cfg.name
    assert idm_domain==idm_cfg.name
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    yield service_cfg, idm_cfg, http_client, connection_config


def test_init(setup_gc30003):
    service_cfg, idm_cfg, http_client, connection_config = setup_gc30003
    instances = Instances(service_cfg=service_cfg, idm_cfg=idm_cfg, http_client=http_client)
    assert instances.http_client.skip_authentication==False
    assert instances.http_client.idm_domain_name==idm_cfg.name
    assert instances.http_client.auth_cookie_header is not None
    assert 'nimbula' in instances.http_client.auth_cookie_header['Cookie']


def test_get_instance_details(setup_gc30003):
    service_cfg, idm_cfg, http_client, connection_config = setup_gc30003
    instances = Instances(service_cfg=service_cfg, idm_cfg=idm_cfg, http_client=http_client)
    name = 'Compute-587626604/eric.harris@oracle.com/gc3_naac_soar_ebs1226_demo_01/8706cea9-6f49-428f-b354-a3748478d1c2/'
    instance_details = instances.get_instance_details(name=name)
    assert instance_details.domain == 'compute-587626604.oraclecloud.internal.'

    toml_path = output_dir.joinpath('test_get_instance_details.toml')
    toml_fd = instance_details.export(file_path=toml_path, format='toml', overwrite=True)
    assert toml_fd.exists()

    yaml_path = output_dir.joinpath('test_get_instance_details.yaml')
    yaml_fd = instance_details.export(file_path=yaml_path, format='yaml', overwrite=True)
    assert yaml_fd.exists()

    json_path = output_dir.joinpath('test_get_instance_details.json')
    json_fd = instance_details.export(file_path=json_path, format='json', overwrite=True)
    assert json_fd.exists()





@pytest.fixture()
def setup_gc30003_instances():
    service = 'Instances'
    idm_domain = 'gc30003'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    idm_cfg = gc3_config.idm.domains[idm_domain]
    http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    connection_config = storage_adapter_init()
    instances = Instances(service_cfg=service_cfg, idm_cfg=idm_cfg, http_client=http_client)
    assert service==service_cfg.name
    assert idm_domain==idm_cfg.name
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    yield service_cfg, idm_cfg, http_client, connection_config, instances


def test_instance_model_save(setup_gc30003_instances):
    service_cfg, idm_cfg, http_client, connection_config, instances = setup_gc30003_instances
    name = 'Compute-587626604/eric.harris@oracle.com/gc3_naac_soar_ebs1226_demo_01/8706cea9-6f49-428f-b354-a3748478d1c2/'
    service_response = instances.get_instance(name=name)
    # request_url = http_future.future.request.url
    # service_response = http_future.response()
    # result = service_response.result

    # instance_details = instances.get_instance_details(name=name)
    # assert instance_details.domain == 'compute-587626604.oraclecloud.internal.'
    # instance_model = InstanceModel(instance_details=instance_details)
    # # '/Compute-587626604/eric.harris@oracle.com/gc3_naac_soar_ebs1226_demo_01/8706cea9-6f49-428f-b354-a3748478d1c2'

    assert service_response.metadata.status_code==200
    results_json = service_response.incoming_response.json()['result']
    assert len(results_json) == 1
    result_json = results_json[0]
    instance_model = InstanceModel(**result_json)
    saved = instance_model.save()
    assert saved


def test_instances_model_save():
    service = 'Instances'
    idm_domain = 'gc30003'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    idm_cfg = gc3_config.idm.domains[idm_domain]
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    assert service==service_cfg.name
    assert idm_domain==idm_cfg.name
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    instances = Instances(service_cfg=service_cfg, idm_cfg=idm_cfg, from_url=True)

    # container=instances.idm_container_name.replace('/', '')
    # old_container=instances.idm_container_name

    # container='/Compute-587626604'
    # container='Compute-587626604'
    # container=instances.idm_root_container_name

    # http_future = instances.bravado_service_operations.listInstance(container=instances.idm_user_container_name)
    # http_future = instances.bravado_service_operations.listInstance(container=instances.idm_container_name)
    # http_future = instances.bravado_service_operations.listInstance(container=container)
    # http_future = instances.service_operations.discover_root_instance()
    service_response = instances.dump()
    result = service_response.result
    result_json = service_response.incoming_response.json()
    assert service_response.metadata.status_code==200
    # instance_model = InstanceModel(instance_details=instance_details)
    # # '/Compute-587626604/eric.harris@oracle.com/gc3_naac_soar_ebs1226_demo_01/8706cea9-6f49-428f-b354-a3748478d1c2'
    # assert instance_model.name==instance_details.name
    # saved = instance_model.save()
    # assert saved





@pytest.fixture()
def setup_gc30003_model():
    service = 'Instances'
    idm_domain = 'gc30003'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    service_cfg = gc3_config.iaas_classic.services.compute[service]
    idm_cfg = gc3_config.idm.domains[idm_domain]
    mongodb_connection: MongoClient = storage_adapter_init(mongodb_config=gc3_cfg.iaas_classic.mongodb.as_dict())
    iaas_service = Instances(service_cfg=service_cfg, idm_cfg=idm_cfg)
    assert service==service_cfg.name
    assert idm_domain==idm_cfg.name
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    yield service_cfg, idm_cfg, iaas_service, mongodb_connection


def test_dump(setup_gc30003_model):
    service_cfg, idm_cfg, iaas_service, mongodb_connection = setup_gc30003_model
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    service_response = iaas_service.dump()
    assert service_response.result
    result = service_response.result


def test_save_one(setup_gc30003_model):
    service_cfg, idm_cfg, iaas_service, mongodb_connection = setup_gc30003_model
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    service_response = iaas_service.dump()
    assert service_response.result
    result = service_response.result
    results = service_response.result.result
    result_dict = service_response.incoming_response.json()
    first_result = results[0]
    first_result_dict = first_result._as_dict()
    instance_model = InstanceModel(**first_result_dict)
    saved = instance_model.save()
    assert saved


def test_save_all(setup_gc30003_model):
    service_cfg, idm_cfg, iaas_service, mongodb_connection = setup_gc30003_model
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    service_response = iaas_service.dump()
    assert service_response.result
    results = service_response.result.result
    for result in results:
        result_dict = result._as_dict()
        instance_model = InstanceModel(**result_dict)
        saved = instance_model.save()



def test_insert_all(setup_gc30003_model):
    service_cfg, idm_cfg, iaas_service, mongodb_connection = setup_gc30003_model
    # http_client: IaaSRequestsHTTPClient = IaaSRequestsHTTPClient(idm_cfg=idm_cfg)
    service_response = iaas_service.dump()
    assert service_response.result
    results = service_response.result.result
    instances = [InstanceModel(**result._as_dict()) for result in results]
    _ = InstanceModel.objects().insert(instances)
    assert instances




Instance_response = dict(
    account='/Compute-587626604/default',
    attributes={
        'nodelist': '',
        'cdb': 'yes',
        'service_name': 'DBCS_DEFAULT',
        'flashback_days': '1',
        'gg': 'no',
        'tfa_autocollect': 'no',
        'managed': 'no',
        'net_security_integrity_checksum_level': 'required',
        'automem': 'yes',
        'fra_mnt': '/u03',
        'tmpl_sysauxsz': '2000MB',
        'demo_user': 'oracle',
        'tmpl_logsz': '1000MB',
        'lsnr_port': '1521',
        'tde_ks_login': 'auto',
        'pdbss': 'no',
        'sshkeys': ['ssh-dss AAAAB3NzaC1kc...', 'ssh-rsa AAAAB3NzaC1y... ='],
        'dbdns': 'gc3-naac-soar-d05-dbcs',
        'dg_vm_names': '',
        'init_params': '',
        'oidm_nbr_of_hash_prtn_prty': '4',
        'net_security_encryption_target': 'server',
        'opc_datacenter': 'usdc2',
        'bkup_cron_entry': 'yes',
        'dv': 'no',
        'bkup_disk': 'yes',
        'dbname': 'ORCL',
        'psu': 'default',
        'gfish': 'no',
        'oidm_nbr_of_hash_prtn_bsns_unt_key': '4',
        'managed_uri': 'https://storage.us2.oraclecloud.com/v1/dbaastest-usoracle05695/dbaas_managed/dbaasm/configure_dbaasm.pl',
        'bkup_oss_recovery_window': '30',
        'shared_oh_dbname': '',
        'upgrade_apex': 'no',
        'dbmac': 'nonexa',
        'oidm_intvl_prtn_start_dt': '2013-01-01',
        'dg_observer': 'no',
        'em': 'yes',
        'domain': 'DBCS_DEFAULT',
        'net_security_integrity_enable': 'yes',
        'bkup_use_rcat': 'no',
        'net_security_enable': 'yes',
        'net_security_integrity_methods': 'SHA1',
        'oidm_nbr_of_hash_prtn_accs_mthd': '4',
        'ohome_owner': 'oracle',
        'libopc_mode': 'prod',
        'flashback': 'yes',
        'network': {
            'nimbula_vcable-eth0': {
                'vethernet_id': '0',
                'vethernet': '/oracle/public/default',
                'address': ['c6:b0:24:a4:f9:50', '10.19.11.70'],
                'model': '',
                'vethernet_type': 'vlan',
                'id': '/Compute-587626604/eric.harris@oracle.com/c5a88c6b-e036-4510-8a73-1e76e9c8c582',
                'dhcp_options': []
            }
        },
        'tmpl_systemsz': '2000MB',
        'dg_ssh_pub': '\n',
        'version': '12201',
        'dg_config': 'no',
        'oidm_cl_nbr_yrs': '5',
        'bkup_oss': 'yes',
        'redo_log_size': '1024M',
        'data_mnt': '/u02',
        'setupparams': ' -alist=prep sda dbda tde netcc bkup ords tfa',
        'pdb_name': 'PDB1',
        'oidm_nbr_of_hash_prtn_sku_key': '4',
        'demo_uri': 'https://storage.us2.oraclecloud.com/v1/dbcsswlibp-usoracle29538/pdb_demo/demo.pl',
        'dg_syncmode': 'ASYNC',
        'bp': 'default',
        'nid': 'yes',
        'bp_url': '',
        'dg_scan_ips': '',
        'ore': 'no',
        'nimbula_orchestration': '/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-soar-d05-dbcs/db_1/vm-1',
        'asm': 'false',
        'dg_uniq_names': '',
        'ords_config': 'yes',
        'tde_action': 'config',
        'bkup_cfg_files': 'yes',
        'oidm_nbr_of_hash_prtn_agrmnt': '4',
        'redo_mnt': '/u04',
        'dg_network': 'nat',
        'bp_update': 'no',
        'vols': '(bits:60gb data:100gb fra:170gb redo:25gb)',
        'oidm_nbr_of_hash_prtn_fnl_rdng': '4',
        'redo': '25G',
        'setupdb': 'yes',
        'bkup_daily_time': '',
        'fra': '170G',
        'tmpl_blksz': '8K',
        'service': 'dbcs',
        'dg_drsite': 'no',
        'ncharset': 'AL16UTF16',
        'oidm': 'no',
        'oidm_nbr_of_hash_prtn_org': '4',
        'oidm_nbr_of_hash_prtn_srvc_qnty': '4',
        'setup_rcat': 'no',
        'bits': '60G',
        'ibkp_config': 'no',
        'dns': {
            'domain': 'compute-587626604.oraclecloud.internal.',
            'hostname': 'gc3-naac-soar-d05-dbcs.compute-587626604.oraclecloud.internal.',
            'nimbula_vcable-eth0': 'gc3-naac-soar-d05-dbcs.compute-587626604.oraclecloud.internal.'
        },
        'tfa': 'yes',
        'dg_ssh_priv': '\n',
        'net_security_encryption_methods': 'AES256,AES192,AES128',
        'bkup_disk_recovery_window': '7',
        'bits_mnt': '/u01',
        'net_security_integrity_target': 'server',
        'oidm_nbr_of_hash_prtn_cust': '4',
        'edition': 'enterprise',
        'archlog': 'yes',
        'hdg': 'no',
        'dbca_vars': '-characterSet AL32UTF8 -initParams filesystemio_options=setall,db_files=500',
        'dg_observer_zone': 'primary',
        'hpages': 'no',
        'net_security_encryption_type': 'required',
        'lvm': 'yes',
        'byol': 'no',
        'dborch_version': '5.0.23.17.02',
        'demo': 'no',
        'dbkey': '',
        'bkup_cfg_recovery_window': '30',
        'opcm': 'no',
        'timezone': 'UTC',
        'tmpl_tempsz': '1000MB',
        'oidm_nbr_of_hash_prtn_mtr_rdng': '4',
        'vol_index': 'no',
        'dbtype': 'si',
        'charset': 'AL32UTF8',
        'oidm_wk_strt_day': 'MONDAY',
        'oidm_nbr_of_hash_prtn_acct': '4',
        'dg_observer_user': 'oracle',
        'flashback_minutes': '1440',
        'build': 'no',
        'sid': 'ORCL',
        'psu_url': '',
        'clone': 'no',
        'managed_user': 'root',
        'bkup_nfs': 'no',
        'bundle': 'basic',
        'tmpl_dbrecoverydestsize': '',
        'oidm_user': 'oracle',
        'psm_oss_url': '',
        'ohome_name': '',
        'data': '100G',
        'reduced_volumes': 'no',
        'oidm_uri': 'https://storage.us2.oraclecloud.com/v1/dbcsswlibd-usoracle13098/OIDM/oidm_install.sh',
        'dg_connect_aliases': '',
        'dg_observer_exists': 'no',
        'oidm_nbr_of_hash_prtn_init_rdng': '4',
        'oidm_cl_strt_dt': '2013-01-01',
        'net_security_encryption_enable': 'yes',
        'sm': 'yes',
        'bkup_nfs_recovery_window': '30'
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
    image_metadata_bag='/oracle/machineimage_metadata/c256ea3f213c4ff18f3a831414d99f4b',
    imagelist=None,
    ip='10.19.11.70',
    label='gc3-naac-soar-d05-dbcs db_1 1',
    name='/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-soar-d05-dbcs/db_1/vm-1/57cced1d-c74f-41da-9c24-e86666eee4b2',
    networking={'eth0': {
        'model': '',
        'seclists': ['/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-soar-d05-dbcs/db_1/ora_db', '/Compute-587626604/eric.harris@oracle.com/gc3_naac_soar_seclist_01'],
        'dns': ['gc3-naac-soar-d05-dbcs.compute-587626604.oraclecloud.internal.'],
        'vethernet': '/oracle/public/default',
        'nat': 'ipreservation:/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-soar-d05-dbcs/db_1/vm-1/ipreservation'
    }},
    placement_requirements=['/system/compute/placement/default', '/oracle/compute/dedicated/fcbaed9f-242b-42ce-ac77-dd727f9710eb', '/system/compute/allow_instances'],
    platform='linux',
    priority='/oracle/public/default',
    quota='/Compute-587626604',
    quota_reservation=None,
    relationships=[],
    resolvers=None,
    reverse_dns=True,
    shape='oc4',
    site='',
    sshkeys=['/Compute-587626604/eric.harris@oracle.com/dbaas.gc3-naac-soar-d05-dbcs.DB.ora_user',
             '/Compute-587626604/eric.harris@oracle.com/dbaas.gc3-naac-soar-d05-dbcs.DB.ora_tools'],
    start_time=datetime.datetime(2018, 7, 11, 21, 29, 6, tzinfo=tzutc()),
    state='running',
    storage_attachments=[{
        'index': 1,
        'storage_volume_name': '/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-soar-d05-dbcs/db_1/vm-1/boot',
        'name': '/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-soar-d05-dbcs/db_1/vm-1/57cced1d-c74f-41da-9c24-e86666eee4b2/2bdf7705-4dc9-48ad-a703-9e5afb4edf86'
    }, {
        'index': 2,
        'storage_volume_name': '/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-soar-d05-dbcs/db_1/vm-1/redo',
        'name': '/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-soar-d05-dbcs/db_1/vm-1/57cced1d-c74f-41da-9c24-e86666eee4b2/2cf31d8b-2f86-4898-a62e-7c69ffb8a5ee'
    }, {
        'index': 3,
        'storage_volume_name': '/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-soar-d05-dbcs/db_1/vm-1/fra',
        'name': '/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-soar-d05-dbcs/db_1/vm-1/57cced1d-c74f-41da-9c24-e86666eee4b2/36a98b4a-1e85-449c-aac1-b3b423baff6b'
    }, {
        'index': 4,
        'storage_volume_name': '/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-soar-d05-dbcs/db_1/vm-1/bits',
        'name': '/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-soar-d05-dbcs/db_1/vm-1/57cced1d-c74f-41da-9c24-e86666eee4b2/31890970-9e74-4a2a-bc8c-20af59179e23'
    }, {
        'index': 5,
        'storage_volume_name': '/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-soar-d05-dbcs/db_1/vm-1/data',
        'name': '/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-soar-d05-dbcs/db_1/vm-1/57cced1d-c74f-41da-9c24-e86666eee4b2/1f819ae4-e28c-42ac-9818-8c8fc1c6092a'
    }],
    tags=['ORA.DCS', 'ORA.DB', 'ORA.DCS.PAAS.EE.HOURLY', '/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-soar-d05-dbcs/db_1/vm-1', '078783786aa35e455be7f3c4085f72f9'],
    uri='https://compute.uscom-central-1.oraclecloud.com/instance/Compute-587626604/eric.harris%40oracle.com/dbaas/gc3-naac-soar-d05-dbcs/db_1/vm-1/57cced1d-c74f-41da-9c24-e86666eee4b2',
    vcable_id='/Compute-587626604/eric.harris@oracle.com/c5a88c6b-e036-4510-8a73-1e76e9c8c582',
    virtio=None,
    vnc='10.19.11.69:5900')