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
from collections.abc import MutableMapping, MutableSequence

################################################################################
## Third-Party Imports
from dataclasses import dataclass
import keyring

################################################################################
## Project Imports

from gc3_query.lib import *
from gc3_query import GC3_QUERY_HOME
from gc3_query.lib.atoml.atoml_config import ATomlConfig
from gc3_query.lib.base_collections import OrderedDictAttrBase, ListBase
from gc3_query.lib.gc3logging import get_logging

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

# atoml_config_dir = GC3_QUERY_HOME.joinpath('etc/config')
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



class ConfigListBase(ListBase):

    def __init__(self, data=None):
        super().__init__()
        if isinstance(data, MutableSequence):
            for v in data:
                if isinstance(v, MutableSequence):
                    self.append(ConfigListBase(v))
                if isinstance(v, MutableMapping):
                    self.append(ConfigOrderedDictAttrBase(v))
                else:
                    self.append(v)


class ConfigOrderedDictAttrBase(OrderedDictAttrBase):

    def __init__(self, mapping):
        super().__init__()

        for k,v in mapping.items():
            if isinstance(v, MutableSequence):
                self[k] = ConfigListBase(v)
            if isinstance(v, MutableMapping):
                self[k] = ConfigOrderedDictAttrBase(v)
            else:
                self[k] = v


class GC3Config(ConfigOrderedDictAttrBase):

    def __init__(self, atoml_config_dir: Path = None):
        if not atoml_config_dir:
            atoml_config_dir = GC3_QUERY_HOME.joinpath('etc/config')
        _debug(f"atoml_config_dir={atoml_config_dir}")
        at_config = ATomlConfig(directory_paths=atoml_config_dir)
        gc3_cfg = at_config.toml
        super().__init__(mapping=gc3_cfg)



    def get_credential(self, idm_domain_name: str) -> IDMCredential:
        if idm_domain_name not in self['idm_domains']:
            raise RuntimeError(f"IDM Domain name provided, {idm_domain_name}, is not found in {self}")
        idm_domain_cfg = self['idm_domains'][idm_domain_name]
        service_name = f"gc3@{idm_domain_name}"
        username = self['user']['cloud_username']
        _info(f"service_name={service_name}, username={service_name}")
        _debug(f"password={password}")
        keystore_store = keyring.set_password(service_name=service_name,
                                              username=username,
                                              password=password)


        keystore_check = keyring.get_password(service_name=service_name, username=username)
        if keystore_check==password:
            return  IDMCredential(idm_domain_name=idm_domain_name,
                                  username=username,
                                  password=password,
                                  is_ucm=idm_domain_cfg['is_ucm'],
                                  is_classic=idm_domain_cfg['is_classic']
                                  )
        else:
            raise RuntimeError(f"Failed to set password for service_name={service_name}, username={service_name}")


    def set_credential(self, idm_domain_name: str, password: str) -> IDMCredential:
        """Stores password for idm_domain_name in system/OS keystore

        :param idm_domain_name:
        :param password:
        :return:
        """
        if idm_domain_name not in self['idm_domains']:
            raise RuntimeError(f"IDM Domain name provided, {idm_domain_name}, is not found in {self}")
        idm_domain_cfg = self['idm_domains'][idm_domain_name]
        service_name = f"gc3@{idm_domain_name}"
        username = self['user']['cloud_username']
        _info(f"service_name={service_name}, username={service_name}")
        _debug(f"password={password}")
        keystore_store = keyring.set_password(service_name=service_name,
                                                      username=username,
                                                      password=password)


        keystore_check = keyring.get_password(service_name=service_name, username=username)
        if keystore_check==password:
            return  IDMCredential(idm_domain_name=idm_domain_name,
                                  username=username,
                                  password=password,
                                  is_ucm=idm_domain_cfg['is_ucm'],
                                  is_classic=idm_domain_cfg['is_classic']
                    )
        else:
            raise RuntimeError(f"Failed to set password for service_name={service_name}, username={service_name}")



