# coding: utf-8

import os
import json
from pathlib import Path
from typing import Dict

import bravado
from bravado.client import SwaggerClient
# from bravado.requests_client import RequestsClient
from gc3_query.lib.bravado.requests_client import OCRequestsClient
from bravado.swagger_model import load_file
from secrets import opc_username, opc_password
from bravado_core.exception import MatchingResponseNotFound
from bravado.exception import HTTPBadRequest
from bravado.http_future import HttpFuture

from tinydb import TinyDB

from prettyprinter import pprint, pformat

## https://medium.com/@betz.mark/validate-json-models-with-swagger-and-bravado-5fad6b21a825
# Validate json models with swagger and bravado
from bravado_core.spec import Spec

idm_domain_name = 'gc30003'
idm_service_instance_id = '587626604'
iaas_rest_endpoint = r'https://compute.uscom-central-1.oraclecloud.com'
iaas_auth_endpoint = f'{iaas_rest_endpoint}/authenticate/'

print(f'iaas_rest_endpoint: {iaas_rest_endpoint}')
print(f'iaas_auth_endpoint: {iaas_auth_endpoint}\n')


### Username/pass setup
idm_domain_username = f'/Compute-{idm_domain_name}/{opc_username}'
idm_service_instance_username = f'/Compute-{idm_service_instance_id}/{opc_username}'
# username = traditional_iaas_username
username = idm_service_instance_username
# basic_auth_cred = _basic_auth_str(username, opc_password)

print(f'idm_domain_username: {idm_domain_username}')
print(f'idm_service_instance_username: {idm_service_instance_username}')
print(f'username: {username}')
# print(f'basic_auth_cred: {basic_auth_cred}')

### END Username/pass setup
json_data = {"user": username, "password": opc_password}
print(f'\njson_data: {json_data}')

#
# headers: Dict[str, str] = dict([('Content-Type', 'application/oracle-compute-v3+json'),
#                                 ('Accept', 'application/oracle-compute-v3+directory+json'), ])
# print(f'headers: {headers}')
#
# # In[6]:
#
#
# requests_client = OPCRequestsClient()
# requests_client.session.headers.update(headers)
#
# print(f"requests_client.session.headers before update: {requests_client.session.headers}\n")
# requests_client.session.headers.update(headers)
# print(f"requests_client.session.headers after update: {requests_client.session.headers}\n")
#
#
#
#
# response = requests_client.session.post(url=iaas_auth_endpoint, json=json_data)
#
# print(f'Response OK: {response.ok}, Status Code: {response.status_code}, URL: {response.url}')
# if response.ok and 'Set-Cookie' in response.headers:
#     print(f"Auth request succeess.\n")
#     ### The auth cookie is already placed in the session ... nothing else needs to be done.
#     print(f"\nSession Cookies: {requests_client.session.cookies}")
#     print(f"\nResponse Headers['Set-Cookie']: {response.headers['Set-Cookie']}")
#
# else:
#     print(f'Something failed! Response OK: {response.ok}, Status Code: {response.status_code}')
#
# # In[10]:
#
#
# print(f"requests_client.session.headers before update: {requests_client.session.headers}\n")
# cookie_header = {'Cookie': response.headers['Set-Cookie']}
# print(f"cookie_header: {cookie_header}\n")
# requests_client.session.headers.update(cookie_header)
# print(f"requests_client.session.headers after update: {requests_client.session.headers}\n")
#
# #
#
# # In[11]:
#
#
# cwd = os.getcwd()
# spec_file_path = Path().joinpath('open_api_definitions/iaas_instances.json').resolve()
# print(f'spec_file_path exists: {spec_file_path.exists()}, spec_file_path: {spec_file_path}')
#
# #### http://bravado.readthedocs.io/en/latest/advanced.html#loading-swagger-json-by-file-path
# ## needed for: client = SwaggerClient.from_url('file:///some/path/swagger.json')
# spec_file_uri = f"file:///{spec_file_path}"
# print(f'spec_file_uri: {spec_file_path}')
#
#
# # In[14]:
#
#
# spec_dict = load_file(spec_file_path)
# spec_dict['schemes']
# print(f"Original spec: spec_dict['schemes']: {spec_dict['schemes']}")
# spec_dict['schemes'] = ['https']
# print(f"Spec after scheme update: spec_dict['schemes']: {spec_dict['schemes']}")
#
# # In[17]:
#
#
# swagger_spec: Spec = Spec.from_dict(spec_dict=spec_dict,
#                               origin_url=iaas_rest_endpoint,
#                               http_client=requests_client,
#
#                               )
#
# # In[18]:
#
#
#
# print(f"swagger_spec.api_url: {swagger_spec.api_url}")
#
#
#

