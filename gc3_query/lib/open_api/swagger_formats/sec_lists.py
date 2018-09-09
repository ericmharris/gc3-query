# -*- coding: utf-8 -*-

"""
gc3-query.sec_list    [9/9/2018 11:47 AM]
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
from bravado_core.formatter import SwaggerFormat, NO_OP
from bravado_core.exception import SwaggerValidationError

################################################################################
## Project Imports
from gc3_query.lib import *

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)




class SecListBaseFormat:


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

        :param name:  The three-part name of the object (/Compute-identity_domain/user/object).
        """
        self._name = name
        self.identitiy_domain, user, object_name = self._parse_name(name=name)


    def _parse_name(self, name: str)->Tuple[str]:
        _, _name = name.split(':')
        idm_part, user, *obejct_names = _name.split('/')
        obejct_name = '/'.join(obejct_names)
        return idm_part, user, obejct_name

    @classmethod
    def validate(cls, from_wire: str) -> bool:
        _debug(f"from_wire={from_wire}")
        try:
            as_boolean = cls.str_to_bool[from_wire.lower()]
        except KeyError:
            raise SwaggerValidationError(f"Value={from_wire} not recognized as SecListFormat")
        return isinstance(as_boolean, bool)



class SecListFormat(SecListBaseFormat):

    def __init__(self, name: str):
        """
        seciplist:/oracle/public/paas-infra


        :param from_wire: <p>The three-part name of the object (<code>/Compute-<em>identity_domain</em>/<em>user</em>/<em>object</em></code>).<p>Object
          names can contain only alphanumeric characters, hyphens, underscores, and
          periods. Object names are case-sensitive.

        """
        super().__init__(name)





class SecIPListFormat(SecListBaseFormat):

    def __init__(self, name: str):
        """
        seciplist:/oracle/public/paas-infra


        :param from_wire: <p>The three-part name of the object (<code>/Compute-<em>identity_domain</em>/<em>user</em>/<em>object</em></code>).<p>Object
          names can contain only alphanumeric characters, hyphens, underscores, and
          periods. Object names are case-sensitive.

        """
        super().__init__(name)




def from_wire(name: str) -> Union[SecListFormat, SecIPListFormat]:
    if name.startswith('seclist'):
        return SecListFormat(name=name)
    if name.startswith('seciplist'):
        return SecIPListFormat(name=name)
    raise SwaggerValidationError(f'Failed to find SecList/SecIPList format in: {name}')

sec_list_format = SwaggerFormat(
    # name of the format as used in the Swagger spec
    format='sec-list',

    # Callable to convert a python object to_wire representations
    # to_wire=lambda json_bool_instance: json_bool_instance.as_wire,
    to_wire=from_wire,

    # Callable to convert a from_wire to a python object
    to_python=lambda s: SecListBaseFormat(s),

    # Callable to validate the cidr in string form
    validate=SecListBaseFormat.validate,
    description='Converts "true" and "false" to/from equivalent booleans.'
)