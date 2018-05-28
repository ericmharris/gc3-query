from pathlib import Path

from toml import loads

from .util import quote_key

from gc3_query import GC3_QUERY_HOME

from gc3_query.lib.logging import get_logging

from gc3_query.lib import Path, Union, Dict
_debug, _info, _warning, _error, _critical = get_logging(name=__name__)



class TOMLFile:
    def __init__(self, path: Path):
        """

        :type config_path: Path
        """
        self._name = self.__class__.__name__
        self.path = path.resolve()
        if self.path.is_dir():
            self._init_file = self.path.joinpath('__init__.toml') if self.path.joinpath('__init__.toml').exists() else None
        else:
            self._init_file = self.path.parent.joinpath('__init__.toml') if self.path.parent.joinpath('__init__.toml').exists() else None


        if not self.path.exists():
            raise RuntimeError(f"{self._name} created with file or directory that does not exist: {self.path}")




