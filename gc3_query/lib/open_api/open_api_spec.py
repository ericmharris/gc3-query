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

################################################################################
## Project Imports
from gc3_query.lib import *
from gc3_query.lib.base_collections import NestedOrderedDictAttrListBase
from gc3_query.lib.signatures import GC3Type, GC3VersionedType, GC3VersionTypedMixin

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

        self.kwargs = kwargs
        #  The ultimate form of the Spec depends on the specific REST Endpoint of a given IDM domain which differs from the API Catalog.
        self.rest_endpoint = kwargs.get('rest_endpoint', None)
        if not self.rest_endpoint:
            self.rest_endpoint = idm_cfg['rest_endpoint'] if idm_cfg else self.rest_endpoint

        self.spec_dir_path = OPEN_API_CATALOG_DIR.joinpath(api_catalog_config.api_catalog_name).joinpath(service_cfg.service_name)
        self.spec_file_path = self.spec_dir_path.joinpath(f"{service_cfg.service_name}.json")
        self.spec_export_dir_path = BASE_DIR.joinpath('var/open_api_catalog', api_catalog_config.api_catalog_name, service_cfg.service_name)
        _debug(f"self.spec_dir_path={self.spec_dir_path}\nself.spec_file_path={self.spec_file_path}\nself.spec_export_dir_path={self.spec_export_dir_path}")

        self._spec_dict = self.load_spec(from_url=from_url)
        self._api_spec_dict = self.create_api_spec(spec_dict=self._spec_dict)
        self.api_spec = NestedOrderedDictAttrListBase(mapping=self._api_spec_dict)
        if not self.spec_file_path.exists():
            _warning(f"Spec file not found in catalog, saving to {self.spec_file_path}")
            saved_path = self.save_spec_to_catalog()
            exported_paths = self.export()
        _debug(f"{self.name} created")

        # self.gc3_type = GC3Type(name=__class__.__name__,
        #                                  descr="OpenApiSpec is a wrapper around bravado.Spec for Oracle Cloud.",
        #                                  class_type=__class__)
        #
        # self.gc3_vtype = GC3VersionedType(name=__class__.__name__,
        #                    descr="OpenApiSpec is a wrapper around bravado.Spec for Oracle Cloud.",
        #                    class_type=__class__, version=self.version)

    def load_spec(self, from_url: bool) -> DictStrAny:
        if from_url:
            spec_url = f"{self.service_cfg.spec_furl}".format_map(self.service_cfg)
            _debug(f"spec_url={spec_url}")
            spec_dict: dict = load_url(spec_url=spec_url)
            self.from_url = True
        else:
            if not self.spec_file_path.exists():
                _warning(f"Spec file not found: {self.spec_file_path}!\nAttempting to load it from the API Catalog")
                return self.load_spec(from_url=True)
            spec_file_path = str(self.spec_file_path)
            spec_dict: dict = load_file(spec_file=spec_file_path)
            self.from_url = False
        return spec_dict


    def save_spec_to_catalog(self, overwrite: bool = False) -> Path:
        _debug(f"Saving spec to self.spec_file_path={self.spec_file_path}")
        if self.spec_file_path.exists() and not overwrite:
            raise RuntimeError(f"Can not save with overwrite={overwrite}, spec file already exists!")
        if not self.spec_dir_path.exists():
            _warning(f"spec_dir_path={self.spec_dir_path} did not already exist, attempting to create.")
            self.spec_dir_path.mkdir()
        json.dump(obj=self._spec_dict, fp=self.spec_file_path.open('w'), indent=gc3_cfg.open_api.open_api_spec_catalog.json_export_indent_spaces)
        return self.spec_file_path



    def create_api_spec(self, spec_dict: DictStrAny) -> DictStrAny:
        """Returns a new spec_dict that sucks less

        :param spec_dict:
        :return:
        """
        spec_dict = deepcopy(spec_dict)
        spec_dict['schemes'] = ['https']
        return spec_dict

    def get_bravado_spec(self, rest_endpoint: Union[str, None] = None) -> Spec:
        """

        :param rest_endpoint:
        :return:
        """
        rest_endpoint = rest_endpoint if rest_endpoint else self.rest_endpoint
        if not rest_endpoint:
            raise RuntimeError("rest_endpoint not provided in either method call or in **wkargs={self.kwargs}")
        core_spec: Spec = Spec(spec_dict=self._api_spec_dict, origin_url=rest_endpoint, http_client=None, config=gc3_cfg.swagger_client_config)
        return core_spec

    @property
    def title(self) -> str:
        return self.api_spec.info.title

    @property
    def version(self) -> str:
        if self.kwargs.get('mock_version', False):
            return self.kwargs.get('mock_version')
        return self.api_spec.info.version

    @property
    def description(self) -> str:
        return self.api_spec.info.description

    @property
    def descr(self) -> str:
        return self.api_spec.info.description


    @property
    def paths(self) -> List[str]:
        paths = self.api_spec.paths.keys()
        return list(paths)

    @property
    def operation_ids(self) -> List[str]:
        ids = []
        for path in self.paths:
            for http_method in self.api_spec.paths[path].keys():
                ids.append(self.api_spec.paths[path][http_method]['operationId'])
        return ids

    @property
    def operation_id_descrs(self) -> DictStrAny:
        operation_ids_d = {id:None for id in self.operation_ids}
        for path in self.paths:
            for http_method in self.api_spec.paths[path].keys():
                operation_spec = self.api_spec.paths[path][http_method]
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


    def export(self) -> List[Path]:
        exported_file_paths: List[Path] = []
        export_formats = ['json', 'yaml', 'toml']
        export_paths = {export_format:self.spec_export_dir_path.joinpath(f"{self.name}.{export_format}") for export_format in export_formats}
        _debug(f"export_formats={export_formats}, export_paths={export_paths}")
        if not self.spec_export_dir_path.exists():
            _warning(f"spec_export_dir_path={self.spec_export_dir_path} did not exist, attempting to create.")
            self.spec_export_dir_path.mkdir()
        for f,p in export_paths.items():
            exported_file_path = self.api_spec.export(file_path=p, format=f, overwrite=True)
            exported_file_paths.append(exported_file_path)
        return exported_file_paths

    # def __eq__(self, other):
    #     same_title = self.title==other.title
    #     same_version = self.version==other.version
    #     is_eq = all([same_title, same_version])
    #     return is_eq