######
######
######
######
######
######

# "/instance/": {
#     "get": {
#         "tags": ["Instances"],
#         "summary": "Retrieve Names of Containers",
#         "description": "Retrieves the names of containers that contain objects that you can access. You can use this information to construct the multipart name of an object.<p><b>Required Role: </b>To complete this task, you must have the <code>Compute_Monitor</code> or <code>Compute_Operations</code> role. If this role isn't assigned to you or you're not sure, then ask your system administrator to ensure that the role is assigned to you in Oracle Cloud My Services. See <a target=\"_blank\" href=\"http://www.oracle.com/pls/topic/lookup?ctx=stcomputecs&id=MMOCS-GUID-54C2E747-7D5B-451C-A39C-77936178EBB6\">Modifying User Roles</a> in <em>Managing and Monitoring Oracle Cloud</em>.",
#         "operationId": "discoverRootInstance",
#         "responses": {
#             "200": {
#                 "headers": {
#                     "set-cookie": {
#                         "type": "string",
#                         "description": "The cookie value is returned if the session is extended"
#                     }
#                 },
#                 "description": "OK. See <a class=\"xref\" href=\"Status%20Codes.html\">Status Codes</a> for information about other possible HTTP status codes.",
#                 "schema": {
#                     "$ref": "#/definitions/Instance-discover-response"
#                 }
#             }
#         },
#         "consumes": ["application/oracle-compute-v3+json"],
#         "produces": ["application/oracle-compute-v3+directory+json"],
#         "parameters": [{
#             "name": "Cookie",
#             "in": "header",
#             "type": "string",
#             "description": "The Cookie: header must be included with every request to the service. It must be set to the value of the set-cookie header in the response received to the POST /authenticate/ call."
#         }]
#     }
# },
#
# "Instance-discover-response": {
#     "properties": {
#         "result": {
#             "items": {
#                 "type": "string"
#             },
#             "type": "array"
#         }
#     }
# },

# print("discoverRootInstance starting.")
# instances_resource = swagger_client.Instances
# try:
#     operation = instances_resource.discoverRootInstance()
#     url = operation_future.future.request.url
#     print(f"REST url: {url}")
#     operation_result, operation_response = operation.result()
# except HTTPBadRequest:
#     print("Request failed! ")
#     print(f"URL: {operation_future.future.request.url}")
#     raise
# operation_details = json.loads(operation_result)
# print("discoverRootInstance operation_details for {}:\n {}".format(url, pformat(operation_details)))
# # operation_details for https://compute.uscom-central-1.oraclecloud.com/instance/:
# # {'result': ['/Compute-587626604/']}
# print("discoverRootInstance finished.")


##  Authenticate and get header token
headers = dict([('Content-Type', 'application/oracle-compute-v3+json'),
                ('Accept', 'application/oracle-compute-v3+directory+json'),
                ])
requests_client = OCRequestsClient()
requests_client.session.headers.update(headers)

print(f"requests_client.session.headers before update: {requests_client.session.headers}\n")
requests_client.session.headers.update(headers)
print(f"requests_client.session.headers after update: {requests_client.session.headers}\n")

response = requests_client.session.post(url=iaas_auth_endpoint, json=json_data)
print(f'Response OK: {response.ok}, Status Code: {response.status_code}, URL: {response.url}')
if response.ok and 'Set-Cookie' in response.headers:
    print(f"Auth request succeess.\n")
    ### The auth cookie is already placed in the session ... nothing else needs to be done.
    print(f"\nSession Cookies: {requests_client.session.cookies}")
    print(f"\nResponse Headers['Set-Cookie']: {response.headers['Set-Cookie']}")
