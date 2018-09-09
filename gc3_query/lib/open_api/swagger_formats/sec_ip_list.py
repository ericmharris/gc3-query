# -*- coding: utf-8 -*-

"""
gc3-query.sec_ip_list    [9/9/2018 12:57 PM]
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

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)




class SecIPListFormat:

    def __init__(self, from_wire: str):
        """
        seciplist:/oracle/public/paas-infra


        :param from_wire: <p>The three-part name of the object (<code>/Compute-<em>identity_domain</em>/<em>user</em>/<em>object</em></code>).<p>Object
          names can contain only alphanumeric characters, hyphens, underscores, and
          periods. Object names are case-sensitive.

        """
        self.from_wire = from_wire
