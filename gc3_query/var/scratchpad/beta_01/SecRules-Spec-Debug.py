
# coding: utf-8

# ## Oracle Cloud Instance POC
# 

# [https://porter.io/github.com/Yelp/bravado]
# 
# ## Example with Basic Authentication
# 
# 
# ```
# from bravado.requests_client import RequestsClient
# from bravado.client import SwaggerClient
# 
# http_client = RequestsClient()
# http_client.set_basic_auth(
#     'api.yourhost.com',
#     'username', 'password'
# )
# client = SwaggerClient.from_url(
#     'http://petstore.swagger.io/v2/swagger.json',
#     http_client=http_client,
# )
# pet = client.pet.getPetById(petId=42).response().result
# 
# ```
# 
# ## IaaS Compute Authentication
# 
# API calls to Compute Classic require basic authentication (user name and password). **You can pass your username and password with every API call or you can pass a valid authentication token**. To get a valid authentication token, send an HTTP request to authenticate the user credentials. If the authentication request succeeds, the server returns a cookie containing an authentication token that is valid for 30 minutes. The client making the API calls must include this cookie in the API calls.
# 
# To request for an authentication token and store the authentication token in an environment variable:
# 

# In[2]:



import json
from pathlib import Path
from typing import List, Any, Dict

from bravado.client import SwaggerClient
from bravado.requests_client import RequestsClient
from bravado_core.spec import Spec

# In[3]:
# In[3]:
DictStrAny = Dict[str, Any]

# In[4]:


# from secrets import opc_username, opc_password
import keyring

opc_username = "eric.harris@oracle.com"
opc_password = keyring.get_password(service_name="gc3@gc30003", username="eric.harris@oracle.com")
print(f"opc_username={opc_username}, opc_password={opc_password}")
rest_endpoint = "https://dbaas.oraclecloud.com/"


# In[5]:


################################################################################
## Standard Library Imports

################################################################################
## Third-Party Imports
import dateutil
import pytz
# from bson.int64 import long
from dataclasses import dataclass
from bravado_core.formatter import SwaggerFormat
from bravado_core.exception import SwaggerValidationError


# In[6]:


proxies = {
  'http': 'http://www-proxy-ash7.us.oracle.com:80',
  'https': 'https://www-proxy-ash7.us.oracle.com:80',
}
ORACLE_VPN_CONNECTED=False
ASDF='ASDF'


# ## Models
# 
# ```
# ['backup_supported_version',
#  'created_by',
#  'creation_time',
#  'description',
#  'identity_domain',
#  'last_modified_time',
#  'legacy',
#  'service_name',
#  'service_uri',
#  'service_uuid',
#  'sm_plugin_version',
#  'status',
#  'tags',
#  'tools_version',
#  'version']
# 
# ```
# 

# In[7]:


@dataclass
class DBInstance:
    backup_supported_version: str
    created_by: str
    creation_time: str
    description: str
    identity_domain: str
    last_modified_time: str
    legacy: bool
    service_name: str
    service_uri: str
    service_uuid: str
    sm_plugin_version: str
    status: str
    tags: List[str]
    tools_version: str
    version: str
    
    


# In[8]:



formats = []


def NO_OP(x):
    return x