else:
    print(f'Something failed! Response OK: {response.ok}, Status Code: {response.status_code}')

print(f"requests_client.session.headers before update: {requests_client.session.headers}\n")
cookie_header = {'Cookie': response.headers['Set-Cookie']}
print(f"cookie_header: {cookie_header}\n")
requests_client.session.headers.update(cookie_header)
print(f"requests_client.session.headers after update: {requests_client.session.headers}\n")




## Update the swagger spec to use https
spec_file_path = Path().joinpath('open_api_definitions/iaas_instances.json').resolve()
spec_dict = load_file(spec_file_path)
spec_dict['schemes'] = ['https']

headers = dict([('Content-Type', 'application/oracle-compute-v3+json'),
                ('Accept', 'application/oracle-compute-v3+json'),
                ('Accept', 'application/oracle-compute-v3+directory+json'),
                ])
requests_client = OCRequestsClient()
requests_client.session.headers.update(headers)
requests_client.session.headers.update(cookie_header)
swagger_client = SwaggerClient.from_spec(spec_dict=spec_dict,
                                         origin_url=iaas_rest_endpoint,
                                         http_client=requests_client,
                                         # config={'also_return_response': True,
                                         #         'validate_responses': True,
                                         #         'validate_requests': True,
                                         #         'validate_swagger_spec': True})
                                         # config={'also_return_response': True,
                                         #         'validate_responses': False,
                                         #         'validate_requests': True,
                                         #         'validate_swagger_spec': True})
                                         config={'also_return_response': True,
                                                 'validate_responses': False,
                                                 'validate_requests': False,
                                                 'validate_swagger_spec': False})
instances_resource = swagger_client.Instances

operation_id = "discoverRootInstance"
print(f"Operation {operation_id} starting.")
try:
    operation_future = getattr(instances_resource, operation_id)()
    url = operation_future.future.request.url
    print(f"REST url for {operation_id}: {url}")
    operation_result, operation_response = operation_future.result()
except HTTPBadRequest:
    print("Request failed for {operation_id}! ")
    print(f"URL: {operation_future.future.request.url}")
    raise
operation_details = json.loads(operation_result)
print("\n{} operation_details:\nHTTP method: {}\nAPI url: {}:\n {}\n".format(operation_id, operation_future.operation.http_method, url, pformat(operation_details)))
print(f"Operation {operation_id} finished.\n")
# discoverRootInstance operation_details:
# API url: https://compute.uscom-central-1.oraclecloud.com/instance/:
#  {'result': ['/Compute-587626604/']}


# "/instance/{container}": {
#     "get": {
#         "tags": ["Instances"],
#         "summary": "Retrieve Names of all Instances and Subcontainers in a Container",
#         "description": "Retrieves the names of objects and subcontainers that you can access in the specified container.<p><b>Required Role: </b>To complete this task, you must have the <code>Compute_Operations</code> role. If this role isn't assigned to you or you're not sure, then ask your system administrator to ensure that the role is assigned to you in Oracle Cloud My Services. See <a target=\"_blank\" href=\"http://www.oracle.com/pls/topic/lookup?ctx=stcomputecs&id=MMOCS-GUID-54C2E747-7D5B-451C-A39C-77936178EBB6\">Modifying User Roles</a> in <em>Managing and Monitoring Oracle Cloud</em>.",
#         "operationId": "discoverInstance",
#         "responses": {
#             "200": {
#                 "headers": {
#                     "set-cookie": {
#                         "type": "string",
#                         "description": "The cookie value is returned if the session is extended"
#                     }
#                 },
#                 "description": "OK. See <a class=\"xref\" href=\"Status%20Codes.html\">Status Codes</a> for information about other possible HTTP status codes.",
#                 "schema": {
#                     "$ref": "#/definitions/Instance-discover-response"
#                 }
#             }
#         },
#         "consumes": ["application/oracle-compute-v3+json"],
#         "produces": ["application/oracle-compute-v3+directory+json"],
#         "parameters": [{
#             "name": "container",
#             "in": "path",
#             "description": "Specify <code>/Compute-<i>identityDomain</i>/<i>user</i>/</code> to retrieve the names of objects that you can access. Specify <code>/Compute-<i>identityDomain</i>/</code> to retrieve the names of containers that contain objects that you can access.",
#             "required": true,
#             "type": "string"
#         }, {
#             "name": "Cookie",
#             "in": "header",
#             "type": "string",
#             "description": "The Cookie: header must be included with every request to the service. It must be set to the value of the set-cookie header in the response received to the POST /authenticate/ call."
#         }]
#     }
# },


