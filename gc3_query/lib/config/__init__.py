# -*- coding: utf-8 -*-
from gc3_query.lib import *
from gc3_query.lib.logging import Logging, get_logging

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

base_secrets_file = BASE_DIR.joinpath('etc/config/secrets.py')
user_secrets_file = Path.home().joinpath('.gc3/config/secrets.py')
secrets_file = user_secrets_file if user_secrets_file.exists() else base_secrets_file


if secrets_file.exists():
    pass
else:
    raise RuntimeError(f'File Not Found: {secrets_file}\n')
