# -*- coding: utf-8 -*-

"""
gc3-query.toml_dataclass    [6/1/2018 4:23 PM]
~~~~~~~~~~~~~~~~

<DESCR SHORT>

<DESCR>
"""

################################################################################
## Standard Library Imports

################################################################################
## Third-Party Imports

################################################################################
## Project Imports
from gc3_query.lib import *

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)



class TOMLDataclass:


    def __init__(self, d: Dict) -> None:
        """Takes a dict as returned by the toml library and converts it to a dataclass representation.

        :param d: Dict

        """
        pass