operation_id = "discoverInstance"
print(f"Operation {operation_id} starting.")
try:
    # API url: https://compute.uscom-central-1.oraclecloud.com/instance/Compute-587626604
    container = operation_details['result'][0].lstrip('/').rstrip('/')
    # # API url: https://compute.uscom-central-1.oraclecloud.com/instance/Compute-587626604/eric.harris@oracle.com
    # container = f"{container}/{opc_username}"
    # # API url: https://compute.uscom-central-1.oraclecloud.com/instance/Compute-587626604/eric.harris@oracle.com/
    container = f"{container}/{opc_username}/"
    print(f"container: {container}")
    operation_future = getattr(instances_resource, operation_id)(container=container)
    url = operation_future.future.request.url
    print(f"REST url for {operation_id}: {url}")
    operation_result, operation_response = operation_future.result()
except HTTPBadRequest:
    print("Request failed for {operation_id}! ")
    print(f"URL: {operation_future.future.request.url}")
    raise
operation_details = json.loads(operation_result)
print("\n{} operation_details:\nHTTP method: {}\nAPI url: {}:\n {}\n".format(operation_id, operation_future.operation.http_method, url, pformat(operation_details)))
print(f"Operation {operation_id} finished.\n")
####
#### Specify /Compute-identityDomain/user/ to retrieve the names of objects that you can access.
# Operation discoverInstance starting.
# container: Compute-587626604/eric.harris@oracle.com
# REST url for discoverInstance: https://compute.uscom-central-1.oraclecloud.com/instance/Compute-587626604/eric.harris@oracle.com
#
# discoverInstance operation_details:
# HTTP method: get
# API url: https://compute.uscom-central-1.oraclecloud.com/instance/Compute-587626604/eric.harris@oracle.com:
#  {
#     'result': [
#         '/Compute-587626604/eric.harris@oracle.com/GC3NAAC-CDMT-LWS1/',
#         '/Compute-587626604/eric.harris@oracle.com/GC3NAAC-CDMT-PSFTHR92/',
#         '/Compute-587626604/eric.harris@oracle.com/dbaas/',
#         '/Compute-587626604/eric.harris@oracle.com/paas/'
#     ]
# }
####
#### Specify /Compute-identityDomain/ to retrieve the names of containers that contain objects that you can access.
# Operation discoverInstance starting.
# container: Compute-587626604
# REST url for discoverInstance: https://compute.uscom-central-1.oraclecloud.com/instance/Compute-587626604
#
# discoverInstance operation_details:
# API url: https://compute.uscom-central-1.oraclecloud.com/instance/Compute-587626604:
#  {
#     'result': [
#         '/Compute-587626604/dhiru.vallabhbhai@oracle.com/',
#         '/Compute-587626604/eric.harris@oracle.com/',
#         '/Compute-587626604/mayurnath.gokare@oracle.com/',
#         '/Compute-587626604/ramesh.dadhania@oracle.com/',
#         '/Compute-587626604/seetharaman.nandyal@oracle.com/',
#         '/Compute-587626604/siva.subramani@oracle.com/'
#     ]
# }


