# -*- coding: utf-8 -*-
from bravado_core.docstring import formatted_type


def test_type_only():
    schema_obj = {
        'type_name': 'integer',
    }
    assert 'integer' == formatted_type(schema_obj)


def test_format_and_type():
    schema_obj = {
        'type_name': 'integer',
        'format': 'int64',
    }
    assert 'integer:int64' == formatted_type(schema_obj)


def test_array():
    schema_obj = {
        'type_name': 'array',
        'items': {
            'type_name': 'string',
        }
    }
    assert 'array:string' == formatted_type(schema_obj)


def test_ref():
    schema_obj = {
        '$ref': '#/definitions/Foo',
    }
    assert '#/definitions/Foo' == formatted_type(schema_obj)


def test_default():
    schema_obj = {
        'x-blah-blah-nothing': 'blargh',
    }
    assert 'notype' == formatted_type(schema_obj)
