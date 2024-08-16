# edu_sharing_client.SHARINGV1Api

All URIs are relative to *https://stable.demo.edu-sharing.net/edu-sharing/rest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_children1**](SHARINGV1Api.md#get_children1) | **GET** /sharing/v1/sharing/{repository}/{node}/{share}/children | Get all children of this share.
[**get_info**](SHARINGV1Api.md#get_info) | **GET** /sharing/v1/sharing/{repository}/{node}/{share} | Get general info of a share.


# **get_children1**
> NodeEntries get_children1(repository, node, share, password=password, max_items=max_items, skip_count=skip_count, sort_properties=sort_properties, sort_ascending=sort_ascending)

Get all children of this share.

Only valid for shared folders

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.node_entries import NodeEntries
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
    api_instance = edu_sharing_client.SHARINGV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node
    share = 'share_example' # str | Share token
    password = 'password_example' # str | Password (required if share is locked) (optional)
    max_items = 500 # int | maximum items per page (optional) (default to 500)
    skip_count = 0 # int | skip a number of items (optional) (default to 0)
    sort_properties = ['sort_properties_example'] # List[str] | sort properties (optional)
    sort_ascending = [True] # List[bool] | sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index (optional)

    try:
        # Get all children of this share.
        api_response = api_instance.get_children1(repository, node, share, password=password, max_items=max_items, skip_count=skip_count, sort_properties=sort_properties, sort_ascending=sort_ascending)
        print("The response of SHARINGV1Api->get_children1:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SHARINGV1Api->get_children1: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 
 **share** | **str**| Share token | 
 **password** | **str**| Password (required if share is locked) | [optional] 
 **max_items** | **int**| maximum items per page | [optional] [default to 500]
 **skip_count** | **int**| skip a number of items | [optional] [default to 0]
 **sort_properties** | [**List[str]**](str.md)| sort properties | [optional] 
 **sort_ascending** | [**List[bool]**](bool.md)| sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index | [optional] 

### Return type

[**NodeEntries**](NodeEntries.md)

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

# **get_info**
> SharingInfo get_info(repository, node, share, password=password)

Get general info of a share.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.sharing_info import SharingInfo
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
    api_instance = edu_sharing_client.SHARINGV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node
    share = 'share_example' # str | Share token
    password = 'password_example' # str | Password to validate (optional) (optional)

    try:
        # Get general info of a share.
        api_response = api_instance.get_info(repository, node, share, password=password)
        print("The response of SHARINGV1Api->get_info:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SHARINGV1Api->get_info: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 
 **share** | **str**| Share token | 
 **password** | **str**| Password to validate (optional) | [optional] 

### Return type

[**SharingInfo**](SharingInfo.md)

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