# "/instance/{container}/": {
#     "get": {
#         "tags": ["Instances"],
#         "summary": "Retrieve Details of all Instances in a Container",
#         "description": "Retrieves details of the instances that are in the specified container and match the specified query criteria. If you don't specify any query criteria, then details of all the instances in the container are displayed. To filter the search results, you can pass one or more of the following query parameters, by appending them to the URI in the following syntax:<p><code>?parameter1=value1&ampparameter2=value2&ampparameterN=valueN</code><p><b>Required Role: </b>To complete this task, you must have the <code>Compute_Monitor</code> or <code>Compute_Operations</code> role. If this role isn't assigned to you or you're not sure, then ask your system administrator to ensure that the role is assigned to you in Oracle Cloud My Services. See <a target=\"_blank\" href=\"http://www.oracle.com/pls/topic/lookup?ctx=stcomputecs&id=MMOCS-GUID-54C2E747-7D5B-451C-A39C-77936178EBB6\">Modifying User Roles</a> in <em>Managing and Monitoring Oracle Cloud</em>.",
#         "operationId": "listInstance",
#         "responses": {
#             "200": {
#                 "headers": {
#                     "set-cookie": {
#                         "type": "string",
#                         "description": "The cookie value is returned if the session is extended"
#                     }
#                 },
#                 "description": "OK. See <a class=\"xref\" href=\"Status%20Codes.html\">Status Codes</a> for information about other possible HTTP status codes.",
#                 "schema": {
#                     "$ref": "#/definitions/Instance-list-response"
#                 }
#             }
#         },
#         "consumes": ["application/oracle-compute-v3+json"],
#         "produces": ["application/oracle-compute-v3+json"],
#         "parameters": [{
#             "name": "container",
#             "in": "path",
#             "description": "<code>/Compute-<em>identity_domain</em>/<em>user</em></code> or <p><code>/Compute-<em>identity_domain</em></code>",
#             "required": true,
#             "type": "string"
#         }, {
#             "name": "availability_domain",
#             "in": "query",
#             "description": "The availability domain the instance is in",
#             "required": false,
#             "type": "string"
#         }, {
#             "name": "tags",
#             "in": "query",
#             "description": "Strings used to tag the instance. When you specify tags, only instances tagged with the specified value are displayed.",
#             "required": false,
#             "type": "array",
#             "items": {
#                 "type": "string"
#             }
#         }, {
#             "name": "Cookie",
#             "in": "header",
#             "type": "string",
#             "description": "The Cookie: header must be included with every request to the service. It must be set to the value of the set-cookie header in the response received to the POST /authenticate/ call."
#         }]
#     }
# },
#
# "Instance-list-response": {
#     "properties": {
#         "result": {
#             "items": {
#                 "$ref": "#/definitions/Instance-response"
#             },
#             "type": "array"
#         }
#     }
# },
#
# "Instance-response": {
#     "properties": {
#         "account": {
#             "type": "string",
#             "description": "Shows the default account for your identity domain."
#         },
#         "attributes": {
#             "additionalProperties": {
#                 "type": "object"
#             },
#             "type": "object",
#             "description": "A dictionary of attributes to be made available to the instance. A value with the key \"userdata\" will be made available in an EC2-compatible manner."
#         },
#         "availability_domain": {
#             "type": "string",
#             "description": "The availability domain the instance is in"
#         },
#         "boot_order": {
#             "items": {
#                 "type": "integer"
#             },
#             "type": "array",
#             "description": "Boot order list."
#         },
#         "desired_state": {
#             "type": "string",
#             "description": "Desired state for the instance. The value can be <code>shutdown</code> or <code>running</code> to shutdown an instance or to restart a previously shutdown instance respectively."
#         },
#         "disk_attach": {
#             "type": "string",
#             "description": "A label assigned by the user to identify disks."
#         },
#         "domain": {
#             "type": "string",
#             "description": "The default domain to use for the hostname and for DNS lookups."
#         },
#         "entry": {
#             "type": "integer",
#             "description": "Optional imagelistentry number (default will be used if not specified)."
#         },
#         "error_reason": {
#             "type": "string",
#             "description": "The reason for the instance going to error state, if available."
#         },
#         "fingerprint": {
#             "type": "string",
#             "description": "SSH server fingerprint presented by the instance."
#         },
#         "hostname": {
#             "type": "string",
#             "description": "The hostname for this instance."
#         },
#         "hypervisor": {
#             "additionalProperties": {
#                 "type": "object"
#             },
#             "type": "object",
#             "description": "A dictionary of hypervisor-specific attributes."
#         },
#         "image_format": {
#             "type": "string",
#             "description": "The format of the image."
#         },
#         "imagelist": {
#             "type": "string",
#             "description": "Name of imagelist to be launched."
#         },
#         "ip": {
#             "type": "string",
#             "description": "IP address of the instance."
#         },
#         "label": {
#             "type": "string",
#             "description": "A label assigned by the user, specifically for defining inter-instance relationships."
#         },
#         "name": {
#             "type": "string",
#             "description": "Multipart name of the instance."
#         },
#         "networking": {
#             "additionalProperties": {
#                 "type": "object"
#             },
#             "type": "object",
#             "description": "Mapping of <device name> to network specifiers for virtual NICs to be attached to this instance."
#         },
#         "placement_requirements": {
#             "items": {
#                 "type": "string"
#             },
#             "type": "array",
#             "description": "A list of strings specifying arbitrary tags on nodes to be matched on placement."
#         },
#         "platform": {
#             "type": "string",
#             "description": "The OS platform for the instance."
#         },
#         "priority": {
#             "type": "string",
#             "description": "The priority at which this instance will be run."
#         },
#         "quota": {
#             "type": "string",
#             "description": "Not used"
#         },
#         "relationships": {
#             "items": {
#                 "additionalProperties": {
#                     "type": "object"
#                 },
#                 "type": "object"
#             },
#             "type": "array",
#             "description": "A list of relationship specifications to be satisfied on this instance's placement"
#         },
#         "resolvers": {
#             "items": {
#                 "type": "string"
#             },
#             "type": "array",
#             "description": "Resolvers to use instead of the default resolvers."
#         },
#         "reverse_dns": {
#             "type": "boolean",
#             "description": "Add PTR records for the hostname."
#         },
#         "shape": {
#             "type": "string",
#             "description": "A shape is a resource profile that specifies the number of CPU threads and the amount of memory (in MB) to be allocated to an instance."
#         },
#         "sshkeys": {
#             "items": {
#                 "type": "string"
#             },
#             "type": "array",
#             "description": "SSH keys that will be exposed to the instance."
#         },
#         "start_time": {
#             "type": "string",
#             "description": "Start time of the instance."
#         },
#         "state": {
#             "type": "string",
#             "description": "State of the instance."
#         },
#         "storage_attachments": {
#             "items": {
#                 "type": "string"
#             },
#             "type": "array",
#             "description": "List of dictionaries containing storage attachment Information."
#         },
#         "tags": {
#             "items": {
#                 "type": "string"
#             },
#             "type": "array",
#             "description": "Comma-separated list of strings used to tag the instance."
#         },
#         "uri": {
#             "type": "string",
#             "description": "Uniform Resource Identifier"
#         },
#         "vcable_id": {
#             "type": "string",
#             "description": "vCable for this instance."
#         },
#         "vnc": {
#             "type": "string",
#             "description": "IP address and port of the VNC console for the instance."
#         }
#     }
# },




