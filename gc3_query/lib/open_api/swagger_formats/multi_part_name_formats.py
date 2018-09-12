# -*- coding: utf-8 -*-

"""
gc3-query.multi_part_name_formats    [9/11/2018 4:24 PM]
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

################################################################################
## Project Imports
from gc3_query.lib import *

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

from bravado_core.formatter import SwaggerFormat, NO_OP
from bravado_core.exception import SwaggerValidationError

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
#                dst_list='seclist:/Compute-gc3pilot/eric.harris@oracle.com/psft_secwin_01', id='c16eb739-9b60-4c6a-91a3-97a197d98183',
#                name='/Compute-gc3pilot/eric.harris@oracle.com/psft_pcm_rdp', src_is_ip=True, src_list='seciplist:/oracle/public/public-internet',
#                uri='https://compute.uscom-central-1.oraclecloud.com/secrule/Compute-gc3pilot/eric.harris%40oracle.com/psft_pcm_rdp')


class MultiPartNameBaseFormat:

    def __init__(self, name: str):
        """
        Takes three-part name of object from Oracle Cloud Classic.

        /Compute-586297329/dhiru.vallabhbhai@oracle.com/paas/BDCSCE/gc3apacasbx500/bdcsce/vm-1/8aa0ae10-35f3-4b21-aac1-a4a6328edf1e
        /Compute-605519274/siva.subramani@oracle.com/dbaas/gc3ossitcmf103DBAAS/db_1/vm-1/04db581d-cb17-497e-8a6a-0e74cf4cbf5d
        /Compute-604700914/mayurnath.gokare@oracle.com/paas/OEHPCS/gc3mayurtst100/kafka/vm-1/0e86f68b-422c-4ed6-b62d-b2f1dd1cf28b
        /Compute-gc3pilot/eric.harris@oracle.com/psft-cldmgr-v501/8ee914dc-70c2-49b2-af2c-af1941af94f8

        """
        self.name = name.strip()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.__class__.__name__}({self})"

    def to_wire(self):
        return self.__str__()

    @classmethod
    def validate(cls, name: str) -> bool:
        if name.startswith('/Compute-'):
            return True
        raise SwaggerValidationError(f"Value={from_wire} not recognized as MultiPartNameFormat")


class ThreePartNameFormat(MultiPartNameBaseFormat):

    def __init__(self, name: str):
        """


        :param from_wire: <p>The three-part name of the object (<code>/Compute-<em>identity_domain</em>/<em>user</em>/<em>object</em></code>).<p>Object
          names can contain only alphanumeric characters, hyphens, underscores, and
          periods. Object names are case-sensitive.

        """
        super().__init__(name)
        self.idm_service_instance_id, self.object_owner, self.object_name =  self._parse_name(name=self.name)
        self.idm_domain_name = idm_instance_id_to_name.get(self.idm_service_instance_id, False)
        if not self.idm_domain_name:
            raise RuntimeError(f"Failed to parse IDM Domain name for {self.__class__.__name__}: {name}")
        _debug(f"{self.__class__.__name__} created ")

    def _parse_name(self, name: str) -> Tuple[str]:
        _, idm_name_part, object_owner, *object_name_parts = name.split('/')

        # idm_name_part = 'Compute-605519274'
        _, _idm_service_instance_id = idm_name_part.split('-')
        idm_service_instance_id = _idm_service_instance_id

        _object_name = '/'.join(object_name_parts)
        object_name = f"/{_object_name}"
        return idm_service_instance_id, object_owner, object_name


class TwoPartNameFormat(MultiPartNameBaseFormat):

    def __init__(self, name: str):
        """
        seciplist:/oracle/public/paas-infra


        :param from_wire: <p>The three-part name of the object (<code>/Compute-<em>identity_domain</em>/<em>user</em>/<em>object</em></code>).<p>Object
          names can contain only alphanumeric characters, hyphens, underscores, and
          periods. Object names are case-sensitive.

        """
        super().__init__(name)
        self.object_name, self.type = self._parse_name(name=self.name)
        _debug(f"{self.__class__.__name__} created ")

    def _parse_name(self, name: str) -> Tuple[str]:
        type, object_name = name.split(':')
        return object_name, type


def from_wire(name: str) -> Union[ThreePartNameFormat, TwoPartNameFormat]:
    return ThreePartNameFormat(name=name)


multi_part_name = SwaggerFormat(
    # name of the format as used in the Swagger spec
    format='multi-part-name',

    # Callable to convert a python object to_wire representations
    # to_wire=lambda json_bool_instance: json_bool_instance.as_wire,
    to_wire=lambda format_instance: format_instance.to_wire,

    # Callable to convert a from_wire to a python object
    to_python=from_wire,

    # Callable to validate the cidr in string form
    validate=MultiPartNameBaseFormat.validate,
    description='Converts seciplist:/oracle/public/paas-infra or seclist:/Compute-605519274/siva.subramani@oracle.com/paas/JaaS/gc3ossitcmf103JAAS/wls/ora_ms into objects'
)
