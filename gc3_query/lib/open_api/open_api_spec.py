# -*- coding: utf-8 -*-

"""
#@Filename : open_api_spec
#@Date : [8/9/2018 2:05 PM]
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
from functools import total_ordering
import json

################################################################################
## Third-Party Imports
from dataclasses import dataclass
from bravado_core.spec import Spec
from bravado.swagger_model import load_file, load_url
from melddict import MeldDict
from bravado_core.spec import Spec
import toml
from toml import TomlDecodeError

################################################################################
## Project Imports
from gc3_query.lib import *
from gc3_query.lib.base_collections import NestedOrderedDictAttrListBase
from gc3_query.lib.signatures import GC3Type, GC3VersionedType, GC3VersionTypedMixin
from gc3_query.lib.iaas_classic.iaas_swagger_client import  BRAVADO_CONFIG

_debug, _info, _warning, _error, _critical = get_logging(name=__name__)


@dataclass()
class OperationIdDescr():
    operation_id: str
    path: str
    http_method: str
    description: str
    consumes: str
    produces: str
    parameters: List[Tuple[str, str]]


# @dataclass()
# class OperationID():
#     operation_id: str
#     summary: str
#     path: str


class OpenApiSpec(GC3VersionTypedMixin):

    def __init__(self, api_catalog_config: DictStrAny,
                 service_cfg: Dict[str, Any],
                 from_url: Optional[bool] = False,
                 idm_cfg: Optional[DictStrAny] = None,
                 **kwargs):
        self.api_catalog_config = api_catalog_config
        self.service_cfg = service_cfg
        self.idm_cfg = idm_cfg
        self.name = service_cfg.name

        self.kwargs = {'rest_endpoint': None,   #
                       'mock_version': None,    # Used for unit tests,
                       }
        self.kwargs.update(kwargs)
        #  The ultimate form of the Spec depends on the specific REST Endpoint of a given IDM domain which differs from the API Catalog.
        self.rest_endpoint = kwargs.get('rest_endpoint', None)
        if not self.rest_endpoint:
            self.rest_endpoint = idm_cfg['rest_endpoint'] if idm_cfg else self.rest_endpoint

        self.spec_dir: Path = OPEN_API_CATALOG_DIR.joinpath(api_catalog_config.api_catalog_name).joinpath(service_cfg.service_name)
        self.spec_file: Path = self.spec_dir.joinpath(f"{service_cfg.service_name}.json")

        self.spec_overlay_format = gc3_cfg.open_api.open_api_spec_overlay.spec_overlay_format
        self.spec_overlay_export_formatting = gc3_cfg[self.spec_overlay_format]['export']['formatting']
        self.spec_overlay_file: Path = self.spec_dir.joinpath(f"{self.service_cfg.service_name}_overlay.{self.spec_overlay_format}")

        self._vanilla_spec_dict = self.load_spec(from_url=from_url)
        self._overlaid_spec_dict = MeldDict(self._vanilla_spec_dict)


        # self.spec_dict = self.create_api_spec(spec_dict=self._spec_dict)
        # self.api_spec_overlay = OpenApiSpecOverlay(open_api_spec=self, idm_cfg=self.idm_cfg)
        if not self.spec_overlay_file.exists():
            _ = self.create_spec_overlay_file(file_path=self.spec_overlay_file)
        self.spec_overlays: MeldDict = self.load_spec_overlay_file()
        self.spec_deletions: MeldDict = MeldDict(self.api_catalog_config.open_api_spec_deletions)

        ## Adding the default overlays gave schemes: ['http', 'https']
        self._overlaid_spec_dict.subtract(self.spec_deletions)
        self._overlaid_spec_dict.add(self.spec_overlays)
        self.spec_data = NestedOrderedDictAttrListBase(mapping=self._overlaid_spec_dict)


        self.spec_archive_dir = self.spec_dir.joinpath(gc3_cfg.open_api.open_api_spec_catalog.archive_dir)
        self.spec_archive_file_name = gc3_cfg.open_api.open_api_spec_catalog.archive_file_format.format(name=self.name, version=self.version)
        self.spec_archive_file = self.spec_archive_dir.joinpath(self.spec_archive_file_name)
        self.spec_overlay_archive_dir: Path = self.spec_dir.joinpath(gc3_cfg.open_api.open_api_spec_catalog.archive_dir)
        self.spec_overlay_archive_file: Path = self.spec_overlay_archive_dir.joinpath(f"{self.service_cfg.service_name}_overlay_{self.version}.{self.spec_overlay_format}")
        self.spec_export_dir: Path = BASE_DIR.joinpath('var/open_api_catalog', api_catalog_config.api_catalog_name, service_cfg.service_name)
        _debug(f"self.spec_dir={self.spec_dir}\nself.spec_file={self.spec_file}\nself.spec_export_dir={self.spec_export_dir}")

        if not self.spec_file.exists():
            _warning(f"Spec file not found in catalog, saving to {self.spec_file}")
            _ = self.save_spec()

        if not all([p.exists() for p in self.export_paths.values()]):
            _ = self.export()
            _debug(f"Exported files not found in var, created export files: {self.export_paths.values()}")

        if not self.spec_archive_file.exists():
            _ = self.archive_spec_to_catalog()

        if not self.spec_overlay_file.exists():
            _warning(f"Spec overlay file not found in catalog, saving to {self.spec_file}")
            _ = self.save_spec_overlay()

        if not self.spec_overlay_archive_file.exists():
            _ = self.archive_spec_overlay_to_catalog()

        _debug(f"{self.name} created")

    def load_spec(self, from_url: bool) -> DictStrAny:
        if from_url:
            spec_url = f"{self.service_cfg.spec_furl}".format_map(self.service_cfg)
            _debug(f"spec_url={spec_url}")
            spec_dict: dict = load_url(spec_url=spec_url)
            self.from_url = True
        else:
            if not self.spec_file.exists():
                _warning(f"Spec file not found: {self.spec_file}!\nAttempting to load it from the API Catalog")
                return self.load_spec(from_url=True)
            spec_file_path = str(self.spec_file)
            spec_dict: dict = load_file(spec_file=spec_file_path)
            self.from_url = False
        return spec_dict

    def save_spec(self, file_path=None, overwrite: bool = False) -> Path:
        spec_file = file_path if file_path else self.spec_file
        if not spec_file.parent.exists():
            spec_file.parent.mkdir()
        _debug(f"Saving spec to spec_file={spec_file}")
        if spec_file.exists() and not overwrite:
            _warning(f"spec_file={spec_file} already exists and overwrite={overwrite}, leaving unchanged")
        if not self.spec_dir.exists():
            _warning(f"spec_dir={self.spec_dir} did not already exist, attempting to create.")
            self.spec_dir.mkdir()
        try:
            json.dump(obj=self._vanilla_spec_dict, fp=spec_file.open('w'), indent=gc3_cfg.open_api.open_api_spec_catalog.json_export_indent_spaces)
        except Exception as e:
            _error(e)
        return spec_file

    def archive_spec_to_catalog(self) -> Path:
        _debug(f"Archiving spec to self.spec_archive_file={self.spec_archive_file}")
        spec_archive_file_path = self.save_spec(file_path=self.spec_archive_file)
        return spec_archive_file_path


    def create_spec_overlay_file(self, file_path: Path = None, overwrite: bool = False) -> Path:
        default_overlays = self.api_catalog_config.open_api_spec_overlays
        default_overlays = NestedOrderedDictAttrListBase(mapping=default_overlays)
        exported_file = default_overlays.export(file_path=file_path, format=self.spec_overlay_format)
        return exported_file


    def save_spec_overlay(self, file_path: Path = None, overwrite: bool = False) -> Path:
        spec_overlay_file = file_path if file_path else self.spec_overlay_file
        if not spec_overlay_file.parent.exists():
            spec_overlay_file.parent.mkdir()
        _debug(f"Saving spec to spec_overlay_file={spec_overlay_file}")
        if spec_overlay_file.exists() and not overwrite:
            _warning(f"spec_overlay_file={spec_overlay_file} already exists and overwrite={overwrite}, leaving unchanged")
            return spec_overlay_file
        if not self.spec_dir.exists():
            _warning(f"spec_dir={self.spec_dir} did not already exist, attempting to create.")
            self.spec_dir.mkdir()
        export_path = self.spec_data.export(file_path=spec_overlay_file, format=self.spec_overlay_format, overwrite=overwrite, export_formatting=self.spec_overlay_export_formatting)
        return export_path


    def archive_spec_overlay_to_catalog(self) -> Path:
        _debug(f"Archiving spec overlay to self.spec_archive_file={self.spec_archive_file}")
        spec_overlay_archive_path = self.spec_overlay_archive_file
        _debug(f"Saving spec to spec_overlay_archive_path={spec_overlay_archive_path}")
        if spec_overlay_archive_path.exists():
            _warning(f"Overlay already exists, spec_overlay_archive_path={spec_overlay_archive_path}")
            return spec_overlay_archive_path
        if not spec_overlay_archive_path.parent.exists():
            spec_overlay_archive_path.parent.mkdir()
        export_path = self.spec_data.export(file_path=spec_overlay_archive_path, format=self.spec_overlay_format, overwrite=False,
                                            export_formatting=self.spec_overlay_export_formatting)
        return export_path

    def load_spec_overlay_file(self, spec_overlay_file: Path = None) -> MeldDict:
        """

        :param overlay_spec_dict:
        :return:
        """
        spec_overlay_file = spec_overlay_file if spec_overlay_file else self.spec_overlay_file
        with spec_overlay_file.open() as fd:
            try:
                overlays = MeldDict(toml.load(f=fd))
            except TomlDecodeError as e:
                _error(f"TomlDecodeError while loading spec overlay: {fd}")
                raise
        return overlays

    @property
    def spec_dict(self):
        return self._overlaid_spec_dict


    def get_swagger_spec(self, rest_endpoint: Union[str, None] = None) -> Spec:
        """

        :param rest_endpoint:
        :return:
        """
        rest_endpoint = rest_endpoint if rest_endpoint else self.rest_endpoint
        if not rest_endpoint:
            raise RuntimeError("rest_endpoint not provided in either method call or in **wkargs={self.kwargs}")
        core_spec: Spec = Spec(spec_dict=self.spec_dict, origin_url=rest_endpoint, http_client=None, config=BRAVADO_CONFIG)
        #### bravado_core.spec.Spec#client_spec_dict
        # Return a copy of spec_dict with x-scope metadata removed so that it
        #         is suitable for consumption by Swagger clients.
        client_spec_dict = core_spec.client_spec_dict
        return client_spec_dict

    @property
    def swagger_spec(self) -> Spec:
        return self.get_swagger_spec(rest_endpoint=self.rest_endpoint)

    @property
    def title(self) -> str:
        return self.spec_data.info.title

    @property
    def version(self) -> str:
        if self.kwargs.get('mock_version', False):
            return self.kwargs.get('mock_version')
        return self.spec_data.info.version

    @property
    def description(self) -> str:
        return self.spec_data.info.description

    @property
    def descr(self) -> str:
        return self.spec_data.info.description

    @property
    def paths(self) -> List[str]:
        paths = self.spec_data.paths.keys()
        return list(paths)

    @property
    def operation_ids(self) -> List[str]:
        ids = []
        for path in self.paths:
            for http_method in self.spec_data.paths[path].keys():
                ids.append(self.spec_data.paths[path][http_method]['operationId'])
        return ids

    @property
    def operation_id_descrs(self) -> DictStrAny:
        operation_ids_d = {id: None for id in self.operation_ids}
        for path in self.paths:
            for http_method in self.spec_data.paths[path].keys():
                operation_spec = self.spec_data.paths[path][http_method]
                operation_id = operation_spec.operationId
                id_descr = OperationIdDescr(operation_id=operation_id,
                                            path=path,
                                            http_method=http_method,
                                            description=operation_spec.description,
                                            consumes=operation_spec.consumes,
                                            produces=operation_spec.produces,
                                            parameters=operation_spec.parameters
                                            )
                operation_ids_d[operation_id] = id_descr
        return operation_ids_d

    @property
    def export_paths(self):
        export_formats = ['json', 'yaml', 'toml']
        export_paths = {export_format: self.spec_export_dir.joinpath(f"{self.name}.{export_format}") for export_format in export_formats}
        _debug(f"export_formats={export_formats}, export_paths={export_paths}")
        return export_paths

    def export(self) -> List[Path]:
        exported_file_paths: List[Path] = []
        if not self.spec_export_dir.exists():
            _warning(f"spec_export_dir={self.spec_export_dir} did not exist, attempting to create.")
            self.spec_export_dir.mkdir()
        for f, p in self.export_paths.items():
            exported_file_path = self.spec_data.export(file_path=p, format=f, overwrite=True)
            exported_file_paths.append(exported_file_path)
        return exported_file_paths