operation_id = "listInstance"
print(f"Operation {operation_id} starting.")
try:
    # container = operation_details['result'][0].lstrip('/').rstrip('/')
    # container = 'Compute-587626604/eric.harris@oracle.com'
    container = 'Compute-587626604/eric.harris@oracle.com/GC3NAAC-CDMT-LWS1'
    print(f"container: {container}")
    operation_future = getattr(instances_resource, operation_id)(container=container)
    url = operation_future.future.request.url
    print(f"REST url for {operation_id}: {url}")
    operation_result, operation_response = operation_future.result()
except HTTPBadRequest:
    print("Request failed for {operation_id}! ")
    print(f"URL: {operation_future.future.request.url}")
    raise
operation_details = json.loads(operation_result)
print("\n{} operation_details:\nHTTP method: {}\nAPI url: {}:\n {}\n".format(operation_id, operation_future.operation.http_method, url, pformat(operation_details)))
print(f"Operation {operation_id} finished.")
# Operation listInstance starting.
# container: Compute-587626604/eric.harris@oracle.com
# REST url for listInstance: https://compute.uscom-central-1.oraclecloud.com/instance/Compute-587626604/eric.harris@oracle.com/
#
# listInstance operation_details:
# API url: https://compute.uscom-central-1.oraclecloud.com/instance/Compute-587626604/eric.harris@oracle.com/:
#  {
#     'result': [
#         '/Compute-587626604/eric.harris@oracle.com/GC3NAAC-CDMT-LWS1/',
#         '/Compute-587626604/eric.harris@oracle.com/GC3NAAC-CDMT-PSFTHR92/',
#         '/Compute-587626604/eric.harris@oracle.com/dbaas/',
#         '/Compute-587626604/eric.harris@oracle.com/paas/'
#     ]
# }
#
# Operation listInstance finished.

