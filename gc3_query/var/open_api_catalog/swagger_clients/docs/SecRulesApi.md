# swagger_client.SecRulesApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_sec_rule**](SecRulesApi.md#add_sec_rule) | **POST** /secrule/ | Create a Security Rule
[**delete_sec_rule**](SecRulesApi.md#delete_sec_rule) | **DELETE** /secrule/{name} | Delete a Security Rule
[**discover_root_sec_rule**](SecRulesApi.md#discover_root_sec_rule) | **GET** /secrule/ | Retrieve Names of Containers
[**discover_sec_rule**](SecRulesApi.md#discover_sec_rule) | **GET** /secrule/{container} | Retrieve Names of all Security Rules and Subcontainers in a Container
[**get_sec_rule**](SecRulesApi.md#get_sec_rule) | **GET** /secrule/{name} | Retrieve Details of a Security Rule
[**list_sec_rule**](SecRulesApi.md#list_sec_rule) | **GET** /secrule/{container}/ | Retrieve Details of all Security Rules in a Container
[**update_sec_rule**](SecRulesApi.md#update_sec_rule) | **PUT** /secrule/{name} | Update a Security Rule


# **add_sec_rule**
> SecRuleResponse add_sec_rule(body, cookie=cookie)

Create a Security Rule

<b>Required Role: </b>To complete this task, you must have the <code>Compute_Operations</code> role. If this role isn't assigned to you or you're not sure, then ask your system administrator to ensure that the role is assigned to you in Oracle Cloud My Services. See <a target=\"_blank\" href=\"http://www.oracle.com/pls/topic/lookup?ctx=stcomputecs&id=MMOCS-GUID-54C2E747-7D5B-451C-A39C-77936178EBB6\">Modifying User Roles</a> in <em>Managing and Monitoring Oracle Cloud</em>.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.SecRulesApi()
body = swagger_client.SecRulePostRequest() # SecRulePostRequest | 
cookie = 'cookie_example' # str | The Cookie: header must be included with every request to the service. It must be set to the value of the set-cookie header in the response received to the POST /authenticate/ call. (optional)

try:
    # Create a Security Rule
    api_response = api_instance.add_sec_rule(body, cookie=cookie)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SecRulesApi->add_sec_rule: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**SecRulePostRequest**](SecRulePostRequest.md)|  | 
 **cookie** | **str**| The Cookie: header must be included with every request to the service. It must be set to the value of the set-cookie header in the response received to the POST /authenticate/ call. | [optional] 

### Return type

[**SecRuleResponse**](SecRuleResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/oracle-compute-v3+json
 - **Accept**: application/oracle-compute-v3+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_sec_rule**
> delete_sec_rule(name, cookie=cookie)

Delete a Security Rule

<b>Required Role: </b>To complete this task, you must have the <code>Compute_Operations</code> role. If this role isn't assigned to you or you're not sure, then ask your system administrator to ensure that the role is assigned to you in Oracle Cloud My Services. See <a target=\"_blank\" href=\"http://www.oracle.com/pls/topic/lookup?ctx=stcomputecs&id=MMOCS-GUID-54C2E747-7D5B-451C-A39C-77936178EBB6\">Modifying User Roles</a> in <em>Managing and Monitoring Oracle Cloud</em>.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.SecRulesApi()
name = 'name_example' # str | The three-part name of the object (<code>/Compute-<em>identity_domain</em>/<em>user</em>/<em>object</em></code>).
cookie = 'cookie_example' # str | The Cookie: header must be included with every request to the service. It must be set to the value of the set-cookie header in the response received to the POST /authenticate/ call. (optional)

try:
    # Delete a Security Rule
    api_instance.delete_sec_rule(name, cookie=cookie)
except ApiException as e:
    print("Exception when calling SecRulesApi->delete_sec_rule: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| The three-part name of the object (&lt;code&gt;/Compute-&lt;em&gt;identity_domain&lt;/em&gt;/&lt;em&gt;user&lt;/em&gt;/&lt;em&gt;object&lt;/em&gt;&lt;/code&gt;). | 
 **cookie** | **str**| The Cookie: header must be included with every request to the service. It must be set to the value of the set-cookie header in the response received to the POST /authenticate/ call. | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/oracle-compute-v3+json
 - **Accept**: application/oracle-compute-v3+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **discover_root_sec_rule**
> SecRuleDiscoverResponse discover_root_sec_rule(cookie=cookie)

Retrieve Names of Containers

Retrieves the names of containers that contain objects that you can access. You can use this information to construct the multipart name of an object.<p><b>Required Role: </b>To complete this task, you must have the <code>Compute_Monitor</code> or <code>Compute_Operations</code> role. If this role isn't assigned to you or you're not sure, then ask your system administrator to ensure that the role is assigned to you in Oracle Cloud My Services. See <a target=\"_blank\" href=\"http://www.oracle.com/pls/topic/lookup?ctx=stcomputecs&id=MMOCS-GUID-54C2E747-7D5B-451C-A39C-77936178EBB6\">Modifying User Roles</a> in <em>Managing and Monitoring Oracle Cloud</em>.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.SecRulesApi()
cookie = 'cookie_example' # str | The Cookie: header must be included with every request to the service. It must be set to the value of the set-cookie header in the response received to the POST /authenticate/ call. (optional)

try:
    # Retrieve Names of Containers
    api_response = api_instance.discover_root_sec_rule(cookie=cookie)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SecRulesApi->discover_root_sec_rule: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cookie** | **str**| The Cookie: header must be included with every request to the service. It must be set to the value of the set-cookie header in the response received to the POST /authenticate/ call. | [optional] 

### Return type

[**SecRuleDiscoverResponse**](SecRuleDiscoverResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/oracle-compute-v3+json
 - **Accept**: application/oracle-compute-v3+directory+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **discover_sec_rule**
> SecRuleDiscoverResponse discover_sec_rule(container, cookie=cookie)

Retrieve Names of all Security Rules and Subcontainers in a Container

Retrieves the names of objects and subcontainers that you can access in the specified container.<p><b>Required Role: </b>To complete this task, you must have the <code>Compute_Monitor</code> or <code>Compute_Operations</code> role. If this role isn't assigned to you or you're not sure, then ask your system administrator to ensure that the role is assigned to you in Oracle Cloud My Services. See <a target=\"_blank\" href=\"http://www.oracle.com/pls/topic/lookup?ctx=stcomputecs&id=MMOCS-GUID-54C2E747-7D5B-451C-A39C-77936178EBB6\">Modifying User Roles</a> in <em>Managing and Monitoring Oracle Cloud</em>.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.SecRulesApi()
container = 'container_example' # str | Specify <code>/Compute-<i>identityDomain</i>/<i>user</i>/</code> to retrieve the names of objects that you can access. Specify <code>/Compute-<i>identityDomain</i>/</code> to retrieve the names of containers that contain objects that you can access.
cookie = 'cookie_example' # str | The Cookie: header must be included with every request to the service. It must be set to the value of the set-cookie header in the response received to the POST /authenticate/ call. (optional)

try:
    # Retrieve Names of all Security Rules and Subcontainers in a Container
    api_response = api_instance.discover_sec_rule(container, cookie=cookie)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SecRulesApi->discover_sec_rule: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **container** | **str**| Specify &lt;code&gt;/Compute-&lt;i&gt;identityDomain&lt;/i&gt;/&lt;i&gt;user&lt;/i&gt;/&lt;/code&gt; to retrieve the names of objects that you can access. Specify &lt;code&gt;/Compute-&lt;i&gt;identityDomain&lt;/i&gt;/&lt;/code&gt; to retrieve the names of containers that contain objects that you can access. | 
 **cookie** | **str**| The Cookie: header must be included with every request to the service. It must be set to the value of the set-cookie header in the response received to the POST /authenticate/ call. | [optional] 

### Return type

[**SecRuleDiscoverResponse**](SecRuleDiscoverResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/oracle-compute-v3+json
 - **Accept**: application/oracle-compute-v3+directory+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_sec_rule**
> SecRuleResponse get_sec_rule(name, cookie=cookie)

Retrieve Details of a Security Rule

Retrieves details of the specified security rule. You can use this request to verify whether POST and PUT HTTP requests were completed successfully.<p><b>Required Role: </b>To complete this task, you must have the <code>Compute_Monitor</code> or <code>Compute_Operations</code> role. If this role isn't assigned to you or you're not sure, then ask your system administrator to ensure that the role is assigned to you in Oracle Cloud My Services. See <a target=\"_blank\" href=\"http://www.oracle.com/pls/topic/lookup?ctx=stcomputecs&id=MMOCS-GUID-54C2E747-7D5B-451C-A39C-77936178EBB6\">Modifying User Roles</a> in <em>Managing and Monitoring Oracle Cloud</em>.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.SecRulesApi()
name = 'name_example' # str | The three-part name of the object (<code>/Compute-<em>identity_domain</em>/<em>user</em>/<em>object</em></code>).
cookie = 'cookie_example' # str | The Cookie: header must be included with every request to the service. It must be set to the value of the set-cookie header in the response received to the POST /authenticate/ call. (optional)

try:
    # Retrieve Details of a Security Rule
    api_response = api_instance.get_sec_rule(name, cookie=cookie)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SecRulesApi->get_sec_rule: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| The three-part name of the object (&lt;code&gt;/Compute-&lt;em&gt;identity_domain&lt;/em&gt;/&lt;em&gt;user&lt;/em&gt;/&lt;em&gt;object&lt;/em&gt;&lt;/code&gt;). | 
 **cookie** | **str**| The Cookie: header must be included with every request to the service. It must be set to the value of the set-cookie header in the response received to the POST /authenticate/ call. | [optional] 

### Return type

[**SecRuleResponse**](SecRuleResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/oracle-compute-v3+json
 - **Accept**: application/oracle-compute-v3+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_sec_rule**
> SecRuleListResponse list_sec_rule(container, dst_list=dst_list, description=description, src_list=src_list, disabled=disabled, application=application, name=name, cookie=cookie)

Retrieve Details of all Security Rules in a Container

Retrieves details of the security rules that are in the specified container and match the specified query criteria. If you don't specify any query criteria, then details of all the security rules in the container are displayed. To filter the search results, you can pass one or more of the following query parameters, by appending them to the URI in the following syntax:<p><code>?parameter1=value1&ampparameter2=value2&ampparameterN=valueN</code><p><b>Required Role: </b>To complete this task, you must have the <code>Compute_Monitor</code> or <code>Compute_Operations</code> role. If this role isn't assigned to you or you're not sure, then ask your system administrator to ensure that the role is assigned to you in Oracle Cloud My Services. See <a target=\"_blank\" href=\"http://www.oracle.com/pls/topic/lookup?ctx=stcomputecs&id=MMOCS-GUID-54C2E747-7D5B-451C-A39C-77936178EBB6\">Modifying User Roles</a> in <em>Managing and Monitoring Oracle Cloud</em>.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.SecRulesApi()
container = 'container_example' # str | <p><code>/Compute-<em>identity_domain</em>/<em>user</em></code> or <code>/Compute-<em>identity_domain</em>/</code> for user-defined security rules.
dst_list = 'dst_list_example' # str | <p>The three-part name (<code>/Compute-<em>identity_domain</em>/<em>user</em>/<em>object_name</em></code>) of the destination security list or security IP list.<p>You must use the prefix <code>seclist</code>: or <code>seciplist</code>: to identify the list type.<p><b>Note:</b> You can specify a security IP list as the destination in a secrule, provided <code>src_list</code> is a security list that has DENY as its outbound policy.<p>You cannot specify any of the security IP lists in the <code>/oracle/public</code> container as a destination in a secrule. (optional)
description = 'description_example' # str | <p>A description of the security rule. (optional)
src_list = 'src_list_example' # str | <p>The three-part name (<code>/Compute-<em>identity_domain</em>/<em>user</em>/<em>object_name</em></code>) of the source security list or security IP list.<p>You must use the prefix <code>seclist</code>: or <code>seciplist</code>: to identify the list type. (optional)
disabled = true # bool | <p>Indicates whether the security rule is enabled (set to <code>false</code>) or disabled (<code>true</code>). The default setting is <code>false</code>. (optional)
application = 'application_example' # str | <p>The three-part name of the security application: (<code>/Compute-<em>identity_domain</em>/<em>user</em>/<em>object_name</em></code>) for user-defined security applications and <code>/oracle/public/<em>object_name</em></code> for predefined security applications. (optional)
name = 'name_example' # str | The three-part name of the object (<code>/Compute-<em>identity_domain</em>/<em>user</em>/<em>object</em></code>). (optional)
cookie = 'cookie_example' # str | The Cookie: header must be included with every request to the service. It must be set to the value of the set-cookie header in the response received to the POST /authenticate/ call. (optional)

try:
    # Retrieve Details of all Security Rules in a Container
    api_response = api_instance.list_sec_rule(container, dst_list=dst_list, description=description, src_list=src_list, disabled=disabled, application=application, name=name, cookie=cookie)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SecRulesApi->list_sec_rule: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **container** | **str**| &lt;p&gt;&lt;code&gt;/Compute-&lt;em&gt;identity_domain&lt;/em&gt;/&lt;em&gt;user&lt;/em&gt;&lt;/code&gt; or &lt;code&gt;/Compute-&lt;em&gt;identity_domain&lt;/em&gt;/&lt;/code&gt; for user-defined security rules. | 
 **dst_list** | **str**| &lt;p&gt;The three-part name (&lt;code&gt;/Compute-&lt;em&gt;identity_domain&lt;/em&gt;/&lt;em&gt;user&lt;/em&gt;/&lt;em&gt;object_name&lt;/em&gt;&lt;/code&gt;) of the destination security list or security IP list.&lt;p&gt;You must use the prefix &lt;code&gt;seclist&lt;/code&gt;: or &lt;code&gt;seciplist&lt;/code&gt;: to identify the list type.&lt;p&gt;&lt;b&gt;Note:&lt;/b&gt; You can specify a security IP list as the destination in a secrule, provided &lt;code&gt;src_list&lt;/code&gt; is a security list that has DENY as its outbound policy.&lt;p&gt;You cannot specify any of the security IP lists in the &lt;code&gt;/oracle/public&lt;/code&gt; container as a destination in a secrule. | [optional] 
 **description** | **str**| &lt;p&gt;A description of the security rule. | [optional] 
 **src_list** | **str**| &lt;p&gt;The three-part name (&lt;code&gt;/Compute-&lt;em&gt;identity_domain&lt;/em&gt;/&lt;em&gt;user&lt;/em&gt;/&lt;em&gt;object_name&lt;/em&gt;&lt;/code&gt;) of the source security list or security IP list.&lt;p&gt;You must use the prefix &lt;code&gt;seclist&lt;/code&gt;: or &lt;code&gt;seciplist&lt;/code&gt;: to identify the list type. | [optional] 
 **disabled** | **bool**| &lt;p&gt;Indicates whether the security rule is enabled (set to &lt;code&gt;false&lt;/code&gt;) or disabled (&lt;code&gt;true&lt;/code&gt;). The default setting is &lt;code&gt;false&lt;/code&gt;. | [optional] 
 **application** | **str**| &lt;p&gt;The three-part name of the security application: (&lt;code&gt;/Compute-&lt;em&gt;identity_domain&lt;/em&gt;/&lt;em&gt;user&lt;/em&gt;/&lt;em&gt;object_name&lt;/em&gt;&lt;/code&gt;) for user-defined security applications and &lt;code&gt;/oracle/public/&lt;em&gt;object_name&lt;/em&gt;&lt;/code&gt; for predefined security applications. | [optional] 
 **name** | **str**| The three-part name of the object (&lt;code&gt;/Compute-&lt;em&gt;identity_domain&lt;/em&gt;/&lt;em&gt;user&lt;/em&gt;/&lt;em&gt;object&lt;/em&gt;&lt;/code&gt;). | [optional] 
 **cookie** | **str**| The Cookie: header must be included with every request to the service. It must be set to the value of the set-cookie header in the response received to the POST /authenticate/ call. | [optional] 

### Return type

[**SecRuleListResponse**](SecRuleListResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/oracle-compute-v3+json
 - **Accept**: application/oracle-compute-v3+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_sec_rule**
> SecRuleResponse update_sec_rule(name, body, cookie=cookie)

Update a Security Rule

Disables or enables the specified security rule. You can also update the description of the security rule.<p><b>Required Role: </b>To complete this task, you must have the <code>Compute_Operations</code> role. If this role isn't assigned to you or you're not sure, then ask your system administrator to ensure that the role is assigned to you in Oracle Cloud My Services. See <a target=\"_blank\" href=\"http://www.oracle.com/pls/topic/lookup?ctx=stcomputecs&id=MMOCS-GUID-54C2E747-7D5B-451C-A39C-77936178EBB6\">Modifying User Roles</a> in <em>Managing and Monitoring Oracle Cloud</em>.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.SecRulesApi()
name = 'name_example' # str | The three-part name of the object (<code>/Compute-<em>identity_domain</em>/<em>user</em>/<em>object</em></code>).
body = swagger_client.SecRulePutRequest() # SecRulePutRequest | 
cookie = 'cookie_example' # str | The Cookie: header must be included with every request to the service. It must be set to the value of the set-cookie header in the response received to the POST /authenticate/ call. (optional)

try:
    # Update a Security Rule
    api_response = api_instance.update_sec_rule(name, body, cookie=cookie)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SecRulesApi->update_sec_rule: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| The three-part name of the object (&lt;code&gt;/Compute-&lt;em&gt;identity_domain&lt;/em&gt;/&lt;em&gt;user&lt;/em&gt;/&lt;em&gt;object&lt;/em&gt;&lt;/code&gt;). | 
 **body** | [**SecRulePutRequest**](SecRulePutRequest.md)|  | 
 **cookie** | **str**| The Cookie: header must be included with every request to the service. It must be set to the value of the set-cookie header in the response received to the POST /authenticate/ call. | [optional] 

### Return type

[**SecRuleResponse**](SecRuleResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/oracle-compute-v3+json
 - **Accept**: application/oracle-compute-v3+json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

