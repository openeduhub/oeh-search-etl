# edu_sharing_client.MDSV1Api

All URIs are relative to *https://stable.demo.edu-sharing.net/edu-sharing/rest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_metadata_set**](MDSV1Api.md#get_metadata_set) | **GET** /mds/v1/metadatasets/{repository}/{metadataset} | Get metadata set new.
[**get_metadata_sets**](MDSV1Api.md#get_metadata_sets) | **GET** /mds/v1/metadatasets/{repository} | Get metadata sets V2 of repository.
[**get_values**](MDSV1Api.md#get_values) | **POST** /mds/v1/metadatasets/{repository}/{metadataset}/values | Get values.
[**get_values4_keys**](MDSV1Api.md#get_values4_keys) | **POST** /mds/v1/metadatasets/{repository}/{metadataset}/values_for_keys | Get values for keys.
[**suggest_value**](MDSV1Api.md#suggest_value) | **POST** /mds/v1/metadatasets/{repository}/{metadataset}/values/{widget}/suggest | Suggest a value.


# **get_metadata_set**
> Mds get_metadata_set(repository, metadataset)

Get metadata set new.

Get metadata set new.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.mds import Mds
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
    api_instance = edu_sharing_client.MDSV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    metadataset = '-default-' # str | ID of metadataset (or \"-default-\" for default metadata set) (default to '-default-')

    try:
        # Get metadata set new.
        api_response = api_instance.get_metadata_set(repository, metadataset)
        print("The response of MDSV1Api->get_metadata_set:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MDSV1Api->get_metadata_set: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **metadataset** | **str**| ID of metadataset (or \&quot;-default-\&quot; for default metadata set) | [default to &#39;-default-&#39;]

### Return type

[**Mds**](Mds.md)

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

# **get_metadata_sets**
> MdsEntries get_metadata_sets(repository)

Get metadata sets V2 of repository.

Get metadata sets V2 of repository.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.mds_entries import MdsEntries
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
    api_instance = edu_sharing_client.MDSV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')

    try:
        # Get metadata sets V2 of repository.
        api_response = api_instance.get_metadata_sets(repository)
        print("The response of MDSV1Api->get_metadata_sets:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MDSV1Api->get_metadata_sets: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]

### Return type

[**MdsEntries**](MdsEntries.md)

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

# **get_values**
> Suggestions get_values(repository, metadataset, suggestion_param=suggestion_param)

Get values.

Get values.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.suggestion_param import SuggestionParam
from edu_sharing_client.models.suggestions import Suggestions
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
    api_instance = edu_sharing_client.MDSV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    metadataset = '-default-' # str | ID of metadataset (or \"-default-\" for default metadata set) (default to '-default-')
    suggestion_param = edu_sharing_client.SuggestionParam() # SuggestionParam | suggestionParam (optional)

    try:
        # Get values.
        api_response = api_instance.get_values(repository, metadataset, suggestion_param=suggestion_param)
        print("The response of MDSV1Api->get_values:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MDSV1Api->get_values: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **metadataset** | **str**| ID of metadataset (or \&quot;-default-\&quot; for default metadata set) | [default to &#39;-default-&#39;]
 **suggestion_param** | [**SuggestionParam**](SuggestionParam.md)| suggestionParam | [optional] 

### Return type

[**Suggestions**](Suggestions.md)

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

# **get_values4_keys**
> Suggestions get_values4_keys(repository, metadataset, query=query, var_property=var_property, request_body=request_body)

Get values for keys.

Get values for keys.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.suggestions import Suggestions
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
    api_instance = edu_sharing_client.MDSV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    metadataset = '-default-' # str | ID of metadataset (or \"-default-\" for default metadata set) (default to '-default-')
    query = 'query_example' # str | query (optional)
    var_property = 'var_property_example' # str | property (optional)
    request_body = ['request_body_example'] # List[str] | keys (optional)

    try:
        # Get values for keys.
        api_response = api_instance.get_values4_keys(repository, metadataset, query=query, var_property=var_property, request_body=request_body)
        print("The response of MDSV1Api->get_values4_keys:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MDSV1Api->get_values4_keys: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **metadataset** | **str**| ID of metadataset (or \&quot;-default-\&quot; for default metadata set) | [default to &#39;-default-&#39;]
 **query** | **str**| query | [optional] 
 **var_property** | **str**| property | [optional] 
 **request_body** | [**List[str]**](str.md)| keys | [optional] 

### Return type

[**Suggestions**](Suggestions.md)

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

# **suggest_value**
> MdsValue suggest_value(repository, metadataset, widget, caption, parent=parent, node_id=node_id)

Suggest a value.

Suggest a new value for a given metadataset and widget. The suggestion will be forwarded to the corresponding person in the metadataset file

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.mds_value import MdsValue
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
    api_instance = edu_sharing_client.MDSV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    metadataset = '-default-' # str | ID of metadataset (or \"-default-\" for default metadata set) (default to '-default-')
    widget = 'widget_example' # str | widget id, e.g. cm:name
    caption = 'caption_example' # str | caption of the new entry (id will be auto-generated)
    parent = 'parent_example' # str | parent id of the new entry (might be null) (optional)
    node_id = ['node_id_example'] # List[str] | One or more nodes this suggestion relates to (optional, only for extended mail data) (optional)

    try:
        # Suggest a value.
        api_response = api_instance.suggest_value(repository, metadataset, widget, caption, parent=parent, node_id=node_id)
        print("The response of MDSV1Api->suggest_value:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MDSV1Api->suggest_value: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **metadataset** | **str**| ID of metadataset (or \&quot;-default-\&quot; for default metadata set) | [default to &#39;-default-&#39;]
 **widget** | **str**| widget id, e.g. cm:name | 
 **caption** | **str**| caption of the new entry (id will be auto-generated) | 
 **parent** | **str**| parent id of the new entry (might be null) | [optional] 
 **node_id** | [**List[str]**](str.md)| One or more nodes this suggestion relates to (optional, only for extended mail data) | [optional] 

### Return type

[**MdsValue**](MdsValue.md)

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

