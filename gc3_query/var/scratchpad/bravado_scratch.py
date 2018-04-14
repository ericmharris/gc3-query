# coding: utf-8

import os
from pathlib import Path
from bravado.client import SwaggerClient
from bravado.client import SwaggerClient
from bravado.swagger_model import load_file
# from bravado.requests_client import RequestsClient
from gc3_query.lib.requests_client import OPCRequestsClient
from bravado.swagger_model import load_file
from secrets import opc_username, opc_password

from urllib.parse import quote_plus, unquote_plus

## https://medium.com/@betz.mark/validate-json-models-with-swagger-and-bravado-5fad6b21a825
# Validate json models with swagger and bravado
from bravado_core.spec import Spec
from bravado_core.validate import validate_object
from yaml import load, Loader, dump, Dumper

# In[4]:


idm_domain_name = 'gc30003'
idm_service_instance_id = '587626604'
iaas_rest_endpoint = r'https://compute.uscom-central-1.oraclecloud.com'
iaas_auth_endpoint = f'{iaas_rest_endpoint}/authenticate/'

print(f'iaas_rest_endpoint: {iaas_rest_endpoint}')
print(f'iaas_auth_endpoint: {iaas_auth_endpoint}\n')

# In[5]:


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

files = None
params = None


headers = dict([('Content-Type', 'application/oracle-compute-v3+json'),
                ('Accept', 'application/oracle-compute-v3+directory+json'),
                ])

print(f'headers: {headers}')

# In[6]:


requests_client = OPCRequestsClient()
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

# In[10]:


print(f"requests_client.session.headers before update: {requests_client.session.headers}\n")
cookie_header = {'Cookie': response.headers['Set-Cookie']}
print(f"cookie_header: {cookie_header}\n")
requests_client.session.headers.update(cookie_header)
print(f"requests_client.session.headers after update: {requests_client.session.headers}\n")

#

# In[11]:


cwd = os.getcwd()
spec_file_path = Path().joinpath('open_api_definitions/iaas_instances.json').resolve()
print(f'spec_file_path exists: {spec_file_path.exists()}, spec_file_path: {spec_file_path}')

#### http://bravado.readthedocs.io/en/latest/advanced.html#loading-swagger-json-by-file-path
## needed for: client = SwaggerClient.from_url('file:///some/path/swagger.json')
spec_file_uri = f"file:///{spec_file_path}"
print(f'spec_file_uri: {spec_file_path}')


# In[14]:


spec_dict = load_file(spec_file_path)
spec_dict['schemes']
print(f"Original spec: spec_dict['schemes']: {spec_dict['schemes']}")
spec_dict['schemes'] = ['https']
print(f"Spec after scheme update: spec_dict['schemes']: {spec_dict['schemes']}")

# In[17]:


swagger_spec = Spec.from_dict(spec_dict=spec_dict,
                              origin_url=iaas_rest_endpoint,
                              http_client=requests_client,

                              )

# In[18]:



print(f"swagger_spec.api_url: {swagger_spec.api_url}")



swagger_client = SwaggerClient.from_spec(spec_dict=spec_dict,
                                         origin_url=iaas_rest_endpoint,
                                         http_client=requests_client,
                                         config={'also_return_response': True,
                                                 'validate_responses': False,
                                                 'validate_requests': False,
                                                 'validate_swagger_spec': False})

# In[20]:


print(f"swagger_client: {swagger_client}, swagger_client.Instances.resource.operations: {swagger_client.Instances.resource.operations}")

op = swagger_client.Instances.resource.operations['discoverInstance']
op_api_url = op.swagger_spec.api_url
print(f"discoverInstance Operation: {op}, discoverInstance.api_url: {op_api_url}")

# In[22]:


instances = swagger_client.Instances

# In[23]:


print(f"instances: {instances}, idm_service_instance_username: {idm_service_instance_username}")

# In[25]:



# In[36]:



# In[37]:

##  Fails, URL is /instance/%2FCompute-587626604%2Feric.harris%40oracle.com%2F -> /instance//Compute-587626604/eric.harris%40oracle.com/
# discover_instance_result = discover_instance.result()

## getting https://compute.uscom-central-1.oraclecloud.com/instance/Compute-587626604%2Feric.harris%40oracle.com%2F
## but want https://compute.uscom-central-1.oraclecloud.com/instance/Compute-587626604/eric.harris@oracle.com/
# container = f"{idm_service_instance_username[1:]}/"
container = r"Compute-587626604/eric.harris@oracle.com/"
print(f"container is: {container}")

discover_instance = instances.discoverInstance(container=container)

print(f"""discover_instance: {discover_instance}, 
discover_instance.operation: {discover_instance.operation}, 
discover_instance.operation.params: {discover_instance.operation.params}, 
discover_instance.operation.operation_id: {discover_instance.operation.operation_id}""")

# In[ ]:



# In[ ]:


discover_instance_result, discover_instance_response = discover_instance.result()

# In[ ]:


print(f"""discover_instance_result: {discover_instance_result}, 
discover_instance_response: {discover_instance_response} 
""")


