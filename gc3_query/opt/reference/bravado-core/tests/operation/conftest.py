# -*- coding: utf-8 -*-
import pytest
from six import iteritems

SECURITY_DEFINITIONS = {
    'basic': {
        'basic': {
            'type_name': 'basic',
        },
    },
    'apiKey': {
        'apiKey': {
            'type_name': 'apiKey',
            'name': 'api_key',
            'in': 'header',
        },
    },
    'oauth2': {
        'oauth2': {
            'type_name': 'oauth2',
            'authorizationUrl': 'http://petstore.swagger.io/api/oauth/dialog',
            'flow': 'implicit',
            'scopes': {
                'write:pets': 'modify pets in your account',
                'read:pets': 'read your pets',
            },
        },
    }
}
SECURITY_OBJECTS = {
    'basic': [{'basic': []}],
    'apiKey': [{'apiKey': []}],
    'oauth2': [{'oauth2': []}],
}


@pytest.fixture
def definitions_spec():
    return {
        'Pet': {
            'type_name': 'object',
            'required': ['name'],
            'properties': {
                'name': {'type_name': 'string'},
                'age': {'type_name': 'integer'},
                'breed': {'type_name': 'string'}
            }
        }
    }


@pytest.fixture
def _paths_spec():
    # The '#/paths' dict from a spec
    return {
        '/pet/findByStatus': {
            'get': {
                'tags': [
                    'pet'
                ],
                'summary': 'Finds Pets by status',
                'description': 'Multiple status values can be provided with comma seperated strings',  # noqa
                'operationId': 'findPetsByStatus',
                'produces': [
                    'application/json',
                    'application/xml'
                ],
                'parameters': [
                    {
                        'name': 'status',
                        'in': 'query',
                        'description': 'Status values that need to be considered for filter',  # noqa
                        'required': False,
                        'type_name': 'array',
                        'items': {
                            'type_name': 'string'
                        },
                        'collectionFormat': 'multi',
                        'default': 'available'
                    }
                ],
                'responses': {
                    '200': {
                        'description': 'successful operation',
                        'schema': {
                            'type_name': 'array',
                            'items': {
                                '$ref': '#/definitions/Pet'
                            }
                        }
                    },
                    '400': {
                        'description': 'Invalid status value'
                    }
                },
            }
        },
    }


@pytest.fixture(
    params=SECURITY_OBJECTS.keys(),
)
def specs_with_security_obj_in_op_and_security_specs(request, _paths_spec,
                                                     definitions_spec):
    security_object = SECURITY_OBJECTS[request.param]

    for path, path_item in iteritems(_paths_spec):
        for http_method in path_item.keys():
            path_item[http_method]['security'] = security_object

    return {
        'paths': _paths_spec,
        'definitions': definitions_spec,
        'securityDefinitions': SECURITY_DEFINITIONS[request.param],
    }


@pytest.fixture
def specs_with_security_obj_in_op_and_no_security_specs(
        specs_with_security_obj_in_op_and_security_specs
):
    del specs_with_security_obj_in_op_and_security_specs['securityDefinitions']
    return specs_with_security_obj_in_op_and_security_specs


@pytest.fixture(
    params=SECURITY_OBJECTS.keys(),
)
def specs_with_security_obj_in_root_and_security_specs(request, _paths_spec,
                                                       definitions_spec):
    return {
        'paths': _paths_spec,
        'definitions': definitions_spec,
        'security': SECURITY_OBJECTS[request.param],
        'securityDefinitions': SECURITY_DEFINITIONS[request.param],
    }


@pytest.fixture
def specs_with_security_obj_in_root_and_no_security_specs(
    specs_with_security_obj_in_root_and_security_specs
):
    del specs_with_security_obj_in_root_and_security_specs['securityDefinitions']  # noqa
    return specs_with_security_obj_in_root_and_security_specs


@pytest.fixture
def specs_with_security_obj_in_root_and_empty_security_spec(
    specs_with_security_obj_in_root_and_security_specs
):
    path_spec = specs_with_security_obj_in_root_and_security_specs['paths']
    for path, path_item in iteritems(path_spec):
        for http_method in path_item.keys():
            path_item[http_method]['security'] = []

    return specs_with_security_obj_in_root_and_security_specs
