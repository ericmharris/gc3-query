import pytest
import toml
from pathlib import Path
import json
# from pprint import pprint, pformat
from prettyprinter import pprint, pformat

from gc3_query.lib import *
from gc3_query.lib import gc3_cfg
from gc3_query import BASE_DIR
from gc3_query.lib.base_collections import NestedOrderedDictAttrListBase

from gc3_query.lib.gc3_config import GC3Config, IDMCredential
from gc3_query.lib.iaas_classic.iaas_requests_http_client import IaaSRequestsHTTPClient
from gc3_query.lib.iaas_classic import IaaSServiceBase, IaaSRequestsHTTPClient
from gc3_query.lib.open_api import API_SPECS_DIR
from gc3_query.lib.iaas_classic import BRAVADO_CONFIG
from gc3_query.lib.iaas_classic.ssh_keys import SSHKeys

from bravado_core.spec import Spec
from bravado_core.response import unmarshal_response
from bravado_core.param import marshal_param

TEST_BASE_DIR: Path = Path(__file__).parent
config_dir = TEST_BASE_DIR.joinpath("config")
# config_dir = BASE_DIR.joinpath("etc/config")
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
    gc3_config = GC3Config(atoml_config_dir=config_dir)
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


@pytest.fixture()
def test_chainmap_instead_of_melddict_setup():
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    assert gc3_config
    assert isinstance(gc3_config.iaas_classic, NestedOrderedDictAttrListBase)
    gc3pilot = gc3_config.idm.domains.gc3pilot
    gc35001 = gc3_config.idm.domains.gc35001
    return gc3pilot, gc35001


def test_add(test_chainmap_instead_of_melddict_setup):
    gc3pilot, gc35001 = test_chainmap_instead_of_melddict_setup
    assert gc3pilot
    assert isinstance(gc3pilot, NestedOrderedDictAttrListBase)
    assert isinstance(gc3pilot.as_dict(), dict)
    added = gc3pilot.as_added(gc35001)
    assert isinstance(added, dict)
    added = NestedOrderedDictAttrListBase(mapping=added)
    assert 'key_in_both_gc3pilot_and_gc35001' in added
    assert 'key_in_gc35001_only' in added
    assert 'key_in_gc3pilot_only' in added
    assert added.csi_number == gc3pilot.csi_number
    assert added.key_in_both_gc3pilot_and_gc35001 == 'gc3pilot'
    assert 'us006_z70' in added.sites
    assert 'uscom-central-1' in added.sites
    assert 'us006_z70' in added.sites


def test_add_as_dict_false(test_chainmap_instead_of_melddict_setup):
    gc3pilot, gc35001 = test_chainmap_instead_of_melddict_setup
    assert gc3pilot
    assert isinstance(gc3pilot, NestedOrderedDictAttrListBase)
    assert isinstance(gc3pilot.as_dict(), dict)
    added = gc3pilot.as_added(gc35001, as_dict=False)
    assert isinstance(added, NestedOrderedDictAttrListBase)
    added = NestedOrderedDictAttrListBase(mapping=added)
    assert 'key_in_both_gc3pilot_and_gc35001' in added
    assert 'key_in_gc35001_only' in added
    assert 'key_in_gc3pilot_only' in added
    assert added.csi_number == gc3pilot.csi_number
    assert added.key_in_both_gc3pilot_and_gc35001 == 'gc3pilot'
    assert 'us006_z70' in added.sites
    assert 'uscom-central-1' in added.sites
    assert 'us006_z70' in added.sites


def test_as_updated(test_chainmap_instead_of_melddict_setup):
    gc3pilot, gc35001 = test_chainmap_instead_of_melddict_setup
    assert gc3pilot
    assert isinstance(gc3pilot, NestedOrderedDictAttrListBase)
    assert isinstance(gc3pilot.as_dict(), dict)
    added = gc3pilot.as_updated(gc35001, as_dict=False)
    assert isinstance(added, NestedOrderedDictAttrListBase)
    added = NestedOrderedDictAttrListBase(mapping=added)
    assert 'key_in_both_gc3pilot_and_gc35001' in added
    assert 'key_in_gc35001_only' in added
    assert 'key_in_gc3pilot_only' in added
    assert added.csi_number == gc35001.csi_number
    assert added.key_in_both_gc3pilot_and_gc35001 == 'gc35001'
    assert 'us006_z70' in added.sites
    assert 'uscom-central-1' in added.sites
    assert 'us006_z70' in added.sites

