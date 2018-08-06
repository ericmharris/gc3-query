import pytest
import toml
from pathlib import Path

from gc3_query.lib import *
from gc3_query.lib import BASE_DIR, gc3_cfg

from gc3_query.lib.gc3_config import GC3Config, IDMCredential
from gc3_query.lib.iaas_classic.iaas_requests_http_client import IaaSRequestsHTTPClient
from gc3_query.lib.iaas_classic import IaaSServiceBase, API_SPECS_DIR, IaaSRequestsHTTPClient
from gc3_query.lib.iaas_classic.instances import Instances
from gc3_query.lib.storage_adapters.mongodb import storage_adapter_init
from gc3_query.lib.iaas_classic.models import IaaSServiceModelDynamicDocument

TEST_BASE_DIR: Path = Path(__file__).parent
# config_dir = TEST_BASE_DIR.joinpath("config")
config_dir = BASE_DIR.joinpath("etc/config")


def test_setup():
    assert TEST_BASE_DIR.exists()
    assert config_dir.exists()
    assert API_SPECS_DIR.exists()


def test_init():
    model_base = IaaSServiceModelDynamicDocument()
    assert model_base.connection_config
    assert 'port' in model_base.connection_config





