{'domain': 'compute-587626604.oraclecloud.internal.',
 'placement_requirements': ['/system/compute/placement/default',
  '/oracle/compute/dedicated/fcbaed9f-242b-42ce-ac77-dd727f9710eb',
  '/system/compute/allow_instances'],
 'ip': '10.19.9.86',
 'fingerprint': '59:9b:36:df:e8:b4:02:e6:5c:5b:9f:7b:d4:33:65:ad',
 'image_metadata_bag': '/oracle/machineimage_metadata/0fa1013075c2462aa148af5958353099',
 'site': '',
 'shape': 'oc4',
 'imagelist': None,
 'image_format': 'raw',
 'relationships': [],
 'availability_domain': '/uscom-central-1a',
 'networking': {'eth0': {'model': '',
   'seclists': ['/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-cdmt-d05-jcsdb/db_1/ora_db',
    '/Compute-587626604/eric.harris@oracle.com/GC3NAACCDMT_PSFT'],
   'dns': ['gc3-naac-cdmt-d05-jcsdb.compute-587626604.oraclecloud.internal.'],
   'vethernet': '/oracle/public/default',
   'nat': 'ipreservation:/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-cdmt-d05-jcsdb/db_1/vm-1/ipreservation'}},
 'storage_attachments': [{'index': 1,
   'storage_volume_name': '/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-cdmt-d05-jcsdb/db_1/vm-1/boot',
   'name': '/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-cdmt-d05-jcsdb/db_1/vm-1/963e740b-052b-469c-849c-37a1d0752b7a/e4a13249-83f0-4a22-958f-32f1fc7ba50f'},
  {'index': 2,
   'storage_volume_name': '/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-cdmt-d05-jcsdb/db_1/vm-1/redo',
   'name': '/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-cdmt-d05-jcsdb/db_1/vm-1/963e740b-052b-469c-849c-37a1d0752b7a/5e827e28-7b4d-4302-992b-6782f328c013'},
  {'index': 3,
   'storage_volume_name': '/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-cdmt-d05-jcsdb/db_1/vm-1/fra',
   'name': '/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-cdmt-d05-jcsdb/db_1/vm-1/963e740b-052b-469c-849c-37a1d0752b7a/000ae80c-e3a7-43a1-ad51-2e80e8ec5157'},
  {'index': 4,
   'storage_volume_name': '/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-cdmt-d05-jcsdb/db_1/vm-1/bits',
   'name': '/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-cdmt-d05-jcsdb/db_1/vm-1/963e740b-052b-469c-849c-37a1d0752b7a/61a80d6e-1dd2-4fb1-a6d5-3a4abf144118'},
  {'index': 5,
   'storage_volume_name': '/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-cdmt-d05-jcsdb/db_1/vm-1/data',
   'name': '/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-cdmt-d05-jcsdb/db_1/vm-1/963e740b-052b-469c-849c-37a1d0752b7a/9476420b-bf43-4369-8fdc-4168fbfcd2be'}],
 'hostname': 'gc3-naac-cdmt-d05-jcsdb.compute-587626604.oraclecloud.internal.',
 'quota_reservation': None,
 'disk_attach': '',
 'label': 'gc3-naac-cdmt-d05-jcsdb db_1 1',
 'priority': '/oracle/public/default',
 'platform': 'linux',
 'state': 'running',
 'virtio': None,
 'vnc': '10.19.9.85:5900',
 'desired_state': 'running',
 'tags': ['ORA.DCS',
  'ORA.DB',
  'ORA.DCS.PAAS.EE.HOURLY',
  '/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-cdmt-d05-jcsdb/db_1/vm-1',
  'a336968b7c79808c9d558e39dd73755f'],
 'start_time': '2018-04-27T21:35:05Z',
 'quota': '/Compute-587626604',
 'entry': None,
 'error_reason': '',
 'sshkeys': ['/Compute-587626604/eric.harris@oracle.com/dbaas.gc3-naac-cdmt-d05-jcsdb.DB.ora_user',
  '/Compute-587626604/eric.harris@oracle.com/dbaas.gc3-naac-cdmt-d05-jcsdb.DB.ora_tools'],
 'resolvers': None,
 'account': '/Compute-587626604/default',
 'name': '/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-cdmt-d05-jcsdb/db_1/vm-1/963e740b-052b-469c-849c-37a1d0752b7a',
 'vcable_id': '/Compute-587626604/eric.harris@oracle.com/346a9e40-bf9a-4d27-a596-a63f5b167624',
 'hypervisor': {'mode': 'hvm'},
 'uri': 'https://compute.uscom-central-1.oraclecloud.com/instance/Compute-587626604/eric.harris%40oracle.com/dbaas/gc3-naac-cdmt-d05-jcsdb/db_1/vm-1/963e740b-052b-469c-849c-37a1d0752b7a',
 'reverse_dns': True,
 'attributes': {'nodelist': '',
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
  'sshkeys': ['ssh-dss AAAAB3NzaC1kc3MAAACBAP1/U4EddRIpUt9KnC7s5Of2EbdSPO9EAMMeP4C2USZpRV1AIlH7WT2NWPq/xfW6MPbLm1Vs14E7gB00b/JmYLdrmVClpJ+f6AR7ECLCT7up1/63xhv4O1fnxqimFQ8E+4P208UewwI1VBNaFpEy9nXzrith1yrv8iIDGZ3RSAHHAAAAFQCXYFCPFSMLzLKSuYKi64QL8Fgc9QAAAIEA9+GghdabPd7LvKtcNrhXuXmUr7v6OuqC+VdMCz0HgmdRWVeOutRZT+ZxBxCBgLRJFnEj6EwoFhO3zwkyjMim4TwWeotUfI0o4KOuHiuzpnWRbqN/C/ohNWLx+2J6ASQ7zKTxvqhRkImog9/hWuWfBpKLZl6Ae1UlZAFMO/7PSSoAAACAV0PgmmFiLGK4riYtxxWsAfln+o1AQCI8mlxIQVS0YWSM6wCBIx2byRdNt8n8CtVfktosXpValjTfIDo7X7TUIQ1te5vkFMT75SmBkJCF1BTEWQH88gr3KkBj5i411o/qsOcAZdNpLzeYLxKG4IC3Iz8OJh7i9JCj9GFVupeY/cQ=',
   'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDkl16+TS1DB5jFwxr8tRMfztjLCHK2+wpfqy2eKeUzDJx8oGlasmBTAdwPX9cH3bfPRLJzru6SG2fJWsow4sU0d2clcwLRtqVdFMAdA3MSpIqayQMQJJ7NE5omkucF0pf0RG2p5cT3mBZDw/9IrSKnIAzaescUi72QOtcVSVgOiBcvJeQVn75GFQ0+JVKnVooh4pL2xDwTUj4EeSn5aLSA4ycqpBqvFFzrGsfDjDn55HiL0Dwwo9uM6VasAPHatqVIRA4EXGMu+QU6iw0m75e5n5CzEoL5ut4D2Og6MqrAVHTmtwf3WhPlDIzLu5OZbILydPq3/u58g6IVUHeB/wBd'],
  'dbdns': 'gc3-naac-cdmt-d05-jcsdb',
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
  'network': {'nimbula_vcable-eth0': {'vethernet_id': '0',
    'vethernet': '/oracle/public/default',
    'address': ['c6:b0:20:6c:5e:8a', '10.19.9.86'],
    'model': '',
    'vethernet_type': 'vlan',
    'id': '/Compute-587626604/eric.harris@oracle.com/346a9e40-bf9a-4d27-a596-a63f5b167624',
    'dhcp_options': []}},
  'tmpl_systemsz': '2000MB',
  'dg_ssh_pub': '\n',
  'version': '12102',
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
  'nimbula_orchestration': '/Compute-587626604/eric.harris@oracle.com/dbaas/gc3-naac-cdmt-d05-jcsdb/db_1/vm-1',
  'asm': 'false',
  'dg_uniq_names': '',
  'ords_config': 'yes',
  'tde_action': 'config',
  'bkup_cfg_files': 'yes',
  'oidm_nbr_of_hash_prtn_agrmnt': '4',
  'redo_mnt': '/u04',
  'dg_network': 'nat',
  'bp_update': 'no',
  'vols': '(bits:60gb data:25gb fra:42gb redo:26gb)',
  'oidm_nbr_of_hash_prtn_fnl_rdng': '4',
  'redo': '26G',
  'setupdb': 'yes',
  'bkup_daily_time': '',
  'fra': '42G',
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
  'dns': {'domain': 'compute-587626604.oraclecloud.internal.',
   'hostname': 'gc3-naac-cdmt-d05-jcsdb.compute-587626604.oraclecloud.internal.',
   'nimbula_vcable-eth0': 'gc3-naac-cdmt-d05-jcsdb.compute-587626604.oraclecloud.internal.'},
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
  'data': '25G',
  'reduced_volumes': 'no',
  'oidm_uri': 'https://storage.us2.oraclecloud.com/v1/dbcsswlibd-usoracle13098/OIDM/oidm_install.sh',
  'dg_connect_aliases': '',
  'dg_observer_exists': 'no',
  'oidm_nbr_of_hash_prtn_init_rdng': '4',
  'oidm_cl_strt_dt': '2013-01-01',
  'net_security_encryption_enable': 'yes',
  'sm': 'yes',
  'bkup_nfs_recovery_window': '30'},
 'boot_order': [1]}

​