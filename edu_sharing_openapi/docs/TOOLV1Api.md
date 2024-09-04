# edu_sharing_client.TOOLV1Api

All URIs are relative to *https://stable.demo.edu-sharing.net/edu-sharing/rest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_tool_defintition**](TOOLV1Api.md#create_tool_defintition) | **POST** /tool/v1/tools/{repository}/tooldefinitions | Create a new tool definition object.
[**create_tool_instance**](TOOLV1Api.md#create_tool_instance) | **POST** /tool/v1/tools/{repository}/{toolDefinition}/toolinstances | Create a new tool Instance object.
[**create_tool_object**](TOOLV1Api.md#create_tool_object) | **POST** /tool/v1/tools/{repository}/{toolinstance}/toolobject | Create a new tool object for a given tool instance.
[**get_all_tool_definitions**](TOOLV1Api.md#get_all_tool_definitions) | **GET** /tool/v1/tools/{repository}/tooldefinitions | Get all ToolDefinitions.
[**get_instance**](TOOLV1Api.md#get_instance) | **GET** /tool/v1/tools/{repository}/{nodeid}/toolinstance | Get Instances of a ToolDefinition.
[**get_instances**](TOOLV1Api.md#get_instances) | **GET** /tool/v1/tools/{repository}/{toolDefinition}/toolinstances | Get Instances of a ToolDefinition.


# **create_tool_defintition**
> NodeEntry create_tool_defintition(repository, request_body, rename_if_exists=rename_if_exists, version_comment=version_comment)

Create a new tool definition object.

Create a new tool definition object.

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
    api_instance = edu_sharing_client.TOOLV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    request_body = None # Dict[str, List[str]] | properties, example: {\"{http://www.alfresco.org/model/content/1.0}name\": [\"test\"]}
    rename_if_exists = False # bool | rename if the same node name exists (optional) (default to False)
    version_comment = 'version_comment_example' # str | comment, leave empty = no inital version (optional)

    try:
        # Create a new tool definition object.
        api_response = api_instance.create_tool_defintition(repository, request_body, rename_if_exists=rename_if_exists, version_comment=version_comment)
        print("The response of TOOLV1Api->create_tool_defintition:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TOOLV1Api->create_tool_defintition: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **request_body** | [**Dict[str, List[str]]**](List.md)| properties, example: {\&quot;{http://www.alfresco.org/model/content/1.0}name\&quot;: [\&quot;test\&quot;]} | 
 **rename_if_exists** | **bool**| rename if the same node name exists | [optional] [default to False]
 **version_comment** | **str**| comment, leave empty &#x3D; no inital version | [optional] 

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
**409** | Duplicate Entity/Node conflict (Node with same name exists) |  -  |
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_tool_instance**
> NodeEntry create_tool_instance(repository, tool_definition, request_body, rename_if_exists=rename_if_exists, version_comment=version_comment)

Create a new tool Instance object.

Create a new tool Instance object.

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
    api_instance = edu_sharing_client.TOOLV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    tool_definition = 'tool_definition_example' # str | ID of parent node must have tool_definition aspect
    request_body = None # Dict[str, List[str]] | properties, example: {\"{http://www.alfresco.org/model/content/1.0}name\": [\"test\"]}
    rename_if_exists = False # bool | rename if the same node name exists (optional) (default to False)
    version_comment = 'version_comment_example' # str | comment, leave empty = no inital version (optional)

    try:
        # Create a new tool Instance object.
        api_response = api_instance.create_tool_instance(repository, tool_definition, request_body, rename_if_exists=rename_if_exists, version_comment=version_comment)
        print("The response of TOOLV1Api->create_tool_instance:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TOOLV1Api->create_tool_instance: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **tool_definition** | **str**| ID of parent node must have tool_definition aspect | 
 **request_body** | [**Dict[str, List[str]]**](List.md)| properties, example: {\&quot;{http://www.alfresco.org/model/content/1.0}name\&quot;: [\&quot;test\&quot;]} | 
 **rename_if_exists** | **bool**| rename if the same node name exists | [optional] [default to False]
 **version_comment** | **str**| comment, leave empty &#x3D; no inital version | [optional] 

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
**409** | Duplicate Entity/Node conflict (Node with same name exists) |  -  |
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_tool_object**
> NodeEntry create_tool_object(repository, toolinstance, request_body, rename_if_exists=rename_if_exists, version_comment=version_comment)

Create a new tool object for a given tool instance.

Create a new tool object for a given tool instance.

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
    api_instance = edu_sharing_client.TOOLV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    toolinstance = 'toolinstance_example' # str | ID of parent node (a tool instance object)
    request_body = None # Dict[str, List[str]] | properties, example: {\"{http://www.alfresco.org/model/content/1.0}name\": [\"test\"]}
    rename_if_exists = False # bool | rename if the same node name exists (optional) (default to False)
    version_comment = 'version_comment_example' # str | comment, leave empty = no inital version (optional)

    try:
        # Create a new tool object for a given tool instance.
        api_response = api_instance.create_tool_object(repository, toolinstance, request_body, rename_if_exists=rename_if_exists, version_comment=version_comment)
        print("The response of TOOLV1Api->create_tool_object:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TOOLV1Api->create_tool_object: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **toolinstance** | **str**| ID of parent node (a tool instance object) | 
 **request_body** | [**Dict[str, List[str]]**](List.md)| properties, example: {\&quot;{http://www.alfresco.org/model/content/1.0}name\&quot;: [\&quot;test\&quot;]} | 
 **rename_if_exists** | **bool**| rename if the same node name exists | [optional] [default to False]
 **version_comment** | **str**| comment, leave empty &#x3D; no inital version | [optional] 

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
**409** | Duplicate Entity/Node conflict (Node with same name exists) |  -  |
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_tool_definitions**
> NodeEntry get_all_tool_definitions(repository)

Get all ToolDefinitions.

Get all ToolDefinitions.

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
    api_instance = edu_sharing_client.TOOLV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')

    try:
        # Get all ToolDefinitions.
        api_response = api_instance.get_all_tool_definitions(repository)
        print("The response of TOOLV1Api->get_all_tool_definitions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TOOLV1Api->get_all_tool_definitions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]

### Return type

[**NodeEntry**](NodeEntry.md)

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

# **get_instance**
> NodeEntry get_instance(repository, nodeid)

Get Instances of a ToolDefinition.

Get Instances of a ToolDefinition.

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
    api_instance = edu_sharing_client.TOOLV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    nodeid = 'nodeid_example' # str | ID of node

    try:
        # Get Instances of a ToolDefinition.
        api_response = api_instance.get_instance(repository, nodeid)
        print("The response of TOOLV1Api->get_instance:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TOOLV1Api->get_instance: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **nodeid** | **str**| ID of node | 

### Return type

[**NodeEntry**](NodeEntry.md)

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

# **get_instances**
> NodeEntry get_instances(repository, tool_definition)

Get Instances of a ToolDefinition.

Get Instances of a ToolDefinition.

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
    api_instance = edu_sharing_client.TOOLV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    tool_definition = 'tool_definition_example' # str | ID of node

    try:
        # Get Instances of a ToolDefinition.
        api_response = api_instance.get_instances(repository, tool_definition)
        print("The response of TOOLV1Api->get_instances:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TOOLV1Api->get_instances: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **tool_definition** | **str**| ID of node | 

### Return type

[**NodeEntry**](NodeEntry.md)

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