# "/instance/{name}": {
#     "put": {
#         "tags": ["Instances"],
#  ...
#     "get": {
#         "tags": ["Instances"],
#         "summary": "Retrieve Details of an Instance",
#         "description": "Retrieves details of the specified instance.<p><b>Required Role: </b>To complete this task, you must have the <code>Compute_Monitor</code> or <code>Compute_Operations</code> role. If this role isn't assigned to you or you're not sure, then ask your system administrator to ensure that the role is assigned to you in Oracle Cloud My Services. See <a target=\"_blank\" href=\"http://www.oracle.com/pls/topic/lookup?ctx=stcomputecs&id=MMOCS-GUID-54C2E747-7D5B-451C-A39C-77936178EBB6\">Modifying User Roles</a> in <em>Managing and Monitoring Oracle Cloud</em>.",
#         "operationId": "getInstance",
#         "responses": {
#             "200": {
#                 "headers": {
#                     "set-cookie": {
#                         "type": "string",
#                         "description": "The cookie value is returned if the session is extended"
#                     }
#                 },
#                 "description": "OK. See <a class=\"xref\" href=\"Status%20Codes.html\">Status Codes</a> for information about other possible HTTP status codes.",
#                 "schema": {
#                     "$ref": "#/definitions/Instance-response"
#                 }
#             }
#         },
#         "consumes": ["application/oracle-compute-v3+json"],
#         "produces": ["application/oracle-compute-v3+json"],
#         "parameters": [{
#             "name": "name",
#             "in": "path",
#             "description": "<p>Multipart name of the object.",
#             "required": true,
#             "type": "string"
#         }, {
#             "name": "Cookie",
#             "in": "header",
#             "type": "string",
#             "description": "The Cookie: header must be included with every request to the service. It must be set to the value of the set-cookie header in the response received to the POST /authenticate/ call."
#         }]
#     }
# }
# },

# headers = dict([('Content-Type', 'application/oracle-compute-v3+json'),
#                 ('Accept', 'application/oracle-compute-v3+directory+json, application/oracle-compute-v3+json, json')])
# API url: https://compute.uscom-central-1.oraclecloud.com/instance/Compute-587626604/eric.harris@oracle.com/GC3NAAC-CDMT-LWS1:
#  {
#     'result': [
#         '/Compute-587626604/eric.harris@oracle.com/GC3NAAC-CDMT-LWS1/'
#         'c17bb7ea-724b-4e51-ab72-1bd8714f07b7'
#     ]
# }

# headers = dict([('Content-Type', 'application/oracle-compute-v3+json'),
#                 ('Accept', 'application/oracle-compute-v3+json, application/oracle-compute-v3+directory+json, json')])
# REST url for getInstance: https://compute.uscom-central-1.oraclecloud.com/instance/Compute-587626604/eric.harris@oracle.com/GC3NAAC-CDMT-LWS1
# Accept Header=[application/oracle-compute-v3+json, application/oracle-compute-v3+directory+json, json], Content-Type Header=[application/oracle-compute-v3+json]
# getInstance operation_details:
# HTTP method: get
# API url: https://compute.uscom-central-1.oraclecloud.com/instance/Compute-587626604/eric.harris@oracle.com/GC3NAAC-CDMT-LWS1:
#  {
#     'result': [
#         '/Compute-587626604/eric.harris@oracle.com/GC3NAAC-CDMT-LWS1/'
#         'c17bb7ea-724b-4e51-ab72-1bd8714f07b7'
#     ]
# }


headers = dict([('Content-Type', 'application/oracle-compute-v3+json'),
                ('Accept', 'application/oracle-compute-v3+json, json, text/html')])


