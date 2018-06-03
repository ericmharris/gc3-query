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
from gc3_query.lib.atoml_cfg.exceptions import *
from gc3_query.lib.atoml_cfg.atoml_file import ATomlFile
from gc3_query.lib.atoml_cfg.atoml_directory import ATomlDirectory

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


class ATomlConfig:
    def __init__(self, atoml_files: List[Union[Path, str]] = None, atoml_dir: Union[Path, str] = None) -> None:
        self._name = self.__class__.__name__
        if not atoml_files or atoml_dir:
            raise ATomlConfigError(f"Empty {self._name} created.  Specify at least one atoml file or directory.")
        self._toml_file_paths = [Path(p).resolve() for p in atoml_files] if atoml_files else None
        self._atoml_dir_path = Path(atoml_dir).resolve() if atoml_dir else None


        self._init_atoml_file = self._load_init_atoml_file(self.path.joinpath('__init__.toml')) if atoml_dir else None

        self.atoml_files = self._load_atoml_files(self._toml_file_paths)
        self.atoml_directories = self._load_atoml_directories(self.path)


    def _load_init_atoml_file(self, init_toml_path: Path) -> Union[ATomlFile, None]:
        if not init_toml_path.exists():
            return None
        _init_toml_file =  ATomlFile(init_toml_path)
        return _init_toml_file


    def _load_atoml_files(self, paths: List[Path]) -> List[ATomlFile]:
        toml_files = []
        for p in self.path.glob('*.toml'):
            if p.name.startswith('_'):
                _debug(f"Skipping reading file {p}, starts with '_'.")
                continue
            _debug(f"Reading ATomlFile: {p}")
            toml_files.append(ATomlFile(p))
        return toml_files

    def _load_atoml_directories(self, atoml_dir: Path) -> List[ATomlDirectory]:
        toml_directories = []
        for p in atoml_dir.iterdir():
            if p.name.startswith('_') or p.name.startswith('.'):
                _debug(f"Skipping directory {p}, starts with [._]")
                continue
            if not p.is_dir():
                _debug(f"Skipping {p}, not a directory.")
                continue
            _debug(f"Loading ATomlDirectory: {p}")
            toml_directories.append(ATomlDirectory(p))
        return toml_directories



    def load_file(self, path: Path) -> List[Any]:
        pass
