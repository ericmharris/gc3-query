# -*- coding: utf-8 -*-

"""
gc3-query.open_api_config    [8/23/2018 12:08 PM]
~~~~~~~~~~~~~~~~

<DESCR SHORT>

<DESCR>
"""

################################################################################
## Standard Library Imports
import sys, os

################################################################################
## Third-Party Imports
from dataclasses import dataclass, field

################################################################################
## Project Imports
from gc3_query.lib import *
from gc3_query.lib import gc3_cfg
from .swagger_formats import gc3_formats

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


@dataclass
class OpenApiCoreConfig:
    default_type_to_object: bool
    include_missing_properties: bool
    internally_dereference_refs: bool
    use_models: bool
    validate_requests: bool
    validate_responses: bool
    validate_swagger_spec: bool
    formats: List = field(init=False)

    def __post_init__(self):
        for gc3_format in gc3_formats:
            if gc3_format.format in gc3_cfg.open_api.formats:
                self.formats.append(gc3_format)
