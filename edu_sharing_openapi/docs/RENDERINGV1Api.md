# edu_sharing_client.RENDERINGV1Api

All URIs are relative to *https://stable.demo.edu-sharing.net/edu-sharing/rest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_details_snippet1**](RENDERINGV1Api.md#get_details_snippet1) | **GET** /rendering/v1/details/{repository}/{node} | Get metadata of node.
[**get_details_snippet_with_parameters**](RENDERINGV1Api.md#get_details_snippet_with_parameters) | **POST** /rendering/v1/details/{repository}/{node} | Get metadata of node.


# **get_details_snippet1**
> RenderingDetailsEntry get_details_snippet1(repository, node, version=version, display_mode=display_mode)

Get metadata of node.

Get metadata of node.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.rendering_details_entry import RenderingDetailsEntry
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
    api_instance = edu_sharing_client.RENDERINGV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node
    version = 'version_example' # str | version of node (optional)
    display_mode = 'display_mode_example' # str | Rendering displayMode (optional)

    try:
        # Get metadata of node.
        api_response = api_instance.get_details_snippet1(repository, node, version=version, display_mode=display_mode)
        print("The response of RENDERINGV1Api->get_details_snippet1:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RENDERINGV1Api->get_details_snippet1: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 
 **version** | **str**| version of node | [optional] 
 **display_mode** | **str**| Rendering displayMode | [optional] 

### Return type

[**RenderingDetailsEntry**](RenderingDetailsEntry.md)

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

# **get_details_snippet_with_parameters**
> RenderingDetailsEntry get_details_snippet_with_parameters(repository, node, version=version, display_mode=display_mode, request_body=request_body)

Get metadata of node.

Get metadata of node.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.rendering_details_entry import RenderingDetailsEntry
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
    api_instance = edu_sharing_client.RENDERINGV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node
    version = 'version_example' # str | version of node (optional)
    display_mode = 'display_mode_example' # str | Rendering displayMode (optional)
    request_body = {'key': 'request_body_example'} # Dict[str, str] | additional parameters to send to the rendering service (optional)

    try:
        # Get metadata of node.
        api_response = api_instance.get_details_snippet_with_parameters(repository, node, version=version, display_mode=display_mode, request_body=request_body)
        print("The response of RENDERINGV1Api->get_details_snippet_with_parameters:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RENDERINGV1Api->get_details_snippet_with_parameters: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 
 **version** | **str**| version of node | [optional] 
 **display_mode** | **str**| Rendering displayMode | [optional] 
 **request_body** | [**Dict[str, str]**](str.md)| additional parameters to send to the rendering service | [optional] 

### Return type

[**RenderingDetailsEntry**](RenderingDetailsEntry.md)

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

