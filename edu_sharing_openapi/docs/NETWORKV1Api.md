# edu_sharing_client.NETWORKV1Api

All URIs are relative to *https://stable.demo.edu-sharing.net/edu-sharing/rest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_service**](NETWORKV1Api.md#add_service) | **POST** /network/v1/services | Register service.
[**get_repositories**](NETWORKV1Api.md#get_repositories) | **GET** /network/v1/repositories | Get repositories.
[**get_service**](NETWORKV1Api.md#get_service) | **GET** /network/v1/service | Get own service.
[**get_services**](NETWORKV1Api.md#get_services) | **GET** /network/v1/services | Get services.
[**update_service**](NETWORKV1Api.md#update_service) | **PUT** /network/v1/services/{id} | Update a service.


# **add_service**
> StoredService add_service(service=service)

Register service.

Register a new service.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.service import Service
from edu_sharing_client.models.stored_service import StoredService
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
    api_instance = edu_sharing_client.NETWORKV1Api(api_client)
    service = edu_sharing_client.Service() # Service | Service data object (optional)

    try:
        # Register service.
        api_response = api_instance.add_service(service=service)
        print("The response of NETWORKV1Api->add_service:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NETWORKV1Api->add_service: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **service** | [**Service**](Service.md)| Service data object | [optional] 

### Return type

[**StoredService**](StoredService.md)

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

# **get_repositories**
> RepoEntries get_repositories()

Get repositories.

Get repositories.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.repo_entries import RepoEntries
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
    api_instance = edu_sharing_client.NETWORKV1Api(api_client)

    try:
        # Get repositories.
        api_response = api_instance.get_repositories()
        print("The response of NETWORKV1Api->get_repositories:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NETWORKV1Api->get_repositories: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**RepoEntries**](RepoEntries.md)

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

# **get_service**
> StoredService get_service()

Get own service.

Get the servic entry from the current repository.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.stored_service import StoredService
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
    api_instance = edu_sharing_client.NETWORKV1Api(api_client)

    try:
        # Get own service.
        api_response = api_instance.get_service()
        print("The response of NETWORKV1Api->get_service:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NETWORKV1Api->get_service: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**StoredService**](StoredService.md)

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

# **get_services**
> str get_services(query=query)

Get services.

Get registerted services.

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
    api_instance = edu_sharing_client.NETWORKV1Api(api_client)
    query = 'query_example' # str | search or filter for services (optional)

    try:
        # Get services.
        api_response = api_instance.get_services(query=query)
        print("The response of NETWORKV1Api->get_services:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NETWORKV1Api->get_services: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **query** | **str**| search or filter for services | [optional] 

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

# **update_service**
> StoredService update_service(id, service=service)

Update a service.

Update an existing service.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.service import Service
from edu_sharing_client.models.stored_service import StoredService
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
    api_instance = edu_sharing_client.NETWORKV1Api(api_client)
    id = 'id_example' # str | Service id
    service = edu_sharing_client.Service() # Service | Service data object (optional)

    try:
        # Update a service.
        api_response = api_instance.update_service(id, service=service)
        print("The response of NETWORKV1Api->update_service:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NETWORKV1Api->update_service: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Service id | 
 **service** | [**Service**](Service.md)| Service data object | [optional] 

### Return type

[**StoredService**](StoredService.md)

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

