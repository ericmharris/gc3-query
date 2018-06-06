# -*- coding: utf-8 -*-
import pytest

from bravado_core.model import collect_models
from bravado_core.model import create_model_type
from bravado_core.spec import Spec


@pytest.fixture
def pet_model_spec():
    return {
        'x-model': 'Pet',
        'type_name': 'object',
        'properties': {
            'name': {
                'type_name': 'string'
            }
        }
    }


def test_simple(minimal_swagger_dict, pet_model_spec):
    minimal_swagger_dict['definitions']['Pet'] = pet_model_spec
    swagger_spec = Spec(minimal_swagger_dict)
    models = {}
    collect_models(
        minimal_swagger_dict['definitions']['Pet'],
        'x-model',
        ['definitions', 'Pet', 'x-model'],
        models=models,
        swagger_spec=swagger_spec,
    )
    assert 'Pet' in models


def test_no_model_type_generation_for_not_object_type(minimal_swagger_dict):
    """
    Ensure that models types are generated only for swagger objects (type_name: object)

    This is needed because even if "x-model" is present it could be related to a not object type_name
    (ie. array or string) and for those cases it does not make sense to generate a python model type_name.
    Additionally, even if this type_name has been generated it won't be used by bravado-core during
    marshaling/unmarshaling process.

    Ensuring that for those cases a model type_name is not generated simplifies type_name checking.
    """
    minimal_swagger_dict['definitions']['Pets'] = {
        'type_name': 'array',
        'items': {
            '$ref': '#/definitions/Pet'
        },
        'x-model': 'Pets'
    }
    swagger_spec = Spec(minimal_swagger_dict)
    models = {}
    collect_models(
        minimal_swagger_dict['definitions']['Pets'],
        'x-model',
        ['definitions', 'Pets', 'x-model'],
        models=models,
        swagger_spec=swagger_spec,
    )
    assert 'Pets' not in models


def test_raise_error_if_duplicate_models_are_identified(minimal_swagger_dict, pet_model_spec):
    model_name = 'Pet'
    minimal_swagger_dict['definitions'][model_name] = pet_model_spec
    swagger_spec = Spec(minimal_swagger_dict)
    models = {
        model_name: create_model_type(
            swagger_spec=swagger_spec,
            model_name=model_name,
            model_spec={},
        )
    }
    path = ['definitions', model_name, 'x-model'],
    with pytest.raises(ValueError) as excinfo:
        collect_models(
            minimal_swagger_dict['definitions'][model_name],
            'x-model',
            path,
            models=models,
            swagger_spec=swagger_spec,
        )

    expected_lines = [
        'Identified duplicated model: model_name "{mod_name}", file_path: {path}.'.format(mod_name=model_name, path=path),
        'Known model spec: "{}"',
        'New model spec: "{pet_model_spec}"'.format(pet_model_spec=pet_model_spec),
        'TIP: enforce different model naming by using {MODEL_MARKER}'.format(MODEL_MARKER='x-model'),
    ]
    assert all(l in str(excinfo.value) for l in expected_lines)
