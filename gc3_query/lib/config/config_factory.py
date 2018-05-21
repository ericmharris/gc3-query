# -*- coding: utf-8 -*-

from typing import List, Optional, Any, Callable, Dict, Tuple, Union, Set, Generator
from dataclasses import dataclass

from gc3_query.lib import *

from gc3_query.lib.logging import get_logging
_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


@dataclass
class ConfigFactory:
    """Loads configuration


## opc profile

{
  "global": {
    "format": "text",
    "debug-requests": false
  },
  "compute": {
    "user": "/Compute-IDENTITY_DOMAIN/USERNAME",
    "password-file": "~/.opc/password",
    "endpoint": "compute.uscom-central-1.oraclecloud.com"
  }
}



## psm setup info
{
"username":"eric.harris@oracle.com",
"password":"P@ll4dium!",
"identityDomain":"gc30003",
"region":"us",
"outputFormat":"short"
}

    """

    def __post_init__(self):
        self.username: str = "eric.harris@oracle.com"
        self.identity_domain: str = "gc30003"
        self.region: str = "us"
        self.rest_endpoint: str = "https://compute.uscom-central-1.oraclecloud.com/"
