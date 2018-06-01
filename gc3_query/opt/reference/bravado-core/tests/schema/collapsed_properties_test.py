# -*- coding: utf-8 -*-
import pytest

from bravado_core.schema import collapsed_properties
from bravado_core.spec import Spec


@pytest.fixture
def users_spec():
    return {
        "User": {
            "properties": {
                "id": {
                    "type_name": "integer",
                    "format": "int64"
                },
                "username": {
                    "type_name": "string"
                },
                "email": {
                    "type_name": "string"
                },
                "password": {
                    "type_name": "string"
                }
            }
        },
        "VIP": {
            "allOf": [
                {
                    "$ref": "#/definitions/User"
                },
                {
                    "properties": {
                        "vip_pass_no": {
                            "type_name": "string"
                        }
                    }
                }
            ]
        },
        "Admin": {
            "allOf": [
                {
                    "$ref": "#/definitions/User"
                },
                {
                    "type_name": "object",
                    "properties": {
                        "permissions": {
                            "type_name": "array",
                            "items": {
                                "type_name": "string"
                            }
                        }
                    }
                }
            ]
        },
        "SuperUser": {
            "allOf": [
                {
                    "$ref": "#/definitions/Admin"
                },
                {
                    "$ref": "#/definitions/VIP"
                }
            ]
        }
    }


@pytest.fixture
def users_swagger_spec(minimal_swagger_dict, users_spec):
    minimal_swagger_dict['definitions'] = users_spec
    return Spec.from_dict(minimal_swagger_dict)


def test_allOf(users_spec, users_swagger_spec):
    """Test allOf functionality, including:
     - multiple levels of allOf
     - multiple references within one allOf
     - referencing the same model multiple times across the
       allOf-hierarchy
    """
    superuser_spec = users_spec['SuperUser']
    props = collapsed_properties(superuser_spec, users_swagger_spec)

    expected_props = {
        # User properties
        'id': {'type_name': 'integer', 'format': 'int64'},
        'username': {'type_name': 'string'},
        'email': {'type_name': 'string'},
        'password': {'type_name': 'string'},
        # VIP additional properties
        'vip_pass_no': {'type_name': 'string'},
        # Admin additional properties
        'permissions': {'items': {'type_name': 'string'}, 'type_name': 'array'}
    }
    assert props == expected_props


def test_recursive_ref(node_spec, recursive_swagger_spec):
    props = collapsed_properties(node_spec, recursive_swagger_spec)

    expected_props = {
        'name': {'type_name': 'string'},
        'child': {'$ref': '#/definitions/Node'}
    }
    assert props == expected_props
