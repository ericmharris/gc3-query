import pytest
import toml
from pathlib import Path
import json
# from pprint import pprint, pformat
from prettyprinter import pprint, pformat

from gc3_query.lib import *
from gc3_query.lib import BASE_DIR
from gc3_query.lib.base_collections import NestedOrderedDictAttrListBase

from gc3_query.lib.gc3_config import GC3Config, IDMCredential
from gc3_query.lib.iaas_classic.iaas_requests_http_client import IaaSRequestsHTTPClient
from gc3_query.lib.iaas_classic import IaaSServiceBase, API_SPECS_DIR, IaaSRequestsHTTPClient
from gc3_query.lib.iaas_classic import BRAVADO_CONFIG
from gc3_query.lib.iaas_classic.ssh_keys import SSHKeys

from bravado_core.spec import Spec
from bravado_core.response import unmarshal_response
from bravado_core.param import marshal_param

TEST_BASE_DIR: Path = Path(__file__).parent
# config_dir = TEST_BASE_DIR.joinpath("config")
config_dir = BASE_DIR.joinpath("etc/config")
output_dir = TEST_BASE_DIR.joinpath('output')
spec_files_dir = TEST_BASE_DIR.joinpath('spec_files')


def test_setup():
    assert TEST_BASE_DIR.exists()
    assert API_SPECS_DIR.exists()
    if not config_dir.exists():
        config_dir.mkdir()
    if not output_dir.exists():
        output_dir.mkdir()
    if not spec_files_dir.exists():
        spec_files_dir.mkdir()

def test_init():
    m = dict(name='foo')
    d = NestedOrderedDictAttrListBase(mapping=m)
    assert d


@pytest.fixture()
def test_data_setup():
    gc3_config = GC3Config()
    assert gc3_config
    assert isinstance(gc3_config.iaas_classic, NestedOrderedDictAttrListBase)
    iaas_classic = gc3_config.iaas_classic
    bravado = gc3_config.bravado
    return iaas_classic, bravado



def test_as_dict(test_data_setup):
    iaas_classic, bravado = test_data_setup
    assert iaas_classic
    assert isinstance(iaas_classic, NestedOrderedDictAttrListBase)
    assert isinstance(iaas_classic.as_dict(), dict)



def test_as_dict_melded_with(test_data_setup):
    iaas_classic, bravado = test_data_setup
    assert iaas_classic
    assert isinstance(iaas_classic, NestedOrderedDictAttrListBase)
    assert isinstance(iaas_classic.as_dict(), dict)
    melded = iaas_classic.as_dict_melded_with(bravado)
    assert isinstance(melded, dict)