DEFAULT_FORMATS = {
    'byte': SwaggerFormat(
        format='byte',
        to_wire=lambda b: b if isinstance(b, str) else str(b),
        to_python=lambda s: s if isinstance(s, str) else str(s),
        validate=NO_OP,  # jsonschema validates string
        description='Converts [wire]string:byte <=> python byte'),
    'date': SwaggerFormat(
        format='date',
        to_wire=lambda d: d.isoformat(),
        to_python=lambda d: dateutil.parser.parse(d).date(),
        validate=NO_OP,  # jsonschema validates date
        description='Converts [wire]string:date <=> python datetime.date'),
    # Python has no double. float is C's double in CPython
    'double': SwaggerFormat(
        format='double',
        to_wire=lambda d: d if isinstance(d, float) else float(d),
        to_python=lambda d: d if isinstance(d, float) else float(d),
        validate=NO_OP,  # jsonschema validates number
        description='Converts [wire]number:double <=> python float'),
    'date-time': SwaggerFormat(
        format='date-time',
        to_wire=lambda dt: (dt if dt.tzinfo else pytz.utc.localize(dt)).isoformat(),
        to_python=lambda dt: dateutil.parser.parse(dt),
        validate=NO_OP,  # jsonschema validates date-time
        description=(
            'Converts string:date-time <=> python datetime.datetime')),
    'float': SwaggerFormat(
        format='float',
        to_wire=lambda f: f if isinstance(f, float) else float(f),
        to_python=lambda f: f if isinstance(f, float) else float(f),
        validate=NO_OP,  # jsonschema validates number
        description='Converts [wire]number:float <=> python float'),
    'int32': SwaggerFormat(
        format='int32',
        to_wire=lambda i: i if isinstance(i, int) else int(i),
        to_python=lambda i: i if isinstance(i, int) else int(i),
        validate=NO_OP,  # jsonschema validates integer
        description='Converts [wire]integer:int32 <=> python int'),
    'int64': SwaggerFormat(
        format='int64',
        to_wire=lambda i: i if isinstance(i, long) else long(i),
        to_python=lambda i: i if isinstance(i, long) else long(i),
        validate=NO_OP,  # jsonschema validates integer
        description='Converts [wire]integer:int64 <=> python long'),
}


# In[9]:


class BooleanString:
    str_to_bool: Dict[str, bool] = dict(true=True, false=False)

    def __init__(self, from_wire: str):
        self.from_wire= from_wire
        self._as_boolean = self.str_to_bool[from_wire.lower()]
        _debug(f'created')
        # if self.validate(boolish):
        #     self.as_boolean = self.json_bool_values[boolish]
        # if self.boolish_literal != self.boolish:
        #     _warning(f"case sensitive data passed, self.boolish_literal={self.boolish_literal}")

    @classmethod
    def validate(cls, from_wire: str) -> bool:
        _debug(f"from_wire={from_wire}")
        try:
            as_boolean = cls.str_to_bool[from_wire.lower()]
        except KeyError:
            raise SwaggerValidationError(f"Value={from_wire} not recognized as JsonBool")
        return isinstance(as_boolean, bool)

    def __bool__(self):
        return self.as_boolean

    @property
    def as_boolean(self):
        as_boolean = self.str_to_bool[self.from_wire.lower()]
        return as_boolean

    @property
    def as_wire(self):
        return self.from_wire

    @classmethod
    def bool_to_wire(cls, b):
        _bool_to_wire = 'true' if b else 'false'
        return _bool_to_wire

    @classmethod
    def str_to_python(cls, s):
        _str_to_python = cls.str_to_bool.get(s, False)
        return _str_to_python


json_bool_format = SwaggerFormat(
    # name of the format as used in the Swagger spec
    format='json_bool',

    # Callable to convert a python object to_wire representations
    to_wire=lambda json_bool_instance: json_bool_instance.as_wire,

    # Callable to convert a from_wire to a python object
    to_python=lambda s: BooleanString(s),

    # Callable to validate the cidr in string form
    validate=BooleanString.validate,
    description='Converts "true" and "false" to/from equivalent booleans.'
)


formats.append(json_bool_format)


