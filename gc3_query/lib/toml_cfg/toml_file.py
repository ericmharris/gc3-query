from pathlib import Path
import toml

from gc3_query import GC3_QUERY_HOME

from gc3_query.lib.logging import get_logging

from gc3_query.lib import Path, Union, Dict
_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


class TOMLFile:
    def __init__(self, config_path: Path):
        self.config_path = config_path