requests_client = OCRequestsClient()
requests_client.session.headers.update(headers)
requests_client.session.headers.update(cookie_header)
swagger_client = SwaggerClient.from_spec(spec_dict=spec_dict,
                                         origin_url=iaas_rest_endpoint,
                                         http_client=requests_client,
                                         # config={'also_return_response': True,
                                         #         'validate_responses': True,
                                         #         'validate_requests': True,
                                         #         'validate_swagger_spec': True})
                                         # config={'also_return_response': True,
                                         #         'validate_responses': False,
                                         #         'validate_requests': True,
                                         #         'validate_swagger_spec': True})
                                         config={'also_return_response': True,
                                                 'validate_responses': False,
                                                 'validate_requests': False,
                                                 'validate_swagger_spec': False})
instances_resource = swagger_client.Instances

operation_id = "getInstance"
print(f"\nOperation {operation_id} starting.")
try:
    # name = operation_details['result'][0].lstrip('/').rstrip('/')

    # name = 'Compute-587626604/eric.harris@oracle.com/GC3NAAC-CDMT-LWS1/c17bb7ea-724b-4e51-ab72-1bd8714f07b7'
    # 'result': [
    # ]

    # name = 'Compute-587626604/eric.harris@oracle.com/GC3NAAC-CDMT-LWS1'
    # 'result': [
    #     '/Compute-587626604/eric.harris@oracle.com/GC3NAAC-CDMT-LWS1/'
    #     'c17bb7ea-724b-4e51-ab72-1bd8714f07b7'
    # ]

    # name = 'Compute-587626604/eric.harris@oracle.com/GC3NAAC-CDMT-LWS1/'
    # 'result': [
    #     '/Compute-587626604/eric.harris@oracle.com/GC3NAAC-CDMT-LWS1/'
    #     'c17bb7ea-724b-4e51-ab72-1bd8714f07b7'
    # ]

    # name = 'Compute-gc30003/eric.harris@oracle.com/GC3NAAC-CDMT-LWS1'
    # {'result': []}


    # name = 'Compute-587626604/eric.harris@oracle.com/GC3NAAC-CDMT-LWS1'
    #  This 404'ed because the name is actually
    #  Compute-587626604/eric.harris@oracle.com/GC3NAAC-CDMT-LWS1/c17bb7ea-724b-4e51-ab72-1bd8714f07b7
    #   instead of
    #  Compute-587626604/eric.harris@oracle.com/GC3NAAC-CDMT-LWS1
    name = 'Compute-587626604/eric.harris@oracle.com/GC3NAAC-CDMT-LWS1/c17bb7ea-724b-4e51-ab72-1bd8714f07b7'
    print(f"name: {name}")
    operation_future: HttpFuture = getattr(instances_resource, operation_id)(name=name)
    url = operation_future.future.request.url
    print(f"REST url for {operation_id}: {url}")
    print(f"Accept Header=[{operation_future.future.session.headers['Accept']}], Content-Type Header=[{operation_future.future.session.headers['Content-Type']}]")
    operation_result, operation_response = operation_future.result()
except bravado.exception.HTTPBadRequest:
    print("Request failed for {operation_id}! ")
    print(f"URL: {operation_future.future.request.url}")
    raise
# except bravado.exception.HTTPNotFound:
#     print("Request failed for {operation_id}! ")
#     print(f"URL: {operation_future.future.request.url}")
#     raise
operation_details = json.loads(operation_result)
print("\n{} operation_details:\nHTTP method: {}\nAPI url: {}:\n {}\n".format(operation_id, operation_future.operation.http_method, url, pformat(operation_details)))
print(f"Operation {operation_id} finished.")
# Operation getInstance starting.
# name: Compute-587626604/eric.harris@oracle.com/GC3NAAC-CDMT-LWS1
# REST url for getInstance: https://compute.uscom-central-1.oraclecloud.com/instance/Compute-587626604/eric.harris@oracle.com/GC3NAAC-CDMT-LWS1
#
# getInstance operation_details:
# API url: https://compute.uscom-central-1.oraclecloud.com/instance/Compute-587626604/eric.harris@oracle.com/GC3NAAC-CDMT-LWS1:
#  {
#     'result': [
#         '/Compute-587626604/eric.harris@oracle.com/GC3NAAC-CDMT-LWS1/'
#         'c17bb7ea-724b-4e51-ab72-1bd8714f07b7'
#     ]
# }
#
# Operation getInstance finished.


######
######
######
######
######
######


print('done.')

