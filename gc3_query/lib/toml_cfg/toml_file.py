# -*- coding: utf-8 -*-

"""
LIB_NAME.FILE_NAME
~~~~~~~~~~~~~~~~

<DESCR SHORT>

<DESCR>
"""
from dataclasses import dataclass

from gc3_query.lib import *
from pathlib import Path

import toml

from gc3_query import GC3_QUERY_HOME

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


@dataclass()
class AnnotatedTOML:
    input: str
    key: str
    type_name: str
    value: str
    toml: str

    def __post_init__(self):
        self._name = self.__class__.__name__
        _debug(f"{self._name} __post_init(): {self}")

    def __str__(self):
        return self.toml


class TOMLFile:

    @classmethod
    def pre_process_line(cls, s: str) -> AnnotatedTOML:
        """Returns TOML string with any type_name annotations in the LHS separated out.

        :param s:
        """
        first_eq_loc = s.find('=')
        value = s[first_eq_loc + 1:]
        _debug(f"s={s}, first_eq_loc={first_eq_loc}, value={value}")
        if first_eq_loc == -1:
            return AnnotatedTOML(input=s, key='None', type_name='None', value='None', toml=s)

        if ':' in s[0:first_eq_loc]:
            parts = [p.strip() for p in s[0:first_eq_loc].split(":")]
            assert len(parts) == 2
            key, type_name = parts[0], parts[1]
            _debug(f"key={key}, type_name={type_name}")
        else:
            key = s[0:first_eq_loc - 1].strip()
            type_name = 'None'
            _debug(f"key={key}, type_name={type_name}")

        valid_toml = f"{key} = {value}"
        a_toml = AnnotatedTOML(input=s, key=key, type_name=type_name, value=value, toml=valid_toml)
        return a_toml

    def __init__(self, path: Path):
        """

        :type_name config_path: Path
        """
        self._name = self.__class__.__name__
        self.path = path.resolve()
        self._lines = self.load_file(self.path)
        self.toml_text_lines = [l.toml for l in self._lines]
        self.toml_text = '\n'.join(self.toml_text_lines)
        self.toml = toml.loads(self.toml_text)

    def load_file(self, path: Path) -> List[AnnotatedTOML]:

        if not path.exists():
            raise RuntimeError(f"{self._name} created with file that does not exist: {self.path}")
        if not path.is_file():
            raise RuntimeError(f"{self._name} created with something other than a file (eg. directory): {self.path}")
        with path.open() as fd:
            _lines = fd.readlines()
            pp_lines = [self.pre_process_line(l) for l in _lines]
            _info(f"loaded {len(pp_lines)} lines from {self.path}")

        return pp_lines
