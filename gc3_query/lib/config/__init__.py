# -*- coding: utf-8 -*-
from gc3_query.lib import *
from gc3_query.lib.logging import Logging, get_logging

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

secrets_file = BASE_DIR.joinpath('etc/config/secrets.py')

if secrets_file.exists():
    from gc3_query.etc.config.secrets import opc_password
else:
    raise RuntimeError(f'File Not Found: {secrets_file}\n')