# ## Datetime Formats
# 
# ```
# 
# ValidationError: '2018-02-13T18:52:10.094+0000' is not a 'date-time'
# 
# Failed validating 'format' in schema['properties']['services']['items']['properties']['creation_time']:
#     {'description': 'The date-and-time stamp when the service instance was '
#                     'created.',
#      'format': 'date-time',
#      'type': 'string'}
# 
# On instance['services'][0]['creation_time']:
#     '2018-02-13T18:52:10.094+0000'
# 
# 
# ['2018-02-13T18:52:10.094+0000',
#  '2018-02-08T02:28:59.340+0000',
#  '2018-06-12T07:58:43.885+0000',
#  '2018-02-09T20:07:53.200+0000',
#  '2018-02-09T18:49:59.402+0000',
#  '2018-02-09T18:54:59.716+0000',
#  '2018-04-19T16:15:38.385+0000',
#  '2018-02-06T21:07:36.169+0000',
#  '2018-06-20T21:59:58.528+0000',
#  '2017-11-20T16:37:17.660+0000',
#  '2017-11-20T16:33:24.806+0000',
#  '2017-11-27T18:08:14.002+0000',
#  '2018-03-01T06:24:54.258+0000',
#  '2018-04-26T16:03:53.716+0000',
#  '2018-05-25T11:46:58.318+0000',
#  '2018-04-19T18:57:38.754+0000',
#  '2018-07-11T17:46:36.383+0000',
#  '2018-05-03T02:30:41.464+0000',
#  '2018-04-27T21:32:26.952+0000',
#  '2018-03-01T06:29:36.569+0000']
# 
# ```

# In[10]:

#
# import maya
# from dateutil.parser import parse
# s = '2018-02-13T18:52:10.094+0000'
#
# parse


# In[11]:

#
# dt = parse(s)
# type(dt)
# print(dt)


# In[12]:


paas_date_time =  SwaggerFormat(
        format='paas-date-time',
        to_wire=lambda dt: dt.iso8601(),
        to_python=lambda dt: maya.parse(dt),
        validate=NO_OP,  # jsonschema validates date-time
        description=(
            'Converts string:date-time <=> python datetime.datetime'))


# In[13]:


# mdt = maya.parse(s)


# In[14]:


# mdt.iso8601()


# In[15]:


paas_date_time =  SwaggerFormat(
        format='paas-date-time',
        to_wire=lambda dt: dt.iso8601(),
        to_python=lambda dt: maya.parse(dt),
        validate=NO_OP,  # jsonschema validates date-time
        description=(
            'Converts string:date-time <=> python datetime.datetime'))


# In[16]:


# rest_endpoint = 'https://dbaas.oraclecloud.com/'
# swagger_file = 'dbcsServiceInstancesUsingFormats.json'
rest_endpoint = 'https://compute.uscom-central-1.oraclecloud.com'
auth_endpoint = f'{rest_endpoint}/authenticate/'
swagger_file = 'SecRules.json'

config = {'validate_responses': True, 
          'validate_requests': True, 
         'validate_swagger_spec': True,
#           'validate_swagger_spec': False,
          'use_models': True, 
          'include_missing_properties': True,
          'default_type_to_object': True,
          'internally_dereference_refs': False, 
          'formats': [paas_date_time],
          'also_return_response': True}


# In[17]:


dbcs_spec_dict = json.loads(open(swagger_file, 'r').read())
dbcs_spec_dict.keys()


# In[18]:


# Spec.from_dict(cls, spec_dict, origin_url=None, http_client=None, config=None):
dbcs_swagger_spec = Spec.from_dict(spec_dict=dbcs_spec_dict, origin_url=rest_endpoint , config=config)


# In[19]:


print(f"user_defined_formats=[{dbcs_swagger_spec.user_defined_formats}]")
print(dbcs_swagger_spec.origin_url)
print(dbcs_swagger_spec.api_url)


# In[20]:


print(dbcs_swagger_spec.config)


# In[21]:


http_client = RequestsClient()
http_client.set_basic_auth(rest_endpoint, opc_username, opc_password)


# In[22]:


idm_domain_name = 'gc30003'
idm_service_instance_id = '587626604'


### Username/pass setup
idm_domain_username = f'/Compute-{idm_domain_name}/{opc_username}'
idm_service_instance_username = f'/Compute-{idm_service_instance_id}/{opc_username}'
# username = traditional_iaas_username
username = idm_service_instance_username
# basic_auth_cred = _basic_auth_str(username, opc_password)

