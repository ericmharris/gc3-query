from pathlib import Path
import toml


from gc3_query import GC3_QUERY_HOME
from gc3_query.lib import *
_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


class TOMLConfig:
    def __init__(self, file_paths: Path = None, dir_path: Path = None) -> None:
        self.file_paths = file_paths
        self.dir_path = dir_path



    def load_file(self, path: Path) -> List[Any]:
        pass
