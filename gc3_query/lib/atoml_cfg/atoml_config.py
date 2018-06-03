# -*- coding: utf-8 -*-

"""
gc3-query.atoml_config    [6/3/2018 8:42 AM]
~~~~~~~~~~~~~~~~

<DESCR SHORT>

<DESCR>
"""

################################################################################
## Standard Library Imports
import sys, os

################################################################################
## Third-Party Imports
from dataclasses import dataclass

################################################################################
## Project Imports
from gc3_query.lib import *

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)



class ATOMLConfig:
    def __init__(self, toml_files: List[Path] = None, dir_path: Path = None) -> None:
        self._name = self.__class__.__name__
        self._toml_files = [Path(p).resolve() for p in toml_files]
        self.dir_path = dir_path.resolve()
        self.toml_files = self._read_toml_files(self.path)
        self.toml_directories = self._load_toml_directory(self.path)

    def _init__toml_file(self, init_toml_path: Path) -> Union[TOMLFile, None]:
        if not init_toml_path.exists():
            return None
        _init_toml_file = TOMLFile(init_toml_path)
        return _init_toml_file

    def _read_toml_files(self, path: Path) -> List[TOMLFile]:
        toml_files = []
        for p in self.path.glob('*.toml'):
            if p.name.startswith('_'):
                _debug(f"Skipping reading file {p}, starts with '_'.")
                continue
            _debug(f"Reading TOMLFile: {p}")
            toml_files.append(TOMLFile(p))
        return toml_files

    def _load_toml_directory(self, path: Path) -> List[TOMLDirectory]:
        toml_directories = []
        for p in path.iterdir():
            if p.name.startswith('_') or p.name.startswith('.'):
                _debug(f"Skipping directory {p}, starts with [._]")
                continue
            if not p.is_dir():
                _debug(f"Skipping {p}, not a directory.")
                continue
            _debug(f"Loading TOMLDirectory: {p}")
            toml_directories.append(TOMLDirectory(p))
        return toml_directories



    def load_file(self, path: Path) -> List[Any]:
        pass
