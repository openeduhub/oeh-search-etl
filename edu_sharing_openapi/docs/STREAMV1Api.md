# edu_sharing_client.STREAMV1Api

All URIs are relative to *https://stable.demo.edu-sharing.net/edu-sharing/rest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_entry**](STREAMV1Api.md#add_entry) | **PUT** /stream/v1/add/{repository} | add a new stream object.
[**can_access**](STREAMV1Api.md#can_access) | **GET** /stream/v1/access/{repository}/{node} | test
[**delete_entry**](STREAMV1Api.md#delete_entry) | **DELETE** /stream/v1/delete/{repository}/{entry} | delete a stream object
[**get_property_values**](STREAMV1Api.md#get_property_values) | **GET** /stream/v1/properties/{repository}/{property} | Get top values for a property
[**search1**](STREAMV1Api.md#search1) | **POST** /stream/v1/search/{repository} | Get the stream content for the current user with the given status.
[**update_entry**](STREAMV1Api.md#update_entry) | **PUT** /stream/v1/status/{repository}/{entry} | update status for a stream object and authority


# **add_entry**
> StreamEntryInput add_entry(repository, stream_entry_input)

add a new stream object.

will return the object and add the id to the object if creation succeeded

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.stream_entry_input import StreamEntryInput
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
    api_instance = edu_sharing_client.STREAMV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    stream_entry_input = edu_sharing_client.StreamEntryInput() # StreamEntryInput | Stream object to add

    try:
        # add a new stream object.
        api_response = api_instance.add_entry(repository, stream_entry_input)
        print("The response of STREAMV1Api->add_entry:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling STREAMV1Api->add_entry: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **stream_entry_input** | [**StreamEntryInput**](StreamEntryInput.md)| Stream object to add | 

### Return type

[**StreamEntryInput**](StreamEntryInput.md)

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

# **can_access**
> str can_access(repository, node)

test

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
    api_instance = edu_sharing_client.STREAMV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | The property to aggregate

    try:
        # test
        api_response = api_instance.can_access(repository, node)
        print("The response of STREAMV1Api->can_access:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling STREAMV1Api->can_access: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| The property to aggregate | 

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

# **delete_entry**
> delete_entry(repository, entry)

delete a stream object

the current user must be author of the given stream object

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
    api_instance = edu_sharing_client.STREAMV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    entry = 'entry_example' # str | entry id to delete

    try:
        # delete a stream object
        api_instance.delete_entry(repository, entry)
    except Exception as e:
        print("Exception when calling STREAMV1Api->delete_entry: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **entry** | **str**| entry id to delete | 

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
**200** | OK. |  -  |
**400** | Preconditions are not present. |  -  |
**401** | Authorization failed. |  -  |
**403** | Session user has insufficient rights to perform this operation. |  -  |
**404** | Ressources are not found. |  -  |
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_property_values**
> str get_property_values(repository, var_property)

Get top values for a property

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
    api_instance = edu_sharing_client.STREAMV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    var_property = 'var_property_example' # str | The property to aggregate

    try:
        # Get top values for a property
        api_response = api_instance.get_property_values(repository, var_property)
        print("The response of STREAMV1Api->get_property_values:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling STREAMV1Api->get_property_values: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **var_property** | **str**| The property to aggregate | 

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

# **search1**
> StreamList search1(repository, status=status, query=query, max_items=max_items, skip_count=skip_count, sort_properties=sort_properties, sort_ascending=sort_ascending, request_body=request_body)

Get the stream content for the current user with the given status.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.stream_list import StreamList
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
    api_instance = edu_sharing_client.STREAMV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    status = 'status_example' # str | Stream object status to search for (optional)
    query = 'query_example' # str | generic text to search for (in title or description) (optional)
    max_items = 10 # int | maximum items per page (optional) (default to 10)
    skip_count = 0 # int | skip a number of items (optional) (default to 0)
    sort_properties = ['sort_properties_example'] # List[str] | sort properties, currently supported: created, priority, default: priority desc, created desc (optional)
    sort_ascending = [True] # List[bool] | sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index (optional)
    request_body = {'key': 'request_body_example'} # Dict[str, str] | map with property + value to search (optional)

    try:
        # Get the stream content for the current user with the given status.
        api_response = api_instance.search1(repository, status=status, query=query, max_items=max_items, skip_count=skip_count, sort_properties=sort_properties, sort_ascending=sort_ascending, request_body=request_body)
        print("The response of STREAMV1Api->search1:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling STREAMV1Api->search1: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **status** | **str**| Stream object status to search for | [optional] 
 **query** | **str**| generic text to search for (in title or description) | [optional] 
 **max_items** | **int**| maximum items per page | [optional] [default to 10]
 **skip_count** | **int**| skip a number of items | [optional] [default to 0]
 **sort_properties** | [**List[str]**](str.md)| sort properties, currently supported: created, priority, default: priority desc, created desc | [optional] 
 **sort_ascending** | [**List[bool]**](bool.md)| sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index | [optional] 
 **request_body** | [**Dict[str, str]**](str.md)| map with property + value to search | [optional] 

### Return type

[**StreamList**](StreamList.md)

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

# **update_entry**
> update_entry(repository, entry, authority, status)

update status for a stream object and authority

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
    api_instance = edu_sharing_client.STREAMV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    entry = 'entry_example' # str | entry id to update
    authority = 'authority_example' # str | authority to set/change status
    status = 'status_example' # str | New status for this authority

    try:
        # update status for a stream object and authority
        api_instance.update_entry(repository, entry, authority, status)
    except Exception as e:
        print("Exception when calling STREAMV1Api->update_entry: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **entry** | **str**| entry id to update | 
 **authority** | **str**| authority to set/change status | 
 **status** | **str**| New status for this authority | 

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
**200** | OK. |  -  |
**400** | Preconditions are not present. |  -  |
**401** | Authorization failed. |  -  |
**403** | Session user has insufficient rights to perform this operation. |  -  |
**404** | Ressources are not found. |  -  |
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

