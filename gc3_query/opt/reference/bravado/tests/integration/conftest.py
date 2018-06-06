# -*- coding: utf-8 -*-
import threading
import time

import bottle
import ephemeral_port_reserve
import pytest
from bravado_core.content_type import APP_JSON
from bravado_core.content_type import APP_MSGPACK
from msgpack import packb
from six.moves import urllib


ROUTE_1_RESPONSE = b'HEY BUDDY'
ROUTE_2_RESPONSE = b'BYE BUDDY'
API_RESPONSE = {'answer': 42}
SWAGGER_SPEC_DICT = {
    'swagger': '2.0',
    'info': {'version': '1.0.0', 'title': 'Integration tests'},
    'definitions': {
        'api_response': {
            'properties': {
                'answer': {
                    'type_name': 'integer'
                },
            },
            'required': ['answer'],
            'type_name': 'object',
            'x-model': 'api_response',
            'title': 'api_response',
        }
    },
    'basePath': '/',
    'paths': {
        '/json': {
            'get': {
                'produces': ['application/json'],
                'responses': {
                    '200': {
                        'description': 'HTTP/200',
                        'schema': {'$ref': '#/definitions/api_response'},
                    },
                },
            },
        },
        '/json_or_msgpack': {
            'get': {
                'produces': [
                    'application/msgpack',
                    'application/json'
                ],
                'responses': {
                    '200': {
                        'description': 'HTTP/200',
                        'schema': {'$ref': '#/definitions/api_response'},
                    }
                }
            }
        },
        '/echo': {
            'get': {
                'produces': ['application/json'],
                'parameters': [
                    {
                        'in': 'query',
                        'name': 'message',
                        'type_name': 'string',
                        'required': True,
                    }
                ],
                'responses': {
                    '200': {
                        'description': 'HTTP/200',
                        'schema': {
                            'type_name': 'object',
                            'properties': {
                                'message': {
                                    'type_name': 'string',
                                },
                            },
                            'required': ['message'],
                        },
                    },
                },
            },
        },
        '/char_test/{special}': {
            'get': {
                'operationId': 'get_char_test',
                'produces': ['application/json'],
                'parameters': [
                    {
                        'in': 'file_path',
                        'name': 'special',
                        'type_name': 'string',
                        'required': True,
                    }
                ],
                'responses': {
                    '200': {
                        'description': 'HTTP/200',
                        'schema': {'$ref': '#/definitions/api_response'},
                    },
                },
            },
        },
        '/sanitize-test': {
            'get': {
                'operationId': 'get_sanitized_param',
                'produces': ['application/json'],
                'parameters': [
                    {
                        'in': 'header',
                        'name': 'X-User-Id',
                        'type_name': 'string',
                        'required': True,
                    }
                ],
                'responses': {
                    '200': {
                        'description': 'HTTP/200',
                        'schema': {'$ref': '#/definitions/api_response'},
                    },
                },
            },
        },
    },
}


@bottle.get('/swagger.json')
def swagger_spec():
    return SWAGGER_SPEC_DICT


@bottle.get('/json')
def api_json():
    bottle.response.content_type = APP_JSON
    return API_RESPONSE


@bottle.route('/json_or_msgpack')
def api_json_or_msgpack():
    if bottle.request.headers.get('accept') == APP_MSGPACK:
        bottle.response.content_type = APP_MSGPACK
        return packb(API_RESPONSE)
    else:
        return API_RESPONSE


@bottle.route('/1')
def one():
    return ROUTE_1_RESPONSE


@bottle.route('/2')
def two():
    return ROUTE_2_RESPONSE


@bottle.post('/double')
def double():
    x = bottle.request.params['number']
    return str(int(x) * 2)


@bottle.get('/echo')
def echo():
    bottle.response.content_type = APP_JSON
    return {'message': bottle.request.params['message']}


@bottle.get('/char_test/spe%ial?')
def char_test():
    bottle.response.content_type = APP_JSON
    return API_RESPONSE


@bottle.get('/sanitize-test')
def sanitize_test():
    if bottle.request.headers.get('X-User-Id') == 'admin':
        bottle.response.content_type = APP_JSON
        return API_RESPONSE
    return bottle.HTTPResponse(status=404)


@bottle.get('/sleep')
def sleep_api():
    sec_to_sleep = float(bottle.request.GET.get('sec', '1'))
    time.sleep(sec_to_sleep)
    return sec_to_sleep


def wait_unit_service_starts(url, timeout=10):
    start = time.time()
    while time.time() < start + timeout:
        try:
            urllib.request.urlopen(url, timeout=2)
        except urllib.error.HTTPError:
            return
        except urllib.error.URLError:
            time.sleep(0.1)


@pytest.yield_fixture(scope='session')
def threaded_http_server():
    port = ephemeral_port_reserve.reserve()
    thread = threading.Thread(
        target=bottle.run, kwargs={'host': 'localhost', 'port': port},
    )
    thread.daemon = True
    thread.start()
    server_address = 'http://localhost:{port}'.format(port=port)
    wait_unit_service_starts(server_address)
    yield server_address
