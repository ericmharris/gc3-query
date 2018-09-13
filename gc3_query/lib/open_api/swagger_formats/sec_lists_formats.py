# -*- coding: utf-8 -*-

"""
gc3-query.sec_list    [9/9/2018 11:47 AM]
~~~~~~~~~~~~~~~~

<DESCR SHORT>

<DESCR>
"""

# ################################################################################
# ## Standard Library Imports
# import sys, os
# from typing import List, Optional, Any, Callable, Dict, Tuple, Union, Set, Generator, Iterable
#
# ################################################################################
# ## Third-Party Imports
# from dataclasses import dataclass
# from bravado_core.formatter import SwaggerFormat, NO_OP
# from bravado_core.exception import SwaggerValidationError
#
# ################################################################################
# ## Project Imports
# # from gc3_query.lib import *
# from gc3_query.lib import gc3_cfg
# # from gc3_query.lib.gc3_config import GC3Config
# from gc3_query.lib.gc3logging import get_logging
# _debug, _info, _warning, _error, _critical = get_logging(name=__name__)


# gc3_cfg = GC3Config()

from bravado_core.formatter import SwaggerFormat, NO_OP
from bravado_core.exception import SwaggerValidationError
from collections.abc import MutableMapping
################################################################################
## Project Imports
from gc3_query.lib import *
from gc3_query.lib import gc3_cfg
# from gc3_query.lib.gc3_config import GC3Config
from gc3_query.lib.gc3logging import get_logging

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

# gc3_cfg = GC3Config()


idm_instance_id_to_name = {idm_domain.formal_id: idm_domain.name for idm_domain in [d for d in gc3_cfg.idm.domains.values() if not isinstance(d, str)]}

# SecRule = dict(action='PERMIT', application='/oracle/public/rdp', description='', disabled=False, dst_is_ip=False,
#                dst_list='seclist:/Compute-gc3pilot/eric.harris@oracle.com/psft_seclist_win_01', id='c16eb739-9b60-4c6a-91a3-97a197d98183',
#                name='/Compute-gc3pilot/eric.harris@oracle.com/psft_pcm_rdp', src_is_ip=True, src_list='seciplist:/oracle/public/public-internet',
#                uri='https://compute.uscom-central-1.oraclecloud.com/secrule/Compute-gc3pilot/eric.harris%40oracle.com/psft_pcm_rdp')


class SecListBaseFormat(MutableMapping):

    def __init__(self, name: str):
        """Takes three-part name of object from Oracle Cloud Classic.

        seclist:/Compute-586297329/siva.subramani@oracle.com/paas/JaaS/gc3emacmma804/lb/ora_otd_infraadmin
        seclist:/Compute-586297329/siva.subramani@oracle.com/paas/JaaS/gc3emacmma804/wls/ora_wls_infraadmin
        seclist:/Compute-586297329/mayurnath.gokare@oracle.com/paas/JaaS/gc3apacasbx546/lb/ora_otd
        seclist:/Compute-586297329/dhiru.vallabhbhai@oracle.com/dbaas/gc3emeacetr001/db_1/ora_db
        seclist:/Compute-586297329/ramesh.dadhania@oracle.com/paas/ANALYTICS/gc3emeatfde102/BI/ora_BISecList
        seclist:/Compute-586297329/seetharaman.nandyal@oracle.com/paas/JaaS/gc3apacasbx529/wls/ora_ms
        seclist:/Compute-586297329/seetharaman.nandyal@oracle.com/paas/JaaS/gc3apacasbx529/lb/ora_otd
        seclist:/Compute-586297329/sharad.salian@oracle.com/dbaas/gc3emeaczsi201/db_1/ora_db
        seclist:/Compute-586297329/sharad.salian@oracle.com/paas/SOA/gc3emeaoics106/lb/ora_otd_infraadmin

        seclist:/Compute-gc3pilot/eric.harris@oracle.com/psft_seclist_win_01



        :param name:  The three-part name of the object (/Compute-identity_domain/user/object).
        """
        # self.idm_service_instance_id, self.username, self.list_object_name, self.list_type = self._parse_name(name=self.name)
        # self.idm_domain_name = idm_instance_id_to_name.get(self.idm_service_instance_id, False)
        # if not self.idm_domain_name:
        #     raise RuntimeError(f"Failed to parse IDM Domain name for {self.__class__.__name__}: {name}")
        # _debug(f"{self.__class__.__name__} created ")
        self._d = dict()
        self['name'] = name.strip()
        _debug(f"{self.__class__.__name__} created ")

    # def __str__(self):
    #     return self.name
    #
    # def __repr__(self):
    #     return f"{self.__class__.__name__}({self})"

    def to_wire(self):
        return self.__str__()

    @classmethod
    def validate(cls, sec_list_name: str) -> bool:
        if 'seclist' in sec_list_name:
            return True
        if 'seciplist' in sec_list_name:
            return True
        raise SwaggerValidationError(f"Value={from_wire} not recognized as SecListFormat")

    def __str__(self):
        return self['name']

    def __repr__(self):
        return f"{self.__class__.__name__}({self})"


    def __setitem__(self, key, value):
        self._d[key] = value

    def __getitem__(self, key):
        return self._d[key]

    # access members with a '.'
    def __getattr__(self, key):
        """
        Called when an attribute can't be found in an object's instance __dict__.
        :param key:
        :return:
        """
        return self._d[key]

    def __delitem__(self, key):
        del self._d[key]

    def __iter__(self):
        return iter(self._d)

    def __len__(self):
        return len(self._d)

    def keys(self):
        return list(super().keys())

    def values(self):
        return list(super().values())

    def items(self):
        return list(super().items())

    def __eq__(self, other):
        return self['name'] == other['name']



