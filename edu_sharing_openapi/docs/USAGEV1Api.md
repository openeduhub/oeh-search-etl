# edu_sharing_client.USAGEV1Api

All URIs are relative to *https://stable.demo.edu-sharing.net/edu-sharing/rest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_usage**](USAGEV1Api.md#delete_usage) | **DELETE** /usage/v1/usages/node/{nodeId}/{usageId} | Delete an usage of a node.
[**get_usages**](USAGEV1Api.md#get_usages) | **GET** /usage/v1/usages/{appId} | Get all usages of an application.
[**get_usages1**](USAGEV1Api.md#get_usages1) | **GET** /usage/v1/usages/repository/{repositoryId}/{nodeId} | 
[**get_usages_by_course**](USAGEV1Api.md#get_usages_by_course) | **GET** /usage/v1/usages/course/{appId}/{courseId} | Get all usages of an course.
[**get_usages_by_node**](USAGEV1Api.md#get_usages_by_node) | **GET** /usage/v1/usages/node/{nodeId} | Get all usages of an node.
[**get_usages_by_node_collections**](USAGEV1Api.md#get_usages_by_node_collections) | **GET** /usage/v1/usages/node/{nodeId}/collections | Get all collections where this node is used.
[**set_usage**](USAGEV1Api.md#set_usage) | **POST** /usage/v1/usages/repository/{repositoryId} | Set a usage for a node. app signature headers and authenticated user required.


# **delete_usage**
> Usages delete_usage(node_id, usage_id)

Delete an usage of a node.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.usages import Usages
from edu_sharing_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://stable.demo.edu-sharing.net/edu-sharing/rest
# See configuration.py for a list of all supported configuration parameters.
configuration = edu_sharing_client.Configuration(
    host = "https://stable.demo.edu-sharing.net/edu-sharing/rest"
)


# Enter a context with an instance of the API client
with edu_sharing_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = edu_sharing_client.USAGEV1Api(api_client)
    node_id = 'node_id_example' # str | ID of node
    usage_id = 'usage_id_example' # str | ID of usage

    try:
        # Delete an usage of a node.
        api_response = api_instance.delete_usage(node_id, usage_id)
        print("The response of USAGEV1Api->delete_usage:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling USAGEV1Api->delete_usage: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **node_id** | **str**| ID of node | 
 **usage_id** | **str**| ID of usage | 

### Return type

[**Usages**](Usages.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK. |  -  |
**400** | Preconditions are not present. |  -  |
**401** | Authorization failed. |  -  |
**403** | Session user has insufficient rights to perform this operation. |  -  |
**404** | Ressources are not found. |  -  |
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_usages**
> Usages get_usages(app_id)

Get all usages of an application.

Get all usages of an application.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.usages import Usages
from edu_sharing_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://stable.demo.edu-sharing.net/edu-sharing/rest
# See configuration.py for a list of all supported configuration parameters.
configuration = edu_sharing_client.Configuration(
    host = "https://stable.demo.edu-sharing.net/edu-sharing/rest"
)


# Enter a context with an instance of the API client
with edu_sharing_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = edu_sharing_client.USAGEV1Api(api_client)
    app_id = 'app_id_example' # str | ID of application (or \"-home-\" for home repository)

    try:
        # Get all usages of an application.
        api_response = api_instance.get_usages(app_id)
        print("The response of USAGEV1Api->get_usages:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling USAGEV1Api->get_usages: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| ID of application (or \&quot;-home-\&quot; for home repository) | 

### Return type

[**Usages**](Usages.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK. |  -  |
**400** | Preconditions are not present. |  -  |
**401** | Authorization failed. |  -  |
**403** | Session user has insufficient rights to perform this operation. |  -  |
**404** | Ressources are not found. |  -  |
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_usages1**
> get_usages1(repository_id, node_id, var_from=var_from, to=to)



### Example


```python
import edu_sharing_client
from edu_sharing_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://stable.demo.edu-sharing.net/edu-sharing/rest
# See configuration.py for a list of all supported configuration parameters.
configuration = edu_sharing_client.Configuration(
    host = "https://stable.demo.edu-sharing.net/edu-sharing/rest"
)


# Enter a context with an instance of the API client
with edu_sharing_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = edu_sharing_client.USAGEV1Api(api_client)
    repository_id = '-home-' # str | ID of repository (default to '-home-')
    node_id = '-all-' # str | ID of node. Use -all- for getting usages of all nodes (default to '-all-')
    var_from = 56 # int | from date (optional)
    to = 56 # int | to date (optional)

    try:
        api_instance.get_usages1(repository_id, node_id, var_from=var_from, to=to)
    except Exception as e:
        print("Exception when calling USAGEV1Api->get_usages1: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository_id** | **str**| ID of repository | [default to &#39;-home-&#39;]
 **node_id** | **str**| ID of node. Use -all- for getting usages of all nodes | [default to &#39;-all-&#39;]
 **var_from** | **int**| from date | [optional] 
 **to** | **int**| to date | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**0** | default response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_usages_by_course**
> Usages get_usages_by_course(app_id, course_id)

Get all usages of an course.

Get all usages of an course.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.usages import Usages
from edu_sharing_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://stable.demo.edu-sharing.net/edu-sharing/rest
# See configuration.py for a list of all supported configuration parameters.
configuration = edu_sharing_client.Configuration(
    host = "https://stable.demo.edu-sharing.net/edu-sharing/rest"
)


# Enter a context with an instance of the API client
with edu_sharing_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = edu_sharing_client.USAGEV1Api(api_client)
    app_id = 'app_id_example' # str | ID of application (or \"-home-\" for home repository)
    course_id = 'course_id_example' # str | ID of course

    try:
        # Get all usages of an course.
        api_response = api_instance.get_usages_by_course(app_id, course_id)
        print("The response of USAGEV1Api->get_usages_by_course:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling USAGEV1Api->get_usages_by_course: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| ID of application (or \&quot;-home-\&quot; for home repository) | 
 **course_id** | **str**| ID of course | 

### Return type

[**Usages**](Usages.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK. |  -  |
**400** | Preconditions are not present. |  -  |
**401** | Authorization failed. |  -  |
**403** | Session user has insufficient rights to perform this operation. |  -  |
**404** | Ressources are not found. |  -  |
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_usages_by_node**
> Usages get_usages_by_node(node_id)

Get all usages of an node.

Get all usages of an node.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.usages import Usages
from edu_sharing_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://stable.demo.edu-sharing.net/edu-sharing/rest
# See configuration.py for a list of all supported configuration parameters.
configuration = edu_sharing_client.Configuration(
    host = "https://stable.demo.edu-sharing.net/edu-sharing/rest"
)


# Enter a context with an instance of the API client
with edu_sharing_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = edu_sharing_client.USAGEV1Api(api_client)
    node_id = 'node_id_example' # str | ID of node

    try:
        # Get all usages of an node.
        api_response = api_instance.get_usages_by_node(node_id)
        print("The response of USAGEV1Api->get_usages_by_node:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling USAGEV1Api->get_usages_by_node: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **node_id** | **str**| ID of node | 

### Return type

[**Usages**](Usages.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK. |  -  |
**400** | Preconditions are not present. |  -  |
**401** | Authorization failed. |  -  |
**403** | Session user has insufficient rights to perform this operation. |  -  |
**404** | Ressources are not found. |  -  |
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_usages_by_node_collections**
> str get_usages_by_node_collections(node_id)

Get all collections where this node is used.

### Example


```python
import edu_sharing_client
from edu_sharing_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://stable.demo.edu-sharing.net/edu-sharing/rest
# See configuration.py for a list of all supported configuration parameters.
configuration = edu_sharing_client.Configuration(
    host = "https://stable.demo.edu-sharing.net/edu-sharing/rest"
)


# Enter a context with an instance of the API client
with edu_sharing_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = edu_sharing_client.USAGEV1Api(api_client)
    node_id = 'node_id_example' # str | ID of node

    try:
        # Get all collections where this node is used.
        api_response = api_instance.get_usages_by_node_collections(node_id)
        print("The response of USAGEV1Api->get_usages_by_node_collections:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling USAGEV1Api->get_usages_by_node_collections: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **node_id** | **str**| ID of node | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK. |  -  |
**400** | Preconditions are not present. |  -  |
**401** | Authorization failed. |  -  |
**403** | Session user has insufficient rights to perform this operation. |  -  |
**404** | Ressources are not found. |  -  |
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_usage**
> Usage set_usage(repository_id, create_usage)

Set a usage for a node. app signature headers and authenticated user required.

headers must be set: X-Edu-App-Id, X-Edu-App-Sig, X-Edu-App-Signed, X-Edu-App-Ts

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.create_usage import CreateUsage
from edu_sharing_client.models.usage import Usage
from edu_sharing_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://stable.demo.edu-sharing.net/edu-sharing/rest
# See configuration.py for a list of all supported configuration parameters.
configuration = edu_sharing_client.Configuration(
    host = "https://stable.demo.edu-sharing.net/edu-sharing/rest"
)


# Enter a context with an instance of the API client
with edu_sharing_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = edu_sharing_client.USAGEV1Api(api_client)
    repository_id = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    create_usage = edu_sharing_client.CreateUsage() # CreateUsage |  usage date

    try:
        # Set a usage for a node. app signature headers and authenticated user required.
        api_response = api_instance.set_usage(repository_id, create_usage)
        print("The response of USAGEV1Api->set_usage:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling USAGEV1Api->set_usage: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository_id** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **create_usage** | [**CreateUsage**](CreateUsage.md)|  usage date | 

### Return type

[**Usage**](Usage.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK. |  -  |
**400** | Preconditions are not present. |  -  |
**401** | Authorization failed. |  -  |
**403** | Session user has insufficient rights to perform this operation. |  -  |
**404** | Ressources are not found. |  -  |
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

