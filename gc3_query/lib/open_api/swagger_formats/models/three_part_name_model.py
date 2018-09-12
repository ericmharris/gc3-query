# -*- coding: utf-8 -*-

"""
gc3-query.three_part_name_model    [9/12/2018 10:40 AM]
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
from . import *
_debug, _info, _warning, _error, _critical = get_logging(name=__name__)





class ThreePartNameModel(EmbeddedDocument):
    """
    """

    name = StringField()
    idm_service_instance_id = StringField()
    object_owner = StringField()
    object_name = StringField()
    idm_domain_name = StringField()

