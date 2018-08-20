# -*- coding: utf-8 -*-

"""
#@Filename : test_boolean_string
#@Date : [8/13/2018 7:29 PM]
#@Poject: gc3-query
#@AUTHOR : emharris

~~~~~~~~~~~~~~~~

<DESCR SHORT>

<DESCR>
"""

################################################################################
## Standard Library Imports

################################################################################
## Third-Party Imports


################################################################################
## Project Imports
from gc3_query.lib.iaas_classic.iaas_swagger_client import BRAVADO_CORE_CONFIG
from gc3_query.lib.open_api.swagger_formats.boolean_string import BooleanString

from gc3_query.lib import get_logging
_debug, _info, _warning, _error, _critical = get_logging(name=__name__)

from gc3_query import BASE_DIR

TEST_BASE_DIR: Path = Path(__file__).parent
# config_dir = TEST_BASE_DIR.joinpath("config")
config_dir = BASE_DIR.joinpath("etc/config")
output_dir = TEST_BASE_DIR.joinpath('output')

from gc3_query.lib.gc3_config import GC3Config
from gc3_query.lib.iaas_classic import API_SPECS_DIR
from gc3_query.lib.iaas_classic.sec_rules import SecRules
from gc3_query.lib.open_api.open_api_spec import OpenApiSpec



from bravado_core.spec import Spec
from bravado_core.response import unmarshal_response
from bravado_core.param import marshal_param










def test_setup():
    assert TEST_BASE_DIR.exists()
    assert API_SPECS_DIR.exists()
    if not config_dir.exists():
        config_dir.mkdir()
    if not output_dir.exists():
        output_dir.mkdir()



def test_boolean_string_class():
    bs_true = BooleanString(from_wire='true')
    assert bs_true.validate(bs_true.boolish)
    assert bs_true.as_boolean==True

    bs_false = BooleanString(from_wire='false')
    assert bs_false.validate(bs_false.boolish)
    assert bs_false.as_boolean==False


def test_swagger_format():
    idm_domain = 'gc30003'
    gc3_config = GC3Config(atoml_config_dir=config_dir)
    idm_cfg = gc3_config.idm.domains[idm_domain]
    secrules_service: str = 'SecRules'
    secrules_service_cfg = gc3_config.iaas_classic.services[secrules_service]
    sec_rules = SecRules(service_cfg=secrules_service_cfg, idm_cfg=idm_cfg, from_url=True)
    api_catalog_config = gc3_config.iaas_classic.open_api_spec_catalog
    sec_rules_service_cfg = gc3_config.iaas_classic.services[secrules_service]
    sec_rules_oapi_spec = OpenApiSpec(api_catalog_config=api_catalog_config, service_cfg=sec_rules_service_cfg, idm_cfg=idm_cfg)
    assert sec_rules_oapi_spec.name == secrules_service
    assert sec_rules_oapi_spec.spec_data['schemes'] == ['https']
    assert sec_rules_oapi_spec.title==secrules_service

    # Retrieve the swagger spec from the server and json.load() it
    # spec_dict = ...

    # Create cidr_format add it to the config dict
    # config = ...

    # Create a bravado_core.spec.Spec
    # swagger_spec = Spec.from_dict(spec_dict, config=config)
    spec_dict = sec_rules_oapi_spec.spec_dict
    config = BRAVADO_CORE_CONFIG
    assert 'formats' in config
    swagger_spec = Spec.from_dict(spec_dict=spec_dict, config=config)

    # Get the operation to invoke
    op = swagger_spec.get_op_for_request('GET', "/secrule/{container}/")

    # Get the Param that represents the cidr query parameter
    dst_is_ip_param = op.params.get('dst_is_ip')
    src_is_ip_param = op.params.get('src_is_ip')

    # Create a CIDR object - to_wire() will be called on this during marshalling
    boolean_string_object = BooleanString(from_wire='true')
    request_dict = {'params':{}}

    # Marshal the cidr_object into the request_dict.
    marshal_param(dst_is_ip_param, boolean_string_object, request_dict)

    # Lots of hand-wavey stuff here - use whatever http client you have to
    # send the request and receive a response
    response = sec_rules.http_client.send(request_dict)

    # Extract the list of cidrs
    cidrs = unmarshal_response(response)

    # Verify cidrs are CIDR objects and not strings
    for cidr in cidrs:
        assert type(cidr) == CIDR