json_data = {"user": username, "password": opc_password}
print(json_data)


# In[23]:


http_client = RequestsClient()
http_client.set_basic_auth(rest_endpoint, opc_username, opc_password)
headers = dict([('Content-Type', 'application/oracle-compute-v3+json'),
                ('Accept', 'application/oracle-compute-v3+directory+json'),
                ])
# http_client = OCRequestsClient()
http_client.session.headers.update(headers)
if ORACLE_VPN_CONNECTED:
    http_client.session.proxies.update(proxies)


# print(f"http_client.session.headers before update: {http_client.session.headers}\n")
http_client.session.headers.update(headers)
# print(f"http_client.session.headers after update: {http_client.session.headers}\n")

response = http_client.session.post(url=auth_endpoint, json=json_data)
print(f'Response OK: {response.ok}, Status Code: {response.status_code}, URL: {response.url}')
if response.ok and 'Set-Cookie' in response.headers:
    print(f"Auth request succeess.\n")
    ### The auth cookie is already placed in the session ... nothing else needs to be done.
#     print(f"\nSession Cookies: {http_client.session.cookies}")
#     print(f"\nResponse Headers['Set-Cookie']: {response.headers['Set-Cookie']}")
else:
    print(f'Something failed! Response OK: {response.ok}, Status Code: {response.status_code}')

# print(f"http_client.session.headers before update: {http_client.session.headers}\n")
cookie_header = {'Cookie': response.headers['Set-Cookie']}
# print(f"cookie_header: {cookie_header}\n")
http_client.session.headers.update(cookie_header)
# print(f"http_client.session.headers after update: {http_client.session.headers}\n")


# In[24]:


dir(http_client)


# In[25]:


# SwaggerClient.from_spec(spec_dict, origin_url=None, http_client=None, config=None)


# In[26]:


# client = SwaggerClient.from_url(
#     'http://petstore.swagger.io/v2/swagger.json',
#     http_client=http_client,
# )
# pet = client.pet.getPetById(petId=42).response().result


# In[27]:


client = SwaggerClient.from_spec(spec_dict=dbcs_spec_dict, origin_url=rest_endpoint, http_client=http_client, config=config)


# In[28]:


print(f"user_defined_formats=[{client.spec.user_defined_formats}]")
print(client.swagger_spec.origin_url)
print(client.swagger_spec.api_url)
print(f"bravado_config=[{client.spec.config['bravado']}]")
print(f"schemes=[{client.spec.client_spec_dict['schemes']}]")


# In[29]:


print(client.swagger_spec.config)


# In[30]:


dir(client)
dir(client.SecRules)


# In[1]:


# client.SecRules.discoverRootSecRule?


# In[32]:


# config.keys()


# ```
# 
# curl -v --user 'eric.harris@oracle.com:V@nadium123!' -X GET "https://dbaas.oraclecloud.com:443/paas/service/dbcs/api/v1.1/instances/gc30003" -H "accept: application/json"  -H "X-ID-TENANT-NAME: gc30003"
# 
# 
# ```
# 

