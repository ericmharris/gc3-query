# -*- coding: utf-8 -*-

"""
gc3-query.toml_directory    [6/1/2018 10:50 AM]
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
from gc3_query.lib.atoml_cfg.atoml_file import ATomlFile

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


class ATomlDirectory:

    def __init__(self, path: Path) -> None:
        self._name = self.__class__.__name__
        self.path = path.resolve()
        self.atoml_files = self._read_toml_files(self.path)
        self.atoml_directories: List[ATomlDirectory] = []
        self.toml_directories = self._load_toml_directory(self.path)


    def _read_toml_files(self, path: Path) -> List[ATomlFile]:
        toml_files = []
        for p in self.path.glob('*.toml'):
            if p.name.startswith('_'):
                _debug(f"Skipping reading file {p}, starts with '_'.")
                continue
            _debug(f"Reading TOMLFile: {p}")
            toml_files.append(ATomlFile(p))
        return toml_files


    def _load_toml_directory(self, path: Path) -> List["ATomlDirectory"]:
        toml_directories = []
        for p in path.iterdir():
            if p.name.startswith('_') or p.name.startswith('.'):
                _debug(f"Skipping directory {p}, starts with [._]")
                continue
            if not p.is_dir():
                _debug(f"Skipping {p}, not a directory.")
                continue
            _debug(f"Loading TOMLDirectory: {p}")
            toml_directories.append(ATomlDirectory(p))
        return toml_directories
