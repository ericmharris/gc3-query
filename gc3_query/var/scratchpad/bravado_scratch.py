import os
from bravado.client import SwaggerClient
from bravado.client import SwaggerClient

# Example with Basic Authentication
from bravado.requests_client import RequestsClient
from bravado.client import SwaggerClient

from requests.auth import _basic_auth_str
from secrets import opc_username, opc_password



cwd = os.getcwd()

idm_domain = 'gc30003'
# idm_domain = '587626604'
idm_username = f'{idm_domain}.{opc_username}'
print(f'idm_username: {idm_username}')
# load Swagger resource file into App object
domain_auth_token = _basic_auth_str(idm_username, opc_password)
print(f'domain_auth_token: {domain_auth_token}')

compute_container = '/Compute-587626604/eric.harris@oracle.com'
print(f'compute_container: {compute_container}')
rest_endpoint = r'https://compute.uscom-central-1.oraclecloud.com/'

# client_from_file = SwaggerClient.from_url(f'file:///{cwd}/instances_swagger.json')


swagger_url= r'https://apicatalog.oraclecloud.com/v1/orgs/oracle-public/apicollections/compute/18.1.2/apis/Instances/canonical'
requests_client = RequestsClient()
# requests_client.set_basic_auth('apicatalog.oraclecloud.com', idm_username, opc_password)
requests_client.set_basic_auth(rest_endpoint, idm_username, opc_password)
requests_client.session.headers['Authorization'] = domain_auth_token

# client_from_catalog = SwaggerClient.from_url(spec_url=swagger_url, http_client=requests_client)
client_from_catalog = SwaggerClient.from_url(spec_url=swagger_url, http_client=requests_client, config={'also_return_response': True})

# instance_list = client_from_catalog.Instances.listInstance(container=compute_container)
instance_name = r'/Compute-587626604/eric.harris@oracle.com/GC3NAAC-CDMT-LWS1'
instance_name = '/Compute-587626604/eric.harris@oracle.com/GC3NAAC-CDMT-LWS1/c17bb7ea-724b-4e51-ab72-1bd8714f07b7'
# instance = client_from_catalog.Instances.getInstance(name='/Compute-587626604/eric.harris@oracle.com/GC3NAAC-CDMT-LWS1/c17bb7ea-724b-4e51-ab72-1bd8714f07b7').result()
# instance = client_from_catalog.Instances.getInstance(name=r'/Compute-587626604/eric.harris@oracle.com/GC3NAAC-CDMT-LWS1').result()
## https://bravado.readthedocs.io/en/latest/advanced.html#getting-access-to-the-http-response
instance, http_response = client_from_catalog.Instances.getInstance(name=instance_name).result()

print('done.')


