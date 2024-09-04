# edu_sharing_client.BULKV1Api

All URIs are relative to *https://stable.demo.edu-sharing.net/edu-sharing/rest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**find**](BULKV1Api.md#find) | **POST** /bulk/v1/find | gets a given node
[**sync**](BULKV1Api.md#sync) | **PUT** /bulk/v1/sync/{group} | Create or update a given node


# **find**
> NodeEntry find(request_body, resolve_node=resolve_node)

gets a given node

Get a given node based on the posted, multiple criteria. Make sure that they'll provide an unique result

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.node_entry import NodeEntry
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
    api_instance = edu_sharing_client.BULKV1Api(api_client)
    request_body = None # Dict[str, List[str]] | properties that must match (with \"AND\" concatenated)
    resolve_node = True # bool | Return the full node. If you don't need the data, set to false to only return the id (will improve performance) (optional) (default to True)

    try:
        # gets a given node
        api_response = api_instance.find(request_body, resolve_node=resolve_node)
        print("The response of BULKV1Api->find:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BULKV1Api->find: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **request_body** | [**Dict[str, List[str]]**](List.md)| properties that must match (with \&quot;AND\&quot; concatenated) | 
 **resolve_node** | **bool**| Return the full node. If you don&#39;t need the data, set to false to only return the id (will improve performance) | [optional] [default to True]

### Return type

[**NodeEntry**](NodeEntry.md)

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

# **sync**
> NodeEntry sync(group, match, type, request_body, group_by=group_by, aspects=aspects, resolve_node=resolve_node, reset_version=reset_version)

Create or update a given node

Depending on the given \"match\" properties either a new node will be created or the existing one will be updated

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.node_entry import NodeEntry
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
    api_instance = edu_sharing_client.BULKV1Api(api_client)
    group = 'group_example' # str | The group to which this node belongs to. Used for internal structuring. Please use simple names only
    match = ['match_example'] # List[str] | The properties that must match to identify if this node exists. Multiple properties will be and combined and compared
    type = 'type_example' # str | type of node. If the node already exists, this will not change the type afterwards
    request_body = None # Dict[str, List[str]] | properties, they'll not get filtered via mds, so be careful what you add here
    group_by = ['group_by_example'] # List[str] | The properties on which the imported nodes should be grouped (for each value, a folder with the corresponding data is created) (optional)
    aspects = ['aspects_example'] # List[str] | aspects of node (optional)
    resolve_node = True # bool | Return the generated or updated node. If you don't need the data, set to false to only return the id (will improve performance) (optional) (default to True)
    reset_version = True # bool | reset all versions (like a complete reimport), all data inside edu-sharing will be lost (optional)

    try:
        # Create or update a given node
        api_response = api_instance.sync(group, match, type, request_body, group_by=group_by, aspects=aspects, resolve_node=resolve_node, reset_version=reset_version)
        print("The response of BULKV1Api->sync:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BULKV1Api->sync: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group** | **str**| The group to which this node belongs to. Used for internal structuring. Please use simple names only | 
 **match** | [**List[str]**](str.md)| The properties that must match to identify if this node exists. Multiple properties will be and combined and compared | 
 **type** | **str**| type of node. If the node already exists, this will not change the type afterwards | 
 **request_body** | [**Dict[str, List[str]]**](List.md)| properties, they&#39;ll not get filtered via mds, so be careful what you add here | 
 **group_by** | [**List[str]**](str.md)| The properties on which the imported nodes should be grouped (for each value, a folder with the corresponding data is created) | [optional] 
 **aspects** | [**List[str]**](str.md)| aspects of node | [optional] 
 **resolve_node** | **bool**| Return the generated or updated node. If you don&#39;t need the data, set to false to only return the id (will improve performance) | [optional] [default to True]
 **reset_version** | **bool**| reset all versions (like a complete reimport), all data inside edu-sharing will be lost | [optional] 

### Return type

[**NodeEntry**](NodeEntry.md)

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

