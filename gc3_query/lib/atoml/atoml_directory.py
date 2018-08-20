# -*- coding: utf-8 -*-

"""
gc3-query.toml_directory    [6/1/2018 10:50 AM]
~~~~~~~~~~~~~~~~

<DESCR SHORT>

<DESCR>
"""

################################################################################
## Standard Library Imports

################################################################################
## Third-Party Imports
from melddict import MeldDict

################################################################################
## Project Imports
from gc3_query.lib import *
from gc3_query.lib.atoml.atoml_file import ATomlFile
from gc3_query.lib.atoml.exceptions import *
from gc3_query.lib.gc3logging import get_logging

from gc3_query.lib import get_logging
_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


class ATomlDirectory:

    def __init__(self, directory_path: Union[Path, None]) -> None:
        self._name = self.__class__.__name__
        self.directory_path: Union[Path, None] = None
        self.directory_name: Union[str, None] = None
        self.atoml_files: List[ATomlFile] = []
        self.atoml_directories: List[ATomlDirectory] = []
        if directory_path:
            self.directory_path = directory_path.resolve()
            self.directory_name = self.directory_path.name
            self.atoml_files = self._load_atoml_files(directory_path=self.directory_path)
            self.atoml_directories: List[ATomlDirectory] = self._load_atoml_directories(self.directory_path)

        self._toml = self._merge_toml(atoml_files=self.atoml_files, atoml_directories=self.atoml_directories)
        _debug(f"{self._name} created: {self}")

    def __str__(self):
        return f"<{self._name}: directory_name={self.directory_name}>"

    def __repr__(self):
        return self.__str__()

    def _read_toml_files(self, path: Path) -> List[ATomlFile]:
        toml_files = []
        for p in self.directory_path.glob('*.toml'):
            if p.name.startswith('_'):
                _debug(f"Skipping reading file {p}, starts with '_'.")
                continue
            _debug(f"Reading TOMLFile: {p}")
            toml_files.append(ATomlFile(p))
        return toml_files


    def _load_atoml_directories(self, directory_path: Path) -> List["ATomlDirectory"]:
        toml_directories = []
        for p in directory_path.iterdir():
            if p.is_dir():
                _debug(f"Loading TOMLDirectory: {p}")
                toml_directories.append(ATomlDirectory(p))
        return toml_directories


    def _load_atoml_files(self, directory_path: Path) -> List[ATomlFile]:
        if not directory_path.exists() and self.directory_path.is_dir():
            raise ATomlConfigError(f"Empty {self._name} created.  Specify at least one atoml file or directory.")

        toml_files = []
        at_file_paths = directory_path.glob('*.toml')
        for p in at_file_paths:
            if p.name.startswith('_') and p.name is not '__init__.toml':
                continue
            if p.name.startswith('_'):
                continue
            toml_files.append(ATomlFile(file_path=p))
        return toml_files


    def _load_atoml_dir(self, atoml_dir: Path) -> List[ATomlFile]:
        toml_files = self._load_atoml_files(atoml_dir)
        return toml_files

    def _merge_toml(self, atoml_files: Union[List[ATomlFile], None], atoml_directories: Union[List["ATomlDirectory"], None]) -> Union[Dict, None]:
        if not any([atoml_files,  atoml_directories]):
            _warning(f"Empty toml merge on {self._name}.")
            return
        mt = MeldDict({})
        if atoml_files:
            # toml_dicts = [atf.toml for atf in atoml_files]
            # mt =  dict(*toml_dicts)
            for atf in atoml_files:
                mt.add(atf.toml)
        if atoml_directories:
            # dir_toml_dicts = [atd._toml for atd in atoml_directories]
            # mt = ChainMap(mt, *dir_toml_dicts)
            for atd in atoml_directories:
                mt.add(atd._toml)
        return mt
