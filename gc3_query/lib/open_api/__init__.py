# -*- coding: utf-8 -*-

"""
#@Filename : __init__.py
#@Date : [8/9/2018 12:52 PM]
#@Poject: gc3-query
#@AUTHOR : emharris

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
from gc3_query.lib.gc3logging import get_logging

from gc3_query.lib import get_logging
_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

