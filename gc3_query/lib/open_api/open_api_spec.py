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
import yaml
import json
import toml
from urllib.parse import urlparse, ParseResult
from copy import deepcopy
from bravado.swagger_model import load_file, load_url
from bravado_core.spec import Spec
################################################################################
## Third-Party Imports
from dataclasses import dataclass
from melddict import MeldDict
from toml import TomlDecodeError
from swagger_spec_validator import validator20

################################################################################
## Project Imports
from gc3_query.lib import *
from gc3_query.lib.base_collections import NestedOrderedDictAttrListBase
# from gc3_query.lib.iaas_classic.iaas_swagger_client import BRAVADO_CONFIG
from gc3_query.lib.signatures import GC3VersionTypedMixin
# from . import OPEN_API_CATALOG_DIR

from gc3_query.lib import get_logging
from gc3_query.lib.gc3_bravado import bravado_cfg
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


# class OpenApiSpec():
class OpenApiSpec(GC3VersionTypedMixin):
    def __init__(self, service_cfg: Union[NestedOrderedDictAttrListBase, DictStrAny],
                 open_api_specs_cfg: Union[NestedOrderedDictAttrListBase, DictStrAny],
                 idm_cfg: Optional[Union[NestedOrderedDictAttrListBase, DictStrAny]] = None, **kwargs):
        self.service_cfg = service_cfg
        self.open_api_specs_cfg = open_api_specs_cfg
        self.idm_cfg = idm_cfg
        self.name = service_cfg.name
        self._title = service_cfg.title
        self.api_collection_name = service_cfg.api_collection_name
        self.api_version = service_cfg.api_version

        self.kwargs = {'rest_endpoint': None,   #
                       'mock_version': None,    # Used for unit tests,
                       }
        self.kwargs.update(kwargs)

        #  The ultimate form of the Spec depends on the specific REST Endpoint of a given IDM domain which differs from the API Catalog.
        # self.rest_endpoint = kwargs.get('rest_endpoint', None)
        # if not self.rest_endpoint:
        #     self.rest_endpoint = idm_cfg['rest_endpoint'] if idm_cfg else self.rest_endpoint

        self.spec_dir: Path = gc3_cfg.OPEN_API_SPEC_BASE.joinpath(open_api_specs_cfg.cloud_service_name, service_cfg.api_collection_name)
        self.spec_file: Path = self.spec_dir.joinpath(f"{service_cfg.name}.{open_api_specs_cfg.file_format}")
        self.spec_export_dir: Path = gc3_cfg.BASE_DIR.joinpath(gc3_cfg.open_api.export.export_dir,  self.open_api_specs_cfg.cloud_service_name, service_cfg.api_collection_name)
        self._spec_dict = yaml.load(self.spec_file.open())
        self._spec_data = NestedOrderedDictAttrListBase(mapping=self._spec_dict)

        _debug(f"{self.name} created")


    def __str__(self):
        s = f"<{self.__class__.__name__}: {self.spec_file.name}>"
        return s

    def __repr__(self):
        return self.__str__()

    @property
    def spec_dict(self):
        """Return a spec_dict updated with correct host, etc. for this service

        :return:
        """
        rest_parse_result: ParseResult = urlparse(self.rest_endpoint)
        updated_spec_dict = deepcopy(self._spec_dict)
        updated_spec_dict['host'] = rest_parse_result.netloc
        # if 'tags' not in updated_spec_dict:
        #     updated_spec_dict['tags'] = []
        # updated_spec_dict['tags'].append('gc3')
        return updated_spec_dict

    @property
    def rest_endpoint(self):
        from_kwargs = self.kwargs.get('rest_endpoint', False)
        if from_kwargs:
            return from_kwargs
        if 'rest_endpoint' in self.service_cfg:
            return self.service_cfg.rest_endpoint
        return self.idm_cfg.rest_endpoint

    def get_swagger_spec(self, rest_endpoint: Union[str, None] = None) -> Spec:
        """

        :param rest_endpoint:
        :return:
        """
        rest_endpoint = rest_endpoint if rest_endpoint else self.rest_endpoint
        if not rest_endpoint:
            raise RuntimeError("rest_endpoint not provided in either method call or in **wkargs={self.kwargs}")
        # spec: Spec = Spec(spec_dict=self.spec_dict, origin_url=rest_endpoint, http_client=None, config=gc3_cfg.BRAVADO_CONFIG)
        spec: Spec = Spec(spec_dict=self.spec_dict, origin_url=rest_endpoint, http_client=None, config=bravado_cfg.BRAVADO_CONFIG)
        #### bravado_core.spec.Spec#client_spec_dict
        # Return a copy of spec_dict with x-scope metadata removed so that it
        #         is suitable for consumption by Swagger clients.
        # client_spec_dict = spec.client_spec_dict
        return spec

    @property
    def spec(self) -> Spec:
        return self.get_swagger_spec(rest_endpoint=self.rest_endpoint)

    def build(self) -> bool:
        _ = self.spec.build()
        return True


    def validate(self) -> bool:
        """
    def _validate_spec(self):
        if self.config['validate_swagger_spec']:
            self.resolver = validator20.validate_spec(
                spec_dict=self.spec_dict,
                spec_url=self.origin_url or '',
                http_handlers=build_http_handlers(self.http_client),
            )



        :return:
        """
        raise RuntimeError('Todo:  look at Spec._validate, etc.')


    @property
    def title(self) -> str:
        return self._spec_data.info.title

    @property
    def version(self) -> str:
        if self.kwargs.get('mock_version', False):
            return self.kwargs.get('mock_version')
        return self._spec_data.info.version

    @property
    def description(self) -> str:
        return self._spec_data.info.description

    @property
    def descr(self) -> str:
        return self._spec_data.info.description

    @property
    def paths(self) -> List[str]:
        paths = self._spec_data.paths.keys()
        return list(paths)

    @property
    def operation_ids(self) -> List[str]:
        ids = []
        for path in self.paths:
            for http_method in self._spec_data.paths[path].keys():
                ids.append(self._spec_data.paths[path][http_method]['operationId'])
        return ids

    @property
    def operation_id_descrs(self) -> DictStrAny:
        operation_ids_d = {id: None for id in self.operation_ids}
        for path in self.paths:
            for http_method in self._spec_data.paths[path].keys():
                operation_spec = self._spec_data.paths[path][http_method]
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
            exported_file_path = self._spec_data.export(file_path=p, format=f, overwrite=True)
            exported_file_paths.append(exported_file_path)
        return exported_file_paths
