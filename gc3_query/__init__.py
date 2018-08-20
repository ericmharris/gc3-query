# -*- coding: utf-8 -*-

"""Top-level package for GC3 Query."""
from pathlib import Path
from gc3_query.lib import gc3_cfg

__author__ = """Eric Harris"""
__email__ = 'eric.harris@oracle.com'
__version__ = '0.1.0'



BASE_DIR = gc3_cfg.BASE_DIR
CONFIG_DIR = gc3_cfg.CONFIG_DIR
API_SPECS_DIR = BASE_DIR.joinpath('lib/iaas_classic/api_specs')
OPEN_API_CATALOG_DIR: Path = BASE_DIR.joinpath(gc3_cfg.open_api.open_api_spec_catalog.api_catalog_dir)
