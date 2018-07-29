# -*- coding: utf-8 -*-

"""
gc3-query.toml_file    [6/1/2018 10:50 AM]
~~~~~~~~~~~~~~~~

Single file containing TOML or ATOML

"""

################################################################################
## Standard Library Imports
import sys, os

################################################################################
## Third-Party Imports
from dataclasses import dataclass
import toml
from toml.decoder import TomlDecodeError

################################################################################
## Project Imports
from gc3_query.lib import *

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)






from dataclasses import dataclass
import inspect
import types, typing

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


class ATomlFile:

    @classmethod
    def pre_process_line(cls, s: str) -> AnnotatedTOML:
        """Returns valid TOML string with any type_name annotations in the LHS separated out.

        :param s:
        """
        first_eq_loc = s.find('=')
        if first_eq_loc == -1:
            return AnnotatedTOML(input=s, key='None', type_name='None', value='None', toml=s)

        value = s[first_eq_loc + 1:]
        key = s[0:first_eq_loc - 1].strip()
        _debug(f"s={s}, first_eq_loc={first_eq_loc}, key={key}, value={value}")

        if "'" in key:
            key = key.replace("'", "")
        if ':' in key:
            parts = [p.strip() for p in key.split(":")]
            assert len(parts) == 2
            key, type_name = parts[0], parts[1]
            _debug(f"key={key}, type_name={type_name}")
        else:
            # key = s[0:first_eq_loc - 1].strip()
            # type_name = 'None'
            type_name = 'None'
            _debug(f"key={key}, type_name={type_name}")

        valid_toml = f"{key} = {value}"
        a_toml = AnnotatedTOML(input=s, key=key, type_name=type_name, value=value, toml=valid_toml)
        return a_toml

    def __init__(self, file_path: Path) -> None:
        """

        :type_name config_path: Path
        """
        self._name = self.__class__.__name__
        self.file_path = file_path.resolve()
        self.file_name = self.file_path.name
        self._lines = self.load_file(self.file_path)
        self.toml_text_lines = [l.toml for l in self._lines]
        self.toml_text = ''.join(self.toml_text_lines)
        try:
            self.toml = toml.loads(self.toml_text)
        except TomlDecodeError as e:
            _error(f"TomlDecodeError Exception caught")
            _error(f"class={self._name}")
            _error(f"file_path={self.file_path}")
            _error(e)
            raise

        _debug(f"{self._name} loaded with {len(self.toml_text_lines)} lines.")

    def load_file(self, path: Path) -> List[AnnotatedTOML]:

        if not path.exists():
            raise RuntimeError(f"{self._name} created with file that does not exist: {self.file_path}")
        if not path.is_file():
            raise RuntimeError(f"{self._name} created with something other than a file (eg. directory): {self.file_path}")
        with path.open() as fd:
            _lines = fd.readlines()
            pp_lines = [self.pre_process_line(l) for l in _lines]
            _info(f"loaded {len(pp_lines)} lines from {self.file_path}")

        return pp_lines

    def __str__(self):
        return f"<{self._name}: file_path={self.file_name}>"

    def __repr__(self):
        return self.__str__()


    def __eq__(self, other: 'ATomlFile') -> bool:
        return self.file_path == other.file_path
