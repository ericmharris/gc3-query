# -*- coding: utf-8 -*-

"""
gc3-query.bravado_config    [9/10/2018 1:13 PM]
~~~~~~~~~~~~~~~~

<DESCR SHORT>

<DESCR>
"""

################################################################################
## Standard Library Imports
import sys, os
from copy import deepcopy

################################################################################
## Third-Party Imports
from dataclasses import dataclass
from bravado_core.formatter import SwaggerFormat, NO_OP
from bravado_core.exception import SwaggerValidationError

################################################################################
## Project Imports
from gc3_query.lib import *
from gc3_query.lib import gc3_cfg
from gc3_query.lib.atoml.atoml_config import ATomlConfig
from gc3_query.lib.base_collections import NestedOrderedDictAttrListBase
from gc3_query.lib.gc3logging import get_logging
from gc3_query.lib.open_api import swagger_formats

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)




class BravadoConfig(NestedOrderedDictAttrListBase):

    def __init__(self, atoml_config_dir: Path = None):
        self._name = self.__class__.__name__
        self.atoml_config_dir = atoml_config_dir if atoml_config_dir else self.BASE_DIR.joinpath('etc/config')
        _debug(f"atoml_config_dir={self.atoml_config_dir}")
        self._at_config = ATomlConfig(directory_paths=self.atoml_config_dir)
        gc3_cfg = self._at_config.toml
        super().__init__(mapping=gc3_cfg)
        _debug(f"{self._name} created: {self}")


    @property
    def BASE_DIR(self) -> Path:
        base_dir = Path(__file__).parent.parent.parent
        return base_dir

    @property
    def CONFIG_DIR(self) -> Path:
        return self.atoml_config_dir

    @property
    def OPEN_API_CATALOG_DIR(self) -> Path:
        open_api_catalog_dir = self.BASE_DIR.joinpath(self.open_api.open_api_spec_catalog.api_catalog_dir)
        return open_api_catalog_dir

    @property
    def OPEN_API_SPEC_BASE(self) -> Path:
        open_api_spec_base = self.BASE_DIR.joinpath(self.open_api.open_api_spec_base)
        return open_api_spec_base

    @property
    def BRAVADO_CONFIG(self) -> DictStrAny:
        # bravado_config: DictStrAny = self.bravado.client_config.as_dict()
        # bravado_config.update(self.bravado.core_config.as_dict())
        # gc3_format_names = [f.format for f in self.open_api.formats.values()]
        # for gc3_format in gc3_formats:
        #     if gc3_format.format in gc3_format_names:
        #         bravado_config['formats'].append(gc3_format)

        return self.bravado_config


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
            # config['formats'] = gc3_formats
            config['formats'] = self._load_formats()
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


    def _load_formats(self) -> List[SwaggerFormat]:
        formats = []
        for obj_name in dir(swagger_formats):
            obj = getattr(swagger_formats, obj_name)
            if isinstance(obj, SwaggerFormat):
                formats.append(obj)
        return formats