# 
# ```
#             "get":{
#                 "operationId":"getDomain",
#                 "summary":"View All Service Instances",
#                 "description":"Returns information about all Database Cloud Service instances. You can view the full set of details by specifying the <code>?outputLevel=verbose</code> query parameter.",
#                 "produces":[
#                     "application/json"
#                 ],
#                 "parameters":[
#                     {
#                         "name":"identityDomainId",
#                         "in":"path",
#                         "description":"Identity domain ID for the Database Cloud Service account:<br>&nbsp;<ul><li><p><b>For a Cloud account with Identity Cloud Service</b>: the identity service ID, which has the form <code>idcs-<i>letters-and-numbers</i></code>. You can find this ID in the <b>Identity Service Id</b> field on the Overview tab of the Service Details page for Database Cloud Service in My Services.</p></li><li><p><b>For a traditional cloud account</b>: the name of the identity domain.</p></li></ul>",
#                         "required":true,
#                         "type":"string"
#                     },
#                     {
#                         "name":"outputLevel",
#                         "in":"query",
#                         "description":"Flag that when set to <code>verbose</code> specifies that the response should include the full set of details for all service instances.",
#                         "required":false,
#                         "type":"boolean"
#                     },
#                     {
#                         "name":"Authorization",
#                         "in":"header",
#                         "description":"Base64 encoding of the user name and password of the user making the request. For more information, see <a href='http://www.oracle.com/pls/topic/lookup?ctx=cloud&id=dbcs_rest_secauth'>Security, Authentication and Authorization</a>.",
#                         "required":true,
#                         "type":"string"
#                     },
#                     {
#                         "name":"X-ID-TENANT-NAME",
#                         "in":"header",
#                         "description":"Identity domain ID for the Database Cloud Service account:<br>&nbsp;<ul><li><p><b>For a Cloud account with Identity Cloud Service</b>: the identity service ID, which has the form <code>idcs-<i>letters-and-numbers</i></code>. You can find this ID in the <b>Identity Service Id</b> field on the Overview tab of the Service Details page for Database Cloud Service in My Services.</p></li><li><p><b>For a traditional cloud account</b>: the name of the identity domain.</p></li></ul>",
#                         "required":true,
#                         "type":"string"
#                     }
#                 ],
#                 "responses":{
#                     "202":{
#                         "description":"Accepted. See <a href='http://www.oracle.com/pls/topic/lookup?ctx=cloud&id=dbcs_rest_statuses'>Status Codes</a> for information about other possible HTTP status codes.",
#                         "schema":{
#                             "$ref":"#/definitions/view-all-instances"
#                         }
#                     }
#                 }
#             }
#         },
# 
# 
# ```
# 

# In[33]:

#
# request_options = {'headers': {'Accept': 'application/oracle-compute-v3+directory+json',
#                                'Content-Type': 'application/oracle-compute-v3+json',
#                                'X-ID-TENANT-NAME': 'gc30003',
#                                'Authorization':'Basic ZXJpYy5oYXJyaXNAb3JhY2xlLmNvbTpWQG5hZGl1bTEyMyE='}}
#
#
# # In[34]:
#
#
# http_future = client.SecRules.discoverRootSecRule(_request_options=request_options)
#
#
# # In[35]:
#
#
# response = http_future.response()
#
#
# # In[36]:
#
#
# response.result
#
#
# # In[36]:
# r_incoming_response = response.incoming_response
# r_metadata_response = response.metadata
# r_result_response = response.result
#
#

# In[ ]:


request_options = {'headers': {'Accept':       'application/oracle-compute-v3+json',
                               'Content-Type': 'application/oracle-compute-v3+json',
                               'X-ID-TENANT-NAME': 'gc30003', 
                               'Authorization':'Basic ZXJpYy5oYXJyaXNAb3JhY2xlLmNvbTpWQG5hZGl1bTEyMyE='}}


# In[ ]:


http_future = client.SecRules.listSecRule(container='Compute-587626604', _request_options=request_options)


# In[ ]:


response = http_future.response()


# In[ ]:

r_incoming_response = response.incoming_response
r_metadata_response = response.metadata
r_result_response = response.result
r_result_json = response.incoming_response.json()

r_results = r_result_json['result']
r_result_0 = r_results[0]



# In[ ]:


dir(response.result)


# In[ ]:


response.result.services


# In[ ]:


response.result.services[0]


# In[ ]:


s = response.result.services[0]
print(s)
dir(s)


# In[ ]:


raw_result = response.incoming_response.text
dbcs_raw = Path('raw_result.txt')
fd = dbcs_raw.open('w')
fd.write(raw_result)
fd.close()


# In[ ]:


repr(s.creation_time)


# In[ ]:


type(s)

