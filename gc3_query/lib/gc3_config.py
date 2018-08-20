# -*- coding: utf-8 -*-

"""
#@Filename : gc3_config
#@Date : [7/29/2018 12:13 PM]
#@Poject: gc3-query
#@AUTHOR : emharris

~~~~~~~~~~~~~~~~

<DESCR SHORT>

<DESCR>
"""

################################################################################
## Standard Library Imports

from copy import deepcopy

import keyring
################################################################################
## Third-Party Imports
from dataclasses import dataclass

from gc3_query.lib import *
from gc3_query.lib.atoml.atoml_config import ATomlConfig
from gc3_query.lib.base_collections import NestedOrderedDictAttrListBase
from gc3_query.lib.gc3logging import get_logging
from gc3_query.lib.open_api.swagger_formats import formats

################################################################################
## Project Imports
from gc3_query.lib import get_logging
_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


# atoml_config_dir = BASE_DIR.joinpath('etc/config')
# _debug(f"atoml_config_dir={atoml_config_dir}")
# at_config = ATomlConfig(directory_paths=atoml_config_dir)
# gc3_cfg = at_config.toml


@dataclass
class IDMCredential:
    idm_domain_name: str
    username: str
    password: str
    is_ucm: bool
    is_classic: bool


class GC3Config(NestedOrderedDictAttrListBase):

    def __init__(self, atoml_config_dir: Path = None):
        self._name = self.__class__.__name__
        self.atoml_config_dir = atoml_config_dir if atoml_config_dir else self.BASE_DIR.joinpath('etc/config')
        _debug(f"atoml_config_dir={self.atoml_config_dir}")
        self._at_config = ATomlConfig(directory_paths=self.atoml_config_dir)
        gc3_cfg = self._at_config.toml
        super().__init__(mapping=gc3_cfg)
        _debug(f"{self._name} created: {self}")

    # def __getattr__(self, key):
    #     value = self._d[key]
    #     return value
    #
    #
    # def __getitem__(self, key):
    #     value = self._d[key]
    #     return value

    @property
    def BASE_DIR(self) -> Path:
        base_dir = Path(__file__).parent.parent
        return base_dir

    @property
    def CONFIG_DIR(self) -> Path:
        return self.atoml_config_dir

    def get_credential(self, idm_domain_name: str) -> IDMCredential:
        if idm_domain_name not in self['idm']['domains']:
            raise RuntimeError(f"IDM Domain name provided, {idm_domain_name}, is not found in {self}")

        idm_domain_cfg = self['idm']['domains'][idm_domain_name]
        service_name = f"gc3@{idm_domain_name}"
        username = self['user']['cloud_username']
        _info(f"service_name={service_name}, username={service_name}")
        password = keyring.get_password(service_name=service_name, username=username)
        if password:
            return IDMCredential(idm_domain_name=idm_domain_name,
                                 username=username,
                                 password=password,
                                 is_ucm=idm_domain_cfg['is_ucm'],
                                 is_classic=idm_domain_cfg['is_classic']
                                 )
        else:
            raise RuntimeError(f"Failed to get password for service_name={service_name}, username={service_name}")

    def set_credential(self, idm_domain_name: str, password: str) -> IDMCredential:
        """Stores password for idm_domain_name in system/OS keystore

        :param idm_domain_name:
        :param password:
        :return:
        """
        if idm_domain_name not in self['idm']['domains']:
            raise RuntimeError(f"IDM Domain name provided, {idm_domain_name}, is not found in {self}")
        idm_domain_cfg = self['idm']['domains'][idm_domain_name]
        service_name = f"gc3@{idm_domain_name}"
        username = self['user']['cloud_username']
        _info(f"service_name={service_name}, username={service_name}")
        _debug(f"password={password}")
        keystore_store = keyring.set_password(service_name=service_name,
                                              username=username,
                                              password=password)

        check_credential = self.get_credential(idm_domain_name=idm_domain_name)
        if check_credential.password == password and check_credential.idm_domain_name == idm_domain_name and check_credential.username == username:
            return check_credential
        else:
            raise RuntimeError(f"Failed to set password for service_name={service_name}, username={service_name}")

    def get_bravado_config(self, config_type: str = 'bravado') -> DictStrAny:
        """
        bravado.client.SwaggerClient#from_spec
        # Apply bravado config defaults
        config = config or {}
        bravado_config = BravadoConfig.from_config_dict(config)
        # remove bravado configs from config dict
        for key in set(bravado_config._fields).intersection(set(config)):
            del config[key]
        # set bravado config object
        config['bravado'] = bravado_config

        :param config_type:
        :return:
        """
        config_types = {'bravado': self.bravado.core_config.as_dict_melded_with(self.bravado.client_config),  # All config
                        'bravado_client': self.bravado.client_config.as_dict(),                                  # Only config for client
                        'bravado_core': self.bravado.core_config.as_dict()                                       # core
                        }
        if config_type not in config_types:
            _error(f"config_type={config_type} not found in {config_types.keys()}")
            raise RuntimeError(f"config_type={config_type} not found in {config_types.keys()}")
        config: dict = config_types[config_type]
        if config_type in ['bravado', 'bravado_core']:
            config['formats'] = formats
        return deepcopy(config)


    @property
    def bravado_config(self):
        return self.get_bravado_config(config_type='bravado')

    @property
    def bravado_core_config(self):
        return self.get_bravado_config(config_type='bravado_core')

    @property
    def bravado_client_config(self):
        return self.get_bravado_config(config_type='bravado_client')


