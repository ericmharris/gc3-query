# -*- coding: utf-8 -*-

"""
#@Filename : spec_overlays
#@Date : [8/11/2018 12:06 PM]
#@Poject: gc3-query
#@AUTHOR : emharris

~~~~~~~~~~~~~~~~

<DESCR SHORT>

<DESCR>
"""

################################################################################
## Standard Library Imports
import sys, os
from copy import deepcopy

################################################################################
## Third-Party Imports
from dataclasses import dataclass, field
import toml
from melddict import MeldDict

################################################################################
## Project Imports
from gc3_query.lib import *
from gc3_query.lib import gc3_cfg
from gc3_query.lib.base_collections import NestedOrderedDictAttrListBase
from gc3_query.lib.signatures import GC3Type, GC3VersionedType, GC3VersionTypedMixin

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

class OpenApiSpecOverlay(GC3VersionTypedMixin):
    """A dict of updates that are applied to correct mistakes in a OpenApiSpec. (eg. spec_dict['schemes'] = ['https'])

    """

    def __init__(self, open_api_spec: 'OpenApiSpec', overlays_spec_dict: DictStrAny=None, idm_cfg: Optional[DictStrAny] = None):
        self.open_api_spec = open_api_spec
        self.api_catalog_config = open_api_spec.api_catalog_config
        self.service_cfg = open_api_spec.service_cfg
        self.idm_cfg = idm_cfg if idm_cfg else open_api_spec.idm_cfg
        self.name = open_api_spec.service_cfg.name
        self.spec_file_path = open_api_spec.spec_file

        self._default_overlays = self.api_catalog_config.open_api_spec_overlays
        # self._default_overlays = deepcopy(self.open_api_spec.api_catalog_config.open_api_spec_overlays)
        self.overlays: MeldDict = MeldDict(self._default_overlays)
        if overlays_spec_dict:
            self.overlays.add(overlays_spec_dict)

        self.spec_dir_path = OPEN_API_CATALOG_DIR.joinpath(open_api_spec.api_catalog_config.api_catalog_name).joinpath(self.service_cfg.service_name)
        self.spec_overlay_format = gc3_cfg.open_api.open_api_spec_overlay.spec_overlay_format
        self.spec_overlay_export_formatting = gc3_cfg[self.spec_overlay_format]['export']['formatting']
        self.spec_overlay_path = self.spec_dir_path.joinpath(f"{self.service_cfg.service_name}_overlay.{self.spec_overlay_format}")

        self.spec_overlay_archive_dir_path = self.spec_dir_path.joinpath(gc3_cfg.open_api.open_api_spec_catalog.archive_dir)
        self.spec_overlay_archive_path = self.spec_overlay_archive_dir_path.joinpath(f"{self.service_cfg.service_name}_overlay_{self.version}.{self.spec_overlay_format}")

        if not self.spec_overlay_path.exists():
            _warning(f"Spec overlay file not found in catalog, saving to {self.spec_file}")
            saved_path = self.save_spec_overlay()

        if not self.spec_overlay_archive_path.exists():
            archived_path = self.archive_spec_overlay_to_catalog()

        self.overlays.add(self.load_spec_overlay())

        _debug(f"{self.name} created")



    def save_spec_overlay(self, file_path: Path = None, overwrite: bool = False) -> Path:
        spec_overlay_path = file_path if file_path else self.spec_overlay_path
        if not spec_overlay_path.parent.exists():
            spec_overlay_path.parent.mkdir()
        _debug(f"Saving spec to spec_overlay_path={spec_overlay_path}")
        if spec_overlay_path.exists() and not overwrite:
            _warning(f"spec_overlay_path={spec_overlay_path} already exists and overwrite={overwrite}, leaving unchanged")
            return spec_overlay_path
        if not self.spec_dir_path.exists():
            _warning(f"spec_dir_path={self.spec_dir_path} did not already exist, attempting to create.")
            self.spec_dir_path.mkdir()
        export_path = self.overlays.export(file_path=spec_overlay_path, format=self.spec_overlay_format, overwrite=overwrite, export_formatting=self.spec_overlay_export_formatting)
        return export_path


    def archive_spec_overlay_to_catalog(self) -> Path:
        _debug(f"Archiving spec overlay to self.spec_archive_file={self.spec_overlay_archive_path}")
        spec_overlay_archive_path = self.spec_overlay_archive_path
        _debug(f"Saving spec to spec_overlay_archive_path={spec_overlay_archive_path}")
        if spec_overlay_archive_path.exists():
            _warning(f"Overlay already exists, spec_overlay_archive_path={spec_overlay_archive_path}")
            return spec_overlay_archive_path
        if not spec_overlay_archive_path.parent.exists():
            spec_overlay_archive_path.parent.mkdir()
        export_path = self.open_api_spec.spec_data.export(file_path=spec_overlay_archive_path, format=self.spec_overlay_format, overwrite=False, export_formatting=self.spec_overlay_export_formatting)
        return export_path



    def load_spec_overlay(self, spec_overlay_path: Path = None) -> MeldDict:
        """

        :param overlay_spec_dict:
        :return:
        """
        spec_overlay_path = spec_overlay_path if spec_overlay_path else self.spec_overlay_path
        with spec_overlay_path.open() as fd:
            overlays = MeldDict(toml.load(f=fd))
        return overlays



    @property
    def title(self) -> str:
        return self.open_api_spec.title

    @property
    def version(self) -> str:
        return self.open_api_spec.version

    @property
    def description(self) -> str:
        return self.open_api_spec.description

    @property
    def descr(self) -> str:
        return self.open_api_spec.descr


    @property
    def paths(self) -> List[str]:
        return self.open_api_spec.paths

    @property
    def operation_ids(self) -> List[str]:
        return self.open_api_spec.operation_ids

    @property
    def operation_id_descrs(self) -> DictStrAny:
        return self.open_api_spec.operation_id_descrs
