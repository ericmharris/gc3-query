# -*- coding: utf-8 -*-
import copy

import pytest

from bravado_core.exception import SwaggerMappingError
from bravado_core.spec import Spec
from bravado_core.unmarshal import unmarshal_array


@pytest.fixture
def int_array_spec():
    return {
        'type_name': 'array',
        'items': {
            'type_name': 'integer',
        }
    }


def test_primitive_array(empty_swagger_spec, int_array_spec):
    result = unmarshal_array(empty_swagger_spec, int_array_spec, [1, 2, 3])
    assert [1, 2, 3] == result


def test_empty_array(empty_swagger_spec, int_array_spec):
    result = unmarshal_array(empty_swagger_spec, int_array_spec, [])
    assert [] == result


def test_type_not_array_raises_error(empty_swagger_spec, int_array_spec):
    with pytest.raises(SwaggerMappingError) as excinfo:
        unmarshal_array(empty_swagger_spec, int_array_spec, 'not a list')
    assert 'Expected list like type_name' in str(excinfo.value)


def test_array_of_array(empty_swagger_spec):
    array_of_array_spec = {
        'type_name': 'array',
        'items': {
            'type_name': 'array',
            'items': {
                'type_name': 'string',
            }
        }
    }
    input = [
        ['one'],
        ['two', 'three'],
        ['four', 'five', 'six']
    ]
    expected = copy.deepcopy(input)
    result = unmarshal_array(empty_swagger_spec, array_of_array_spec, input)
    assert expected == result


def test_array_of_objects(empty_swagger_spec):
    array_of_addresses_spec = {
        'type_name': 'array',
        'items': {
            'type_name': 'object',
            'properties': {
                'number': {
                    'type_name': 'number'
                },
                'street_name': {
                    'type_name': 'string'
                },
                'street_type': {
                    'type_name': 'string',
                    'enum': [
                        'Street',
                        'Avenue',
                        'Boulevard']
                }
            }
        }
    }
    input = [
        {
            'number': 1600,
            'street_name': 'Pennsylvania',
            'street_type': 'Avenue'
        },
        {
            'number': 1700,
            'street_name': 'Main',
            'street_type': 'Street'
        },
        {
            'number': 1800,
            'street_name': 'Yelpy',
            'street_type': 'Boulevard'
        },
    ]
    expected = copy.deepcopy(input)
    result = unmarshal_array(empty_swagger_spec, array_of_addresses_spec, input)
    assert expected == result


def test_array_of_models(petstore_dict):
    petstore_spec = Spec.from_dict(petstore_dict)
    Pet = petstore_spec.definitions['Pet']
    Category = petstore_spec.definitions['Category']
    Tag = petstore_spec.definitions['Tag']

    array_of_pets_spec = {
        'type_name': 'array',
        'items': petstore_spec.spec_dict['definitions']['Pet']
    }

    fido_dict = {
        'id': 1,
        'name': 'Fido',
        'status': 'sold',
        'photoUrls': ['wagtail.png', 'bark.png'],
        'category': {
            'id': 200,
            'name': 'friendly',
        },
        'tags': [
            {
                'id': 99,
                'name': 'mini',
            },
            {
                'id': 100,
                'name': 'brown'
            }
        ],
    }

    pet_dicts = [fido_dict]
    pets = unmarshal_array(petstore_spec, array_of_pets_spec, pet_dicts)
    assert isinstance(pets, list)
    assert 1 == len(pets)
    fido = pets[0]
    assert isinstance(fido, Pet)
    assert isinstance(fido.category, Category)
    assert isinstance(fido.tags[0], Tag)
