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
import copy
from collections.abc import Mapping, Sequence

################################################################################
## Third-Party Imports
from dataclasses import dataclass
from melddict import MeldDict

################################################################################
## Project Imports
from gc3_query.lib import *
from gc3_query.lib.atoml.exceptions import *
from gc3_query.lib.atoml.atoml_file import ATomlFile
from gc3_query.lib.atoml.atoml_directory import ATomlDirectory
from gc3_query.lib.gc3logging import get_logging

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


# class ATomlConfig(ATomlDirectory, metaclass=Mapping):
class ATomlConfig(ATomlDirectory):
    def __init__(self, file_paths: Iterable[Path] = None, directory_paths: Union[Path, Iterable[Path]] = None) -> None:
        self._name = self.__class__.__name__
        if not file_paths and not directory_paths:
            raise ATomlConfigError(f"Empty {self._name} created.  Specify at least one atoml file or directory.")

        if isinstance(directory_paths, Path):
            super().__init__(directory_path=directory_paths)
            self.atoml_dir_path = Path(directory_paths).resolve() if directory_paths else None
        elif isinstance(directory_paths, Sequence):
            directory_path = directory_paths.pop(0)
            self.atoml_dir_path = Path(directory_path).resolve()
            super().__init__(directory_path=self.atoml_dir_path)
            if directory_paths:
                self.atoml_directory_paths = [Path(p).resolve() for p in directory_paths]
                self.atoml_directories.extend([ATomlDirectory(directory_path=p) for p in self.atoml_directory_paths])
        else:
            self.atoml_dir_path = None
            super().__init__(directory_path=self.atoml_dir_path)

        self.atoml_file_paths = [Path(p).resolve() for p in file_paths] if file_paths else None

        ## __init__.toml is automatically loaded if it's found in the directory
        self._atoml_settings_file: Union[ATomlFile, None] = self._load_atoml_settings_file(
            atoml_dir_path=self.atoml_dir_path,
            atoml_file_paths=self.atoml_file_paths)
        if self.atoml_file_paths:
            self.atoml_files.extend(self.load_atoml_files(atoml_file_paths=self.atoml_file_paths))
        # self.atoml_files = self._load_atoml_files_from_dir(atoml_dir=self.atoml_dir_path, atoml_files=self.atoml_files) if self.atoml_dir_path else self.atoml_files
        self.toml = self.merged_toml(atoml_settings_file=self._atoml_settings_file,
                                     atoml_files=self.atoml_files,
                                     atoml_directories=self.atoml_directories)

        _debug(f"{self._name} created: {self}")

    # def __str__(self):
    #     return f"<{self._name}>"
    #
    # def __repr__(self):
    #     return self.__str__()

    def __getitem__(self, item):
        return self.toml.__getitem__(item)

    def __iter__(self):
        return self.toml.__iter__()

    def __len__(self):
        return self.toml.__len__()

    def __contains__(self, item):
        return self.toml.__contains__(item)

    def __eq__(self, other):
        return self.toml.__eq__(other)

    def __ne__(self, other):
        return self.toml.__ne__(other)

    def keys(self):
        return self.toml.keys()

    def items(self):
        return self.toml.items()

    def values(self):
        return self.toml.values()

    def get(self, k):
        return self.toml.get(k)

    def _load_atoml_settings_file(self, atoml_dir_path: Path, atoml_file_paths: List[Path]) -> ATomlFile:
        """Loads global settings from __init__.toml file, if present

        :param atoml_file_paths:
        :param atoml_dir_path:
        :return:
        """
        if atoml_dir_path:
            atsf = atoml_dir_path.joinpath('__init__.toml')
            if atsf.exists():
                return ATomlFile(atsf)
        if atoml_file_paths:
            atsf = atoml_file_paths[0].parent.joinpath('__init__.toml')
            if atsf.exists():
                return ATomlFile(atsf)
        return None

    @property
    def file_names(self) -> List[str]:
        if self.atoml_files:
            fn = [tf.file_name for tf in self.atoml_files]
            fn.append(self._atoml_settings_file.file_name)
            return fn
        return [self._atoml_settings_file.file_name]

    def load_atoml_files(self, atoml_file_paths: List[Path]) -> List[ATomlFile]:
        toml_files = []
        for p in atoml_file_paths:
            if p.name.startswith('_') and p.name is not '__init__.toml':
                continue
            if p.name.startswith('_'):
                continue
            toml_files.append(ATomlFile(file_path=p))
        return toml_files

    # def _load_atoml_files_from_dir(self, atoml_dir: Path, atoml_files: Union[List[ATomlFile], None]) -> List[ATomlFile]:
    #     toml_file_paths = [] if atoml_files is None else copy.deepcopy(atoml_files)
    #     for p in atoml_dir.glob('*.toml'):
    #         toml_file_paths.append(p.resolve())
    #     toml_files = self._load_atoml_files(toml_file_paths)
    #     return toml_files

    def _load_atoml_directories(self, atoml_dir: Path) -> List[ATomlDirectory]:
        """

        :param atoml_dir:
        :return:
        """
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

    def merged_toml(self, atoml_settings_file: ATomlFile, atoml_files: List[ATomlFile], atoml_directories: Union[List[ATomlDirectory], None]) -> Dict:
        if not any([atoml_files,  atoml_directories]) and atoml_settings_file:
            _warning(f"{self._name} created with only an __init__.toml file.")
            return copy.deepcopy(atoml_settings_file.toml)
        # mt = copy.deepcopy(atoml_settings_file.toml) if atoml_settings_file else dict()
        mt = MeldDict(atoml_settings_file.toml) if atoml_settings_file else MeldDict({})
        if atoml_files:
            for atf in atoml_files:
                # mt.update(atf.toml)
                mt.add(atf.toml)
        if atoml_directories:
            for atd in atoml_directories:
                # mt.update(atd._toml)
                mt.add(atd._toml)
        return mt

        # raise RuntimeError("should never get here...")
