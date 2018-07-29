import pytest
import toml
from pathlib import Path

from gc3_query.lib import *

from gc3_query.lib.gc3_config import GC3Config

TEST_BASE_DIR: Path = Path(__file__).parent.joinpath("GC3Config")


def test_init():
    config_dir = TEST_BASE_DIR.joinpath("config")
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    assert 'gc30003' in gc3_config['idm_domains']
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'


def test_set_credential():
    config_dir = TEST_BASE_DIR.joinpath("config")
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    assert 'gc3test' in gc3_config['idm_domains']
    assert gc3_config.user.cloud_username == 'eric.harris@oracle.com'
    is_success = gc3_config.set_credential(idm_domain_name='gc3test', password='Welcome123' )
    assert is_success