class SecListFormat(SecListBaseFormat):

    def __init__(self, name: str):
        """
        seciplist:/oracle/public/paas-infra


        :param from_wire: <p>The three-part name of the object (<code>/Compute-<em>identity_domain</em>/<em>user</em>/<em>object</em></code>).<p>Object
          names can contain only alphanumeric characters, hyphens, underscores, and
          periods. Object names are case-sensitive.

        """
        super().__init__(name)
        self.idm_service_instance_id, self.object_owner, self.object_name, self.object_type = self._parse_name(name=self.name)
        self.idm_domain_name = idm_instance_id_to_name.get(self.idm_service_instance_id, False)
        self.object_type = "SecList"
        if not self.idm_domain_name:
            raise RuntimeError(f"Failed to parse IDM Domain name for {self.__class__.__name__}: {name}")
        _debug(f"{self.__class__.__name__} created ")

    def _parse_name(self, name: str) -> Tuple[str]:
        list_type, _name = name.split(':')
        _, idm_name_part, username, *object_name_parts = _name.split('/')

        # idm_name_part = 'Compute-605519274'
        _, _idm_service_instance_id = idm_name_part.split('-')
        idm_service_instance_id = _idm_service_instance_id

        _list_object_name = '/'.join(object_name_parts)
        list_object_name = f"/{_list_object_name}"
        return idm_service_instance_id, username, list_object_name, list_type


class SecIPListFormat(SecListBaseFormat):

    def __init__(self, name: str):
        """
        seciplist:/oracle/public/paas-infra


        :param from_wire: <p>The three-part name of the object (<code>/Compute-<em>identity_domain</em>/<em>user</em>/<em>object</em></code>).<p>Object
          names can contain only alphanumeric characters, hyphens, underscores, and
          periods. Object names are case-sensitive.

        """
        super().__init__(name)
        self.object_name, self.object_type = self._parse_name(name=self.name)
        self.object_type = "SecIPList"
        _debug(f"{self.__class__.__name__} created ")

    def _parse_name(self, name: str) -> Tuple[str]:
        object_type, object_name = name.split(':')
        return object_name, object_type


def from_wire(name: str) -> Union[SecListFormat, SecIPListFormat]:
    if 'seclist' in name:
        return SecListFormat(name=name)
    if 'seciplist' in name:
        return SecIPListFormat(name=name)
    raise SwaggerValidationError(f'Failed to find SecList/SecIPList format in: {name}')


sec_list_format = SwaggerFormat(
    # name of the format as used in the Swagger spec
    format='sec-list',

    # Callable to convert a python object to_wire representations
    # to_wire=lambda json_bool_instance: json_bool_instance.as_wire,
    to_wire=lambda sec_list_format_instance: sec_list_format_instance.to_wire,

    # Callable to convert a from_wire to a python object
    to_python=from_wire,

    # Callable to validate the cidr in string form
    validate=SecListBaseFormat.validate,
    description='Converts seciplist:/oracle/public/paas-infra or seclist:/Compute-605519274/siva.subramani@oracle.com/paas/JaaS/gc3ossitcmf103JAAS/wls/ora_ms into objects'
)
