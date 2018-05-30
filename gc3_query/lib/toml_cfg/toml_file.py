from pathlib import Path

from toml import loads

from .util import quote_key

from gc3_query import GC3_QUERY_HOME

from gc3_query.lib.logging import get_logging

from gc3_query.lib import Path, Union, Dict
_debug, _info, _warning, _error, _critical = get_logging(name=__name__)



class TOMLFile:

    @classmethod
    def quote_key(cls, s):
        return quote_key(s)

    def __init__(self, path: Path):
        """

        :type config_path: Path
        """
        self._name = self.__class__.__name__
        self.path = path.resolve()
        self.text = self.load(self.path)



    def load(self, path: Path) -> str:

        if not path.exists():
            raise RuntimeError(f"{self._name} created with file that does not exist: {self.path}")
        if not path.is_file():
            raise RuntimeError(f"{self._name} created with something other than a file (eg. directory): {self.path}")
        with path.open().readlines() as _lines:
           lines_w_qkeys = [self.quote_key(l) for l in _lines]
           _debug(f"lines_w_qkeys={lines_w_qkeys}")




