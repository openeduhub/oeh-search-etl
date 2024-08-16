# edu_sharing_client.NODEV1Api

All URIs are relative to *https://stable.demo.edu-sharing.net/edu-sharing/rest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_aspects**](NODEV1Api.md#add_aspects) | **PUT** /node/v1/nodes/{repository}/{node}/aspects | Add aspect to node.
[**add_workflow_history**](NODEV1Api.md#add_workflow_history) | **PUT** /node/v1/nodes/{repository}/{node}/workflow | Add workflow.
[**change_content1**](NODEV1Api.md#change_content1) | **POST** /node/v1/nodes/{repository}/{node}/content | Change content of node.
[**change_content_as_text**](NODEV1Api.md#change_content_as_text) | **POST** /node/v1/nodes/{repository}/{node}/textContent | Change content of node as text.
[**change_metadata**](NODEV1Api.md#change_metadata) | **PUT** /node/v1/nodes/{repository}/{node}/metadata | Change metadata of node.
[**change_metadata_with_versioning**](NODEV1Api.md#change_metadata_with_versioning) | **POST** /node/v1/nodes/{repository}/{node}/metadata | Change metadata of node (new version).
[**change_preview**](NODEV1Api.md#change_preview) | **POST** /node/v1/nodes/{repository}/{node}/preview | Change preview of node.
[**change_template_metadata**](NODEV1Api.md#change_template_metadata) | **PUT** /node/v1/nodes/{repository}/{node}/metadata/template | Set the metadata template for this folder.
[**copy_metadata**](NODEV1Api.md#copy_metadata) | **PUT** /node/v1/nodes/{repository}/{node}/metadata/copy/{from} | Copy metadata from another node.
[**create_child**](NODEV1Api.md#create_child) | **POST** /node/v1/nodes/{repository}/{node}/children | Create a new child.
[**create_child_by_copying**](NODEV1Api.md#create_child_by_copying) | **POST** /node/v1/nodes/{repository}/{node}/children/_copy | Create a new child by copying.
[**create_child_by_moving**](NODEV1Api.md#create_child_by_moving) | **POST** /node/v1/nodes/{repository}/{node}/children/_move | Create a new child by moving.
[**create_fork_of_node**](NODEV1Api.md#create_fork_of_node) | **POST** /node/v1/nodes/{repository}/{node}/children/_fork | Create a copy of a node by creating a forked version (variant).
[**create_share**](NODEV1Api.md#create_share) | **PUT** /node/v1/nodes/{repository}/{node}/shares | Create a share for a node.
[**delete**](NODEV1Api.md#delete) | **DELETE** /node/v1/nodes/{repository}/{node} | Delete node.
[**delete_preview**](NODEV1Api.md#delete_preview) | **DELETE** /node/v1/nodes/{repository}/{node}/preview | Delete preview of node.
[**get_assocs**](NODEV1Api.md#get_assocs) | **GET** /node/v1/nodes/{repository}/{node}/assocs | Get related nodes.
[**get_children**](NODEV1Api.md#get_children) | **GET** /node/v1/nodes/{repository}/{node}/children | Get children of node.
[**get_lrmi_data**](NODEV1Api.md#get_lrmi_data) | **GET** /node/v1/nodes/{repository}/{node}/lrmi | Get lrmi data.
[**get_metadata**](NODEV1Api.md#get_metadata) | **GET** /node/v1/nodes/{repository}/{node}/metadata | Get metadata of node.
[**get_nodes**](NODEV1Api.md#get_nodes) | **POST** /node/v1/nodes/{repository} | Searching nodes.
[**get_notify_list**](NODEV1Api.md#get_notify_list) | **GET** /node/v1/nodes/{repository}/{node}/notifys | Get notifys (sharing history) of the node.
[**get_parents**](NODEV1Api.md#get_parents) | **GET** /node/v1/nodes/{repository}/{node}/parents | Get parents of node.
[**get_permission**](NODEV1Api.md#get_permission) | **GET** /node/v1/nodes/{repository}/{node}/permissions | Get all permission of node.
[**get_published_copies**](NODEV1Api.md#get_published_copies) | **GET** /node/v1/nodes/{repository}/{node}/publish | Publish
[**get_shares**](NODEV1Api.md#get_shares) | **GET** /node/v1/nodes/{repository}/{node}/shares | Get shares of node.
[**get_stats**](NODEV1Api.md#get_stats) | **GET** /node/v1/nodes/{repository}/{node}/stats | Get statistics of node.
[**get_template_metadata**](NODEV1Api.md#get_template_metadata) | **GET** /node/v1/nodes/{repository}/{node}/metadata/template | Get the metadata template + status for this folder.
[**get_text_content**](NODEV1Api.md#get_text_content) | **GET** /node/v1/nodes/{repository}/{node}/textContent | Get the text content of a document.
[**get_version_metadata**](NODEV1Api.md#get_version_metadata) | **GET** /node/v1/nodes/{repository}/{node}/versions/{major}/{minor}/metadata | Get metadata of node version.
[**get_versions**](NODEV1Api.md#get_versions) | **GET** /node/v1/nodes/{repository}/{node}/versions | Get all versions of node.
[**get_versions1**](NODEV1Api.md#get_versions1) | **GET** /node/v1/nodes/{repository}/{node}/versions/metadata | Get all versions of node, including it&#39;s metadata.
[**get_workflow_history**](NODEV1Api.md#get_workflow_history) | **GET** /node/v1/nodes/{repository}/{node}/workflow | Get workflow history.
[**has_permission**](NODEV1Api.md#has_permission) | **GET** /node/v1/nodes/{repository}/{node}/permissions/{user} | Which permissions has user/group for node.
[**import_node**](NODEV1Api.md#import_node) | **POST** /node/v1/nodes/{repository}/{node}/import | Import node
[**islocked**](NODEV1Api.md#islocked) | **GET** /node/v1/nodes/{repository}/{node}/lock/status | locked status of a node.
[**prepare_usage**](NODEV1Api.md#prepare_usage) | **POST** /node/v1/nodes/{repository}/{node}/prepareUsage | create remote object and get properties.
[**publish_copy**](NODEV1Api.md#publish_copy) | **POST** /node/v1/nodes/{repository}/{node}/publish | Publish
[**remove_share**](NODEV1Api.md#remove_share) | **DELETE** /node/v1/nodes/{repository}/{node}/shares/{shareId} | Remove share of a node.
[**report_node**](NODEV1Api.md#report_node) | **POST** /node/v1/nodes/{repository}/{node}/report | Report the node.
[**revert_version**](NODEV1Api.md#revert_version) | **PUT** /node/v1/nodes/{repository}/{node}/versions/{major}/{minor}/_revert | Revert to node version.
[**set_owner**](NODEV1Api.md#set_owner) | **POST** /node/v1/nodes/{repository}/{node}/owner | Set owner of node.
[**set_permission**](NODEV1Api.md#set_permission) | **POST** /node/v1/nodes/{repository}/{node}/permissions | Set local permissions of node.
[**set_property**](NODEV1Api.md#set_property) | **POST** /node/v1/nodes/{repository}/{node}/property | Set single property of node.
[**store_x_api_data**](NODEV1Api.md#store_x_api_data) | **POST** /node/v1/nodes/{repository}/{node}/xapi | Store xApi-Conform data for a given node
[**unlock**](NODEV1Api.md#unlock) | **GET** /node/v1/nodes/{repository}/{node}/lock/unlock | unlock node.
[**update_share**](NODEV1Api.md#update_share) | **POST** /node/v1/nodes/{repository}/{node}/shares/{shareId} | update share of a node.


# **add_aspects**
> NodeEntry add_aspects(repository, node, request_body)

Add aspect to node.

Add aspect to node.

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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node
    request_body = ['request_body_example'] # List[str] | aspect name, e.g. ccm:lomreplication

    try:
        # Add aspect to node.
        api_response = api_instance.add_aspects(repository, node, request_body)
        print("The response of NODEV1Api->add_aspects:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NODEV1Api->add_aspects: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 
 **request_body** | [**List[str]**](str.md)| aspect name, e.g. ccm:lomreplication | 

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

# **add_workflow_history**
> add_workflow_history(repository, node, workflow_history)

Add workflow.

Add workflow entry to node.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.workflow_history import WorkflowHistory
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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node
    workflow_history = edu_sharing_client.WorkflowHistory() # WorkflowHistory | The history entry to put (editor and time can be null and will be filled automatically)

    try:
        # Add workflow.
        api_instance.add_workflow_history(repository, node, workflow_history)
    except Exception as e:
        print("Exception when calling NODEV1Api->add_workflow_history: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 
 **workflow_history** | [**WorkflowHistory**](WorkflowHistory.md)| The history entry to put (editor and time can be null and will be filled automatically) | 

### Return type

void (empty response body)

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

# **change_content1**
> NodeEntry change_content1(repository, node, mimetype, version_comment=version_comment, file=file)

Change content of node.

Change content of node.

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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node
    mimetype = 'mimetype_example' # str | MIME-Type
    version_comment = 'version_comment_example' # str | comment, leave empty = no new version, otherwise new version is generated (optional)
    file = None # bytearray | file upload (optional)

    try:
        # Change content of node.
        api_response = api_instance.change_content1(repository, node, mimetype, version_comment=version_comment, file=file)
        print("The response of NODEV1Api->change_content1:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NODEV1Api->change_content1: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 
 **mimetype** | **str**| MIME-Type | 
 **version_comment** | **str**| comment, leave empty &#x3D; no new version, otherwise new version is generated | [optional] 
 **file** | **bytearray**| file upload | [optional] 

### Return type

[**NodeEntry**](NodeEntry.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
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

# **change_content_as_text**
> NodeEntry change_content_as_text(repository, node, mimetype, version_comment=version_comment)

Change content of node as text.

Change content of node as text.

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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node
    mimetype = 'mimetype_example' # str | MIME-Type
    version_comment = 'version_comment_example' # str | comment, leave empty = no new version, otherwise new version is generated (optional)

    try:
        # Change content of node as text.
        api_response = api_instance.change_content_as_text(repository, node, mimetype, version_comment=version_comment)
        print("The response of NODEV1Api->change_content_as_text:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NODEV1Api->change_content_as_text: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 
 **mimetype** | **str**| MIME-Type | 
 **version_comment** | **str**| comment, leave empty &#x3D; no new version, otherwise new version is generated | [optional] 

### Return type

[**NodeEntry**](NodeEntry.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
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

# **change_metadata**
> NodeEntry change_metadata(repository, node, request_body)

Change metadata of node.

Change metadata of node.

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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node
    request_body = None # Dict[str, List[str]] | properties

    try:
        # Change metadata of node.
        api_response = api_instance.change_metadata(repository, node, request_body)
        print("The response of NODEV1Api->change_metadata:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NODEV1Api->change_metadata: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 
 **request_body** | [**Dict[str, List[str]]**](List.md)| properties | 

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

# **change_metadata_with_versioning**
> NodeEntry change_metadata_with_versioning(repository, node, version_comment, request_body)

Change metadata of node (new version).

Change metadata of node (new version).

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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node
    version_comment = 'version_comment_example' # str | comment
    request_body = None # Dict[str, List[str]] | properties

    try:
        # Change metadata of node (new version).
        api_response = api_instance.change_metadata_with_versioning(repository, node, version_comment, request_body)
        print("The response of NODEV1Api->change_metadata_with_versioning:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NODEV1Api->change_metadata_with_versioning: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 
 **version_comment** | **str**| comment | 
 **request_body** | [**Dict[str, List[str]]**](List.md)| properties | 

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

# **change_preview**
> NodeEntry change_preview(repository, node, mimetype, create_version=create_version, image=image)

Change preview of node.

Change preview of node.

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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node
    mimetype = 'mimetype_example' # str | MIME-Type
    create_version = True # bool | create a node version (optional) (default to True)
    image = None # object |  (optional)

    try:
        # Change preview of node.
        api_response = api_instance.change_preview(repository, node, mimetype, create_version=create_version, image=image)
        print("The response of NODEV1Api->change_preview:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NODEV1Api->change_preview: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 
 **mimetype** | **str**| MIME-Type | 
 **create_version** | **bool**| create a node version | [optional] [default to True]
 **image** | [**object**](object.md)|  | [optional] 

### Return type

[**NodeEntry**](NodeEntry.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: multipart/form-data
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

# **change_template_metadata**
> NodeEntry change_template_metadata(repository, node, enable, request_body)

Set the metadata template for this folder.

All the given metadata will be inherited to child nodes.

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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node
    enable = True # bool | Is the inherition currently enabled
    request_body = None # Dict[str, List[str]] | properties

    try:
        # Set the metadata template for this folder.
        api_response = api_instance.change_template_metadata(repository, node, enable, request_body)
        print("The response of NODEV1Api->change_template_metadata:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NODEV1Api->change_template_metadata: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 
 **enable** | **bool**| Is the inherition currently enabled | 
 **request_body** | [**Dict[str, List[str]]**](List.md)| properties | 

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

# **copy_metadata**
> NodeEntry copy_metadata(repository, node, var_from)

Copy metadata from another node.

Copies all common metadata from one note to another. Current user needs write access to the target node and read access to the source node.

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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node
    var_from = 'var_from_example' # str | The node where to copy the metadata from

    try:
        # Copy metadata from another node.
        api_response = api_instance.copy_metadata(repository, node, var_from)
        print("The response of NODEV1Api->copy_metadata:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NODEV1Api->copy_metadata: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 
 **var_from** | **str**| The node where to copy the metadata from | 

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
**409** | Duplicate Entity/Node conflict (Node with same name exists) |  -  |
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_child**
> NodeEntry create_child(repository, node, type, request_body, aspects=aspects, rename_if_exists=rename_if_exists, version_comment=version_comment, assoc_type=assoc_type)

Create a new child.

Create a new child.

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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of parent node use -userhome- for userhome or -inbox- for inbox node
    type = 'type_example' # str | type of node
    request_body = None # Dict[str, List[str]] | properties, example: {\"{http://www.alfresco.org/model/content/1.0}name\": [\"test\"]}
    aspects = ['aspects_example'] # List[str] | aspects of node (optional)
    rename_if_exists = False # bool | rename if the same node name exists (optional) (default to False)
    version_comment = 'version_comment_example' # str | comment, leave empty = no inital version (optional)
    assoc_type = 'assoc_type_example' # str | Association type, can be empty (optional)

    try:
        # Create a new child.
        api_response = api_instance.create_child(repository, node, type, request_body, aspects=aspects, rename_if_exists=rename_if_exists, version_comment=version_comment, assoc_type=assoc_type)
        print("The response of NODEV1Api->create_child:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NODEV1Api->create_child: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of parent node use -userhome- for userhome or -inbox- for inbox node | 
 **type** | **str**| type of node | 
 **request_body** | [**Dict[str, List[str]]**](List.md)| properties, example: {\&quot;{http://www.alfresco.org/model/content/1.0}name\&quot;: [\&quot;test\&quot;]} | 
 **aspects** | [**List[str]**](str.md)| aspects of node | [optional] 
 **rename_if_exists** | **bool**| rename if the same node name exists | [optional] [default to False]
 **version_comment** | **str**| comment, leave empty &#x3D; no inital version | [optional] 
 **assoc_type** | **str**| Association type, can be empty | [optional] 

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

# **create_child_by_copying**
> NodeEntry create_child_by_copying(repository, node, source, with_children)

Create a new child by copying.

Create a new child by copying.

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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of parent node
    source = 'source_example' # str | ID of source node
    with_children = True # bool | flag for children

    try:
        # Create a new child by copying.
        api_response = api_instance.create_child_by_copying(repository, node, source, with_children)
        print("The response of NODEV1Api->create_child_by_copying:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NODEV1Api->create_child_by_copying: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of parent node | 
 **source** | **str**| ID of source node | 
 **with_children** | **bool**| flag for children | 

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
**409** | Duplicate Entity/Node conflict (Node with same name exists) |  -  |
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_child_by_moving**
> NodeEntry create_child_by_moving(repository, node, source)

Create a new child by moving.

Create a new child by moving.

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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of parent node
    source = 'source_example' # str | ID of source node

    try:
        # Create a new child by moving.
        api_response = api_instance.create_child_by_moving(repository, node, source)
        print("The response of NODEV1Api->create_child_by_moving:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NODEV1Api->create_child_by_moving: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of parent node | 
 **source** | **str**| ID of source node | 

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
**409** | Duplicate Entity/Node conflict (Node with same name exists) |  -  |
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_fork_of_node**
> NodeEntry create_fork_of_node(repository, node, source, with_children)

Create a copy of a node by creating a forked version (variant).

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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of parent node
    source = 'source_example' # str | ID of source node
    with_children = True # bool | flag for children

    try:
        # Create a copy of a node by creating a forked version (variant).
        api_response = api_instance.create_fork_of_node(repository, node, source, with_children)
        print("The response of NODEV1Api->create_fork_of_node:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NODEV1Api->create_fork_of_node: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of parent node | 
 **source** | **str**| ID of source node | 
 **with_children** | **bool**| flag for children | 

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
**409** | Duplicate Entity/Node conflict (Node with same name exists) |  -  |
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_share**
> NodeShare create_share(repository, node, expiry_date=expiry_date, password=password)

Create a share for a node.

Create a new share for a node

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.node_share import NodeShare
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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node
    expiry_date = -1 # int | expiry date for this share, leave empty or -1 for unlimited (optional) (default to -1)
    password = 'password_example' # str | password for this share, use none to not use a password (optional)

    try:
        # Create a share for a node.
        api_response = api_instance.create_share(repository, node, expiry_date=expiry_date, password=password)
        print("The response of NODEV1Api->create_share:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NODEV1Api->create_share: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 
 **expiry_date** | **int**| expiry date for this share, leave empty or -1 for unlimited | [optional] [default to -1]
 **password** | **str**| password for this share, use none to not use a password | [optional] 

### Return type

[**NodeShare**](NodeShare.md)

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

# **delete**
> delete(repository, node, recycle=recycle, protocol=protocol, store=store)

Delete node.

Delete node.

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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node
    recycle = True # bool | move the node to recycle (optional) (default to True)
    protocol = 'protocol_example' # str | protocol (optional)
    store = 'store_example' # str | store (optional)

    try:
        # Delete node.
        api_instance.delete(repository, node, recycle=recycle, protocol=protocol, store=store)
    except Exception as e:
        print("Exception when calling NODEV1Api->delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 
 **recycle** | **bool**| move the node to recycle | [optional] [default to True]
 **protocol** | **str**| protocol | [optional] 
 **store** | **str**| store | [optional] 

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

# **delete_preview**
> NodeEntry delete_preview(repository, node)

Delete preview of node.

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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node

    try:
        # Delete preview of node.
        api_response = api_instance.delete_preview(repository, node)
        print("The response of NODEV1Api->delete_preview:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NODEV1Api->delete_preview: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 

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

# **get_assocs**
> NodeEntries get_assocs(repository, node, direction, max_items=max_items, skip_count=skip_count, sort_properties=sort_properties, sort_ascending=sort_ascending, assoc_name=assoc_name, property_filter=property_filter)

Get related nodes.

Get nodes related based on an assoc.

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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node
    direction = 'direction_example' # str | Either where the given node should be the \"SOURCE\" or the \"TARGET\"
    max_items = 500 # int | maximum items per page (optional) (default to 500)
    skip_count = 0 # int | skip a number of items (optional) (default to 0)
    sort_properties = ['sort_properties_example'] # List[str] | sort properties (optional)
    sort_ascending = [True] # List[bool] | sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index (optional)
    assoc_name = 'assoc_name_example' # str | Association name (e.g. ccm:forkio). (optional)
    property_filter = ['property_filter_example'] # List[str] | property filter for result nodes (or \"-all-\" for all properties) (optional)

    try:
        # Get related nodes.
        api_response = api_instance.get_assocs(repository, node, direction, max_items=max_items, skip_count=skip_count, sort_properties=sort_properties, sort_ascending=sort_ascending, assoc_name=assoc_name, property_filter=property_filter)
        print("The response of NODEV1Api->get_assocs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NODEV1Api->get_assocs: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 
 **direction** | **str**| Either where the given node should be the \&quot;SOURCE\&quot; or the \&quot;TARGET\&quot; | 
 **max_items** | **int**| maximum items per page | [optional] [default to 500]
 **skip_count** | **int**| skip a number of items | [optional] [default to 0]
 **sort_properties** | [**List[str]**](str.md)| sort properties | [optional] 
 **sort_ascending** | [**List[bool]**](bool.md)| sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index | [optional] 
 **assoc_name** | **str**| Association name (e.g. ccm:forkio). | [optional] 
 **property_filter** | [**List[str]**](str.md)| property filter for result nodes (or \&quot;-all-\&quot; for all properties) | [optional] 

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

# **get_children**
> NodeEntries get_children(repository, node, max_items=max_items, skip_count=skip_count, filter=filter, sort_properties=sort_properties, sort_ascending=sort_ascending, assoc_name=assoc_name, property_filter=property_filter)

Get children of node.

Get children of node.

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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of parent node (or \"-userhome-\" for home directory of current user, \"-shared_files-\" for shared folders, \"-to_me_shared_files\" for shared files for the user,\"-my_shared_files-\" for files shared by the user, \"-inbox-\" for the inbox, \"-workflow_receive-\" for files assigned by workflow, \"-saved_search-\" for saved searches of the user)
    max_items = 500 # int | maximum items per page (optional) (default to 500)
    skip_count = 0 # int | skip a number of items (optional) (default to 0)
    filter = ['filter_example'] # List[str] | filter by type files,folders (optional)
    sort_properties = ['sort_properties_example'] # List[str] | sort properties (optional)
    sort_ascending = [True] # List[bool] | sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index (optional)
    assoc_name = 'assoc_name_example' # str | Filter for a specific association. May be empty (optional)
    property_filter = ['property_filter_example'] # List[str] | property filter for result nodes (or \"-all-\" for all properties) (optional)

    try:
        # Get children of node.
        api_response = api_instance.get_children(repository, node, max_items=max_items, skip_count=skip_count, filter=filter, sort_properties=sort_properties, sort_ascending=sort_ascending, assoc_name=assoc_name, property_filter=property_filter)
        print("The response of NODEV1Api->get_children:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NODEV1Api->get_children: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of parent node (or \&quot;-userhome-\&quot; for home directory of current user, \&quot;-shared_files-\&quot; for shared folders, \&quot;-to_me_shared_files\&quot; for shared files for the user,\&quot;-my_shared_files-\&quot; for files shared by the user, \&quot;-inbox-\&quot; for the inbox, \&quot;-workflow_receive-\&quot; for files assigned by workflow, \&quot;-saved_search-\&quot; for saved searches of the user) | 
 **max_items** | **int**| maximum items per page | [optional] [default to 500]
 **skip_count** | **int**| skip a number of items | [optional] [default to 0]
 **filter** | [**List[str]**](str.md)| filter by type files,folders | [optional] 
 **sort_properties** | [**List[str]**](str.md)| sort properties | [optional] 
 **sort_ascending** | [**List[bool]**](bool.md)| sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index | [optional] 
 **assoc_name** | **str**| Filter for a specific association. May be empty | [optional] 
 **property_filter** | [**List[str]**](str.md)| property filter for result nodes (or \&quot;-all-\&quot; for all properties) | [optional] 

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

# **get_lrmi_data**
> JSONObject get_lrmi_data(repository, node, version=version)

Get lrmi data.

Get lrmi data of node.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.json_object import JSONObject
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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node
    version = 'version_example' # str | Version of the node (optional)

    try:
        # Get lrmi data.
        api_response = api_instance.get_lrmi_data(repository, node, version=version)
        print("The response of NODEV1Api->get_lrmi_data:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NODEV1Api->get_lrmi_data: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 
 **version** | **str**| Version of the node | [optional] 

### Return type

[**JSONObject**](JSONObject.md)

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

# **get_metadata**
> NodeEntry get_metadata(repository, node, property_filter=property_filter)

Get metadata of node.

Get metadata of node.

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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node
    property_filter = ['property_filter_example'] # List[str] | property filter for result nodes (or \"-all-\" for all properties) (optional)

    try:
        # Get metadata of node.
        api_response = api_instance.get_metadata(repository, node, property_filter=property_filter)
        print("The response of NODEV1Api->get_metadata:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NODEV1Api->get_metadata: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 
 **property_filter** | [**List[str]**](str.md)| property filter for result nodes (or \&quot;-all-\&quot; for all properties) | [optional] 

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

# **get_nodes**
> SearchResult get_nodes(repository, query, facets=facets, max_items=max_items, skip_count=skip_count, sort_properties=sort_properties, sort_ascending=sort_ascending, property_filter=property_filter)

Searching nodes.

Searching nodes.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.search_result import SearchResult
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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    query = 'query_example' # str | lucene query
    facets = ['facets_example'] # List[str] | facets (optional)
    max_items = 10 # int | maximum items per page (optional) (default to 10)
    skip_count = 0 # int | skip a number of items (optional) (default to 0)
    sort_properties = ['sort_properties_example'] # List[str] | sort properties (optional)
    sort_ascending = [True] # List[bool] | sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index (optional)
    property_filter = ['property_filter_example'] # List[str] | property filter for result nodes (or \"-all-\" for all properties) (optional)

    try:
        # Searching nodes.
        api_response = api_instance.get_nodes(repository, query, facets=facets, max_items=max_items, skip_count=skip_count, sort_properties=sort_properties, sort_ascending=sort_ascending, property_filter=property_filter)
        print("The response of NODEV1Api->get_nodes:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NODEV1Api->get_nodes: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **query** | **str**| lucene query | 
 **facets** | [**List[str]**](str.md)| facets | [optional] 
 **max_items** | **int**| maximum items per page | [optional] [default to 10]
 **skip_count** | **int**| skip a number of items | [optional] [default to 0]
 **sort_properties** | [**List[str]**](str.md)| sort properties | [optional] 
 **sort_ascending** | [**List[bool]**](bool.md)| sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index | [optional] 
 **property_filter** | [**List[str]**](str.md)| property filter for result nodes (or \&quot;-all-\&quot; for all properties) | [optional] 

### Return type

[**SearchResult**](SearchResult.md)

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

# **get_notify_list**
> str get_notify_list(repository, node)

Get notifys (sharing history) of the node.

Ordered by the time of each notify

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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node

    try:
        # Get notifys (sharing history) of the node.
        api_response = api_instance.get_notify_list(repository, node)
        print("The response of NODEV1Api->get_notify_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NODEV1Api->get_notify_list: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 

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

# **get_parents**
> ParentEntries get_parents(repository, node, property_filter=property_filter, full_path=full_path)

Get parents of node.

Get all parents metadata + own metadata of node. Index 0 is always the current node

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.parent_entries import ParentEntries
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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node
    property_filter = ['property_filter_example'] # List[str] | property filter for result nodes (or \"-all-\" for all properties) (optional)
    full_path = True # bool | activate to return the full alfresco path, otherwise the path for the user home is resolved (optional)

    try:
        # Get parents of node.
        api_response = api_instance.get_parents(repository, node, property_filter=property_filter, full_path=full_path)
        print("The response of NODEV1Api->get_parents:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NODEV1Api->get_parents: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 
 **property_filter** | [**List[str]**](str.md)| property filter for result nodes (or \&quot;-all-\&quot; for all properties) | [optional] 
 **full_path** | **bool**| activate to return the full alfresco path, otherwise the path for the user home is resolved | [optional] 

### Return type

[**ParentEntries**](ParentEntries.md)

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

# **get_permission**
> NodePermissionEntry get_permission(repository, node)

Get all permission of node.

Get all permission of node.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.node_permission_entry import NodePermissionEntry
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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node

    try:
        # Get all permission of node.
        api_response = api_instance.get_permission(repository, node)
        print("The response of NODEV1Api->get_permission:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NODEV1Api->get_permission: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 

### Return type

[**NodePermissionEntry**](NodePermissionEntry.md)

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

# **get_published_copies**
> NodeEntries get_published_copies(repository, node)

Publish

Get all published copies of the current node

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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node

    try:
        # Publish
        api_response = api_instance.get_published_copies(repository, node)
        print("The response of NODEV1Api->get_published_copies:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NODEV1Api->get_published_copies: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 

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

# **get_shares**
> str get_shares(repository, node, email=email)

Get shares of node.

Get list of shares (via mail/token) for a node.

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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node
    email = 'email_example' # str | Filter for a specific email or use LINK for link shares (Optional) (optional)

    try:
        # Get shares of node.
        api_response = api_instance.get_shares(repository, node, email=email)
        print("The response of NODEV1Api->get_shares:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NODEV1Api->get_shares: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 
 **email** | **str**| Filter for a specific email or use LINK for link shares (Optional) | [optional] 

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

# **get_stats**
> NodeStats get_stats(repository, node)

Get statistics of node.

Get statistics (views, downloads) of node. Requires ChangePermissions permission on node

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.node_stats import NodeStats
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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node

    try:
        # Get statistics of node.
        api_response = api_instance.get_stats(repository, node)
        print("The response of NODEV1Api->get_stats:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NODEV1Api->get_stats: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 

### Return type

[**NodeStats**](NodeStats.md)

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

# **get_template_metadata**
> NodeEntry get_template_metadata(repository, node)

Get the metadata template + status for this folder.

All the given metadata will be inherited to child nodes.

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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node

    try:
        # Get the metadata template + status for this folder.
        api_response = api_instance.get_template_metadata(repository, node)
        print("The response of NODEV1Api->get_template_metadata:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NODEV1Api->get_template_metadata: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 

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
**409** | Duplicate Entity/Node conflict (Node with same name exists) |  -  |
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_text_content**
> NodeText get_text_content(repository, node)

Get the text content of a document.

May fails with 500 if the node can not be read.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.node_text import NodeText
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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node

    try:
        # Get the text content of a document.
        api_response = api_instance.get_text_content(repository, node)
        print("The response of NODEV1Api->get_text_content:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NODEV1Api->get_text_content: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 

### Return type

[**NodeText**](NodeText.md)

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

# **get_version_metadata**
> NodeVersionEntry get_version_metadata(repository, node, major, minor, property_filter=property_filter)

Get metadata of node version.

Get metadata of node version.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.node_version_entry import NodeVersionEntry
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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node
    major = 56 # int | major version
    minor = 56 # int | minor version
    property_filter = ['property_filter_example'] # List[str] | property filter for result nodes (or \"-all-\" for all properties) (optional)

    try:
        # Get metadata of node version.
        api_response = api_instance.get_version_metadata(repository, node, major, minor, property_filter=property_filter)
        print("The response of NODEV1Api->get_version_metadata:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NODEV1Api->get_version_metadata: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 
 **major** | **int**| major version | 
 **minor** | **int**| minor version | 
 **property_filter** | [**List[str]**](str.md)| property filter for result nodes (or \&quot;-all-\&quot; for all properties) | [optional] 

### Return type

[**NodeVersionEntry**](NodeVersionEntry.md)

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

# **get_versions**
> NodeVersionRefEntries get_versions(repository, node)

Get all versions of node.

Get all versions of node.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.node_version_ref_entries import NodeVersionRefEntries
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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node

    try:
        # Get all versions of node.
        api_response = api_instance.get_versions(repository, node)
        print("The response of NODEV1Api->get_versions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NODEV1Api->get_versions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 

### Return type

[**NodeVersionRefEntries**](NodeVersionRefEntries.md)

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

# **get_versions1**
> NodeVersionEntries get_versions1(repository, node, property_filter=property_filter)

Get all versions of node, including it's metadata.

Get all versions of node, including it's metadata.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.node_version_entries import NodeVersionEntries
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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node
    property_filter = ['property_filter_example'] # List[str] | property filter for result nodes (or \"-all-\" for all properties) (optional)

    try:
        # Get all versions of node, including it's metadata.
        api_response = api_instance.get_versions1(repository, node, property_filter=property_filter)
        print("The response of NODEV1Api->get_versions1:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NODEV1Api->get_versions1: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 
 **property_filter** | [**List[str]**](str.md)| property filter for result nodes (or \&quot;-all-\&quot; for all properties) | [optional] 

### Return type

[**NodeVersionEntries**](NodeVersionEntries.md)

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

# **get_workflow_history**
> str get_workflow_history(repository, node)

Get workflow history.

Get workflow history of node.

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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node

    try:
        # Get workflow history.
        api_response = api_instance.get_workflow_history(repository, node)
        print("The response of NODEV1Api->get_workflow_history:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NODEV1Api->get_workflow_history: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 

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

# **has_permission**
> str has_permission(repository, node, user)

Which permissions has user/group for node.

Check for actual permissions (also when user is in groups) for a specific node

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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node
    user = 'user_example' # str | Authority (user/group) to check (use \"-me-\" for current user

    try:
        # Which permissions has user/group for node.
        api_response = api_instance.has_permission(repository, node, user)
        print("The response of NODEV1Api->has_permission:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NODEV1Api->has_permission: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 
 **user** | **str**| Authority (user/group) to check (use \&quot;-me-\&quot; for current user | 

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

# **import_node**
> NodeEntry import_node(repository, node, parent)

Import node

Import a node from a foreign repository to the local repository.

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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = 'repository_example' # str | The id of the foreign repository
    node = 'node_example' # str | ID of node
    parent = 'parent_example' # str | Parent node where to store it locally, may also use -userhome- or -inbox-

    try:
        # Import node
        api_response = api_instance.import_node(repository, node, parent)
        print("The response of NODEV1Api->import_node:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NODEV1Api->import_node: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| The id of the foreign repository | 
 **node** | **str**| ID of node | 
 **parent** | **str**| Parent node where to store it locally, may also use -userhome- or -inbox- | 

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

# **islocked**
> NodeLocked islocked(repository, node)

locked status of a node.

locked status of a node.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.node_locked import NodeLocked
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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node

    try:
        # locked status of a node.
        api_response = api_instance.islocked(repository, node)
        print("The response of NODEV1Api->islocked:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NODEV1Api->islocked: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 

### Return type

[**NodeLocked**](NodeLocked.md)

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

# **prepare_usage**
> NodeRemote prepare_usage(repository, node)

create remote object and get properties.

create remote object and get properties.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.node_remote import NodeRemote
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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node

    try:
        # create remote object and get properties.
        api_response = api_instance.prepare_usage(repository, node)
        print("The response of NODEV1Api->prepare_usage:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NODEV1Api->prepare_usage: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 

### Return type

[**NodeRemote**](NodeRemote.md)

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

# **publish_copy**
> NodeEntry publish_copy(repository, node, handle_mode=handle_mode, handle_param=handle_param)

Publish

Create a published copy of the current node 

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.handle_param import HandleParam
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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node
    handle_mode = 'handle_mode_example' # str | handle mode, if a handle should be created. Skip this parameter if you don't want an handle (optional)
    handle_param = edu_sharing_client.HandleParam() # HandleParam | handle parameter, if a handle and/or doi should be created. Skip this parameter if you don't want a handle or doi, (optional)

    try:
        # Publish
        api_response = api_instance.publish_copy(repository, node, handle_mode=handle_mode, handle_param=handle_param)
        print("The response of NODEV1Api->publish_copy:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NODEV1Api->publish_copy: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 
 **handle_mode** | **str**| handle mode, if a handle should be created. Skip this parameter if you don&#39;t want an handle | [optional] 
 **handle_param** | [**HandleParam**](HandleParam.md)| handle parameter, if a handle and/or doi should be created. Skip this parameter if you don&#39;t want a handle or doi, | [optional] 

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

# **remove_share**
> remove_share(repository, node, share_id)

Remove share of a node.

Remove the specified share id

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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node
    share_id = 'share_id_example' # str | share id

    try:
        # Remove share of a node.
        api_instance.remove_share(repository, node, share_id)
    except Exception as e:
        print("Exception when calling NODEV1Api->remove_share: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 
 **share_id** | **str**| share id | 

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

# **report_node**
> report_node(repository, node, reason, user_email, user_comment=user_comment)

Report the node.

Report a node to notify the admin about an issue)

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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node
    reason = 'reason_example' # str | the reason for the report
    user_email = 'user_email_example' # str | mail of reporting user
    user_comment = 'user_comment_example' # str | additional user comment (optional)

    try:
        # Report the node.
        api_instance.report_node(repository, node, reason, user_email, user_comment=user_comment)
    except Exception as e:
        print("Exception when calling NODEV1Api->report_node: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 
 **reason** | **str**| the reason for the report | 
 **user_email** | **str**| mail of reporting user | 
 **user_comment** | **str**| additional user comment | [optional] 

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

# **revert_version**
> NodeEntry revert_version(repository, node, major, minor)

Revert to node version.

Revert to node version.

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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node
    major = 56 # int | major version
    minor = 56 # int | minor version

    try:
        # Revert to node version.
        api_response = api_instance.revert_version(repository, node, major, minor)
        print("The response of NODEV1Api->revert_version:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NODEV1Api->revert_version: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 
 **major** | **int**| major version | 
 **minor** | **int**| minor version | 

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

# **set_owner**
> set_owner(repository, node, username=username)

Set owner of node.

Set owner of node.

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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node
    username = 'username_example' # str | username (optional)

    try:
        # Set owner of node.
        api_instance.set_owner(repository, node, username=username)
    except Exception as e:
        print("Exception when calling NODEV1Api->set_owner: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 
 **username** | **str**| username | [optional] 

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

# **set_permission**
> set_permission(repository, node, send_mail, send_copy, acl, mailtext=mailtext)

Set local permissions of node.

Set local permissions of node.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.acl import ACL
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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node
    send_mail = True # bool | sendMail
    send_copy = True # bool | sendCopy
    acl = edu_sharing_client.ACL() # ACL | permissions
    mailtext = 'mailtext_example' # str | mailtext (optional)

    try:
        # Set local permissions of node.
        api_instance.set_permission(repository, node, send_mail, send_copy, acl, mailtext=mailtext)
    except Exception as e:
        print("Exception when calling NODEV1Api->set_permission: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 
 **send_mail** | **bool**| sendMail | 
 **send_copy** | **bool**| sendCopy | 
 **acl** | [**ACL**](ACL.md)| permissions | 
 **mailtext** | **str**| mailtext | [optional] 

### Return type

void (empty response body)

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

# **set_property**
> set_property(repository, node, var_property, keep_modified_date=keep_modified_date, value=value)

Set single property of node.

When the property is unset (null), it will be removed

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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node
    var_property = 'var_property_example' # str | property
    keep_modified_date = False # bool | keepModifiedDate (optional) (default to False)
    value = ['value_example'] # List[str] | value (optional)

    try:
        # Set single property of node.
        api_instance.set_property(repository, node, var_property, keep_modified_date=keep_modified_date, value=value)
    except Exception as e:
        print("Exception when calling NODEV1Api->set_property: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 
 **var_property** | **str**| property | 
 **keep_modified_date** | **bool**| keepModifiedDate | [optional] [default to False]
 **value** | [**List[str]**](str.md)| value | [optional] 

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

# **store_x_api_data**
> object store_x_api_data(repository, node, body)

Store xApi-Conform data for a given node

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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node
    body = 'body_example' # str | xApi conform json data

    try:
        # Store xApi-Conform data for a given node
        api_response = api_instance.store_x_api_data(repository, node, body)
        print("The response of NODEV1Api->store_x_api_data:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NODEV1Api->store_x_api_data: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 
 **body** | **str**| xApi conform json data | 

### Return type

**object**

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

# **unlock**
> unlock(repository, node)

unlock node.

unlock node.

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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node

    try:
        # unlock node.
        api_instance.unlock(repository, node)
    except Exception as e:
        print("Exception when calling NODEV1Api->unlock: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 

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

# **update_share**
> NodeShare update_share(repository, node, share_id, expiry_date=expiry_date, password=password)

update share of a node.

update the specified share id

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.node_share import NodeShare
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
    api_instance = edu_sharing_client.NODEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node
    share_id = 'share_id_example' # str | share id
    expiry_date = -1 # int | expiry date for this share, leave empty or -1 for unlimited (optional) (default to -1)
    password = 'password_example' # str | new password for share, leave empty if you don't want to change it (optional)

    try:
        # update share of a node.
        api_response = api_instance.update_share(repository, node, share_id, expiry_date=expiry_date, password=password)
        print("The response of NODEV1Api->update_share:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NODEV1Api->update_share: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 
 **share_id** | **str**| share id | 
 **expiry_date** | **int**| expiry date for this share, leave empty or -1 for unlimited | [optional] [default to -1]
 **password** | **str**| new password for share, leave empty if you don&#39;t want to change it | [optional] 

### Return type

[**NodeShare**](NodeShare.md)

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

