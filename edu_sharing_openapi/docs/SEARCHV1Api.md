# edu_sharing_client.SEARCHV1Api

All URIs are relative to *https://stable.demo.edu-sharing.net/edu-sharing/rest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_metdata**](SEARCHV1Api.md#get_metdata) | **GET** /search/v1/metadata/{repository} | get nodes with metadata and collections
[**get_relevant_nodes**](SEARCHV1Api.md#get_relevant_nodes) | **GET** /search/v1/relevant/{repository} | Get relevant nodes for the current user
[**load_save_search**](SEARCHV1Api.md#load_save_search) | **GET** /search/v1/queries/load/{nodeId} | Load a saved search query.
[**save_search**](SEARCHV1Api.md#save_search) | **POST** /search/v1/queries/{repository}/{metadataset}/{query}/save | Save a search query.
[**search**](SEARCHV1Api.md#search) | **POST** /search/v1/queries/{repository}/{metadataset}/{query} | Perform queries based on metadata sets.
[**search_by_property**](SEARCHV1Api.md#search_by_property) | **GET** /search/v1/custom/{repository} | Search for custom properties with custom values
[**search_contributor**](SEARCHV1Api.md#search_contributor) | **GET** /search/v1/queries/{repository}/contributor | Search for contributors
[**search_facets**](SEARCHV1Api.md#search_facets) | **POST** /search/v1/queries/{repository}/{metadataset}/{query}/facets | Search in facets.
[**search_fingerprint**](SEARCHV1Api.md#search_fingerprint) | **POST** /search/v1/queries/{repository}/fingerprint/{nodeid} | Perform queries based on metadata sets.
[**search_lrmi**](SEARCHV1Api.md#search_lrmi) | **POST** /search/v1/queries/{repository}/{metadataset}/{query}/lrmi | Perform queries based on metadata sets.


# **get_metdata**
> NodeEntries get_metdata(repository, node_ids=node_ids, property_filter=property_filter)

get nodes with metadata and collections

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
    api_instance = edu_sharing_client.SEARCHV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node_ids = ['node_ids_example'] # List[str] | nodeIds (optional)
    property_filter = ['property_filter_example'] # List[str] | property filter for result nodes (or \"-all-\" for all properties) (optional)

    try:
        # get nodes with metadata and collections
        api_response = api_instance.get_metdata(repository, node_ids=node_ids, property_filter=property_filter)
        print("The response of SEARCHV1Api->get_metdata:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SEARCHV1Api->get_metdata: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node_ids** | [**List[str]**](str.md)| nodeIds | [optional] 
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

# **get_relevant_nodes**
> SearchResultNode get_relevant_nodes(repository, property_filter=property_filter, max_items=max_items, skip_count=skip_count)

Get relevant nodes for the current user

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.search_result_node import SearchResultNode
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
    api_instance = edu_sharing_client.SEARCHV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    property_filter = ['property_filter_example'] # List[str] | property filter for result nodes (or \"-all-\" for all properties) (optional)
    max_items = 10 # int | maximum items per page (optional) (default to 10)
    skip_count = 0 # int | skip a number of items (optional) (default to 0)

    try:
        # Get relevant nodes for the current user
        api_response = api_instance.get_relevant_nodes(repository, property_filter=property_filter, max_items=max_items, skip_count=skip_count)
        print("The response of SEARCHV1Api->get_relevant_nodes:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SEARCHV1Api->get_relevant_nodes: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **property_filter** | [**List[str]**](str.md)| property filter for result nodes (or \&quot;-all-\&quot; for all properties) | [optional] 
 **max_items** | **int**| maximum items per page | [optional] [default to 10]
 **skip_count** | **int**| skip a number of items | [optional] [default to 0]

### Return type

[**SearchResultNode**](SearchResultNode.md)

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

# **load_save_search**
> Node load_save_search(node_id, content_type=content_type, max_items=max_items, skip_count=skip_count, sort_properties=sort_properties, sort_ascending=sort_ascending, property_filter=property_filter, request_body=request_body)

Load a saved search query.

Load a saved search query.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.node import Node
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
    api_instance = edu_sharing_client.SEARCHV1Api(api_client)
    node_id = 'node_id_example' # str | Node id of the search item
    content_type = 'content_type_example' # str | Type of element (optional)
    max_items = 10 # int | maximum items per page (optional) (default to 10)
    skip_count = 0 # int | skip a number of items (optional) (default to 0)
    sort_properties = ['sort_properties_example'] # List[str] | sort properties (optional)
    sort_ascending = [True] # List[bool] | sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index (optional)
    property_filter = ['property_filter_example'] # List[str] | property filter for result nodes (or \"-all-\" for all properties) (optional)
    request_body = ['request_body_example'] # List[str] | facets (optional)

    try:
        # Load a saved search query.
        api_response = api_instance.load_save_search(node_id, content_type=content_type, max_items=max_items, skip_count=skip_count, sort_properties=sort_properties, sort_ascending=sort_ascending, property_filter=property_filter, request_body=request_body)
        print("The response of SEARCHV1Api->load_save_search:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SEARCHV1Api->load_save_search: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **node_id** | **str**| Node id of the search item | 
 **content_type** | **str**| Type of element | [optional] 
 **max_items** | **int**| maximum items per page | [optional] [default to 10]
 **skip_count** | **int**| skip a number of items | [optional] [default to 0]
 **sort_properties** | [**List[str]**](str.md)| sort properties | [optional] 
 **sort_ascending** | [**List[bool]**](bool.md)| sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index | [optional] 
 **property_filter** | [**List[str]**](str.md)| property filter for result nodes (or \&quot;-all-\&quot; for all properties) | [optional] 
 **request_body** | [**List[str]**](str.md)| facets | [optional] 

### Return type

[**Node**](Node.md)

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

# **save_search**
> NodeEntry save_search(repository, metadataset, query, name, mds_query_criteria, replace=replace)

Save a search query.

Save a search query.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.mds_query_criteria import MdsQueryCriteria
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
    api_instance = edu_sharing_client.SEARCHV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    metadataset = '-default-' # str | ID of metadataset (or \"-default-\" for default metadata set) (default to '-default-')
    query = 'query_example' # str | ID of query
    name = 'name_example' # str | Name of the new search item
    mds_query_criteria = [edu_sharing_client.MdsQueryCriteria()] # List[MdsQueryCriteria] | search parameters
    replace = False # bool | Replace if search with the same name exists (optional) (default to False)

    try:
        # Save a search query.
        api_response = api_instance.save_search(repository, metadataset, query, name, mds_query_criteria, replace=replace)
        print("The response of SEARCHV1Api->save_search:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SEARCHV1Api->save_search: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **metadataset** | **str**| ID of metadataset (or \&quot;-default-\&quot; for default metadata set) | [default to &#39;-default-&#39;]
 **query** | **str**| ID of query | 
 **name** | **str**| Name of the new search item | 
 **mds_query_criteria** | [**List[MdsQueryCriteria]**](MdsQueryCriteria.md)| search parameters | 
 **replace** | **bool**| Replace if search with the same name exists | [optional] [default to False]

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

# **search**
> SearchResultNode search(repository, metadataset, query, search_parameters, content_type=content_type, max_items=max_items, skip_count=skip_count, sort_properties=sort_properties, sort_ascending=sort_ascending, property_filter=property_filter)

Perform queries based on metadata sets.

Perform queries based on metadata sets.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.search_parameters import SearchParameters
from edu_sharing_client.models.search_result_node import SearchResultNode
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
    api_instance = edu_sharing_client.SEARCHV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    metadataset = '-default-' # str | ID of metadataset (or \"-default-\" for default metadata set) (default to '-default-')
    query = 'query_example' # str | ID of query
    search_parameters = edu_sharing_client.SearchParameters() # SearchParameters | search parameters
    content_type = 'content_type_example' # str | Type of element (optional)
    max_items = 10 # int | maximum items per page (optional) (default to 10)
    skip_count = 0 # int | skip a number of items (optional) (default to 0)
    sort_properties = ['sort_properties_example'] # List[str] | sort properties (optional)
    sort_ascending = [True] # List[bool] | sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index (optional)
    property_filter = ['property_filter_example'] # List[str] | property filter for result nodes (or \"-all-\" for all properties) (optional)

    try:
        # Perform queries based on metadata sets.
        api_response = api_instance.search(repository, metadataset, query, search_parameters, content_type=content_type, max_items=max_items, skip_count=skip_count, sort_properties=sort_properties, sort_ascending=sort_ascending, property_filter=property_filter)
        print("The response of SEARCHV1Api->search:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SEARCHV1Api->search: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **metadataset** | **str**| ID of metadataset (or \&quot;-default-\&quot; for default metadata set) | [default to &#39;-default-&#39;]
 **query** | **str**| ID of query | 
 **search_parameters** | [**SearchParameters**](SearchParameters.md)| search parameters | 
 **content_type** | **str**| Type of element | [optional] 
 **max_items** | **int**| maximum items per page | [optional] [default to 10]
 **skip_count** | **int**| skip a number of items | [optional] [default to 0]
 **sort_properties** | [**List[str]**](str.md)| sort properties | [optional] 
 **sort_ascending** | [**List[bool]**](bool.md)| sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index | [optional] 
 **property_filter** | [**List[str]**](str.md)| property filter for result nodes (or \&quot;-all-\&quot; for all properties) | [optional] 

### Return type

[**SearchResultNode**](SearchResultNode.md)

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

# **search_by_property**
> SearchResultNode search_by_property(repository, content_type=content_type, combine_mode=combine_mode, var_property=var_property, value=value, comparator=comparator, max_items=max_items, skip_count=skip_count, sort_properties=sort_properties, sort_ascending=sort_ascending, property_filter=property_filter)

Search for custom properties with custom values

e.g. property=cm:name, value:*Test*

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.search_result_node import SearchResultNode
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
    api_instance = edu_sharing_client.SEARCHV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    content_type = 'content_type_example' # str | Type of element (optional)
    combine_mode = 'combine_mode_example' # str | Combine mode, AND or OR, defaults to AND (optional)
    var_property = ['var_property_example'] # List[str] | One (or more) properties to search for, will be combined by specified combine mode (optional)
    value = ['value_example'] # List[str] | One (or more) values to search for, matching the properties defined before (optional)
    comparator = ['comparator_example'] # List[str] | (Optional) comparator, only relevant for date or numerical fields, currently allowed =, <=, >= (optional)
    max_items = 10 # int | maximum items per page (optional) (default to 10)
    skip_count = 0 # int | skip a number of items (optional) (default to 0)
    sort_properties = ['sort_properties_example'] # List[str] | sort properties (optional)
    sort_ascending = [True] # List[bool] | sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index (optional)
    property_filter = ['property_filter_example'] # List[str] | property filter for result nodes (or \"-all-\" for all properties) (optional)

    try:
        # Search for custom properties with custom values
        api_response = api_instance.search_by_property(repository, content_type=content_type, combine_mode=combine_mode, var_property=var_property, value=value, comparator=comparator, max_items=max_items, skip_count=skip_count, sort_properties=sort_properties, sort_ascending=sort_ascending, property_filter=property_filter)
        print("The response of SEARCHV1Api->search_by_property:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SEARCHV1Api->search_by_property: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **content_type** | **str**| Type of element | [optional] 
 **combine_mode** | **str**| Combine mode, AND or OR, defaults to AND | [optional] 
 **var_property** | [**List[str]**](str.md)| One (or more) properties to search for, will be combined by specified combine mode | [optional] 
 **value** | [**List[str]**](str.md)| One (or more) values to search for, matching the properties defined before | [optional] 
 **comparator** | [**List[str]**](str.md)| (Optional) comparator, only relevant for date or numerical fields, currently allowed &#x3D;, &lt;&#x3D;, &gt;&#x3D; | [optional] 
 **max_items** | **int**| maximum items per page | [optional] [default to 10]
 **skip_count** | **int**| skip a number of items | [optional] [default to 0]
 **sort_properties** | [**List[str]**](str.md)| sort properties | [optional] 
 **sort_ascending** | [**List[bool]**](bool.md)| sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index | [optional] 
 **property_filter** | [**List[str]**](str.md)| property filter for result nodes (or \&quot;-all-\&quot; for all properties) | [optional] 

### Return type

[**SearchResultNode**](SearchResultNode.md)

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

# **search_contributor**
> str search_contributor(repository, search_word, contributor_kind, fields=fields, contributor_properties=contributor_properties)

Search for contributors

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
    api_instance = edu_sharing_client.SEARCHV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    search_word = 'search_word_example' # str | search word
    contributor_kind = PERSON # str | contributor kind (default to PERSON)
    fields = ['fields_example'] # List[str] | define which authority fields should be searched: ['firstname', 'lastname', 'email', 'uuid', 'url'] (optional)
    contributor_properties = ['contributor_properties_example'] # List[str] | define which contributor props should be searched: ['ccm:lifecyclecontributer_author', 'ccm:lifecyclecontributer_publisher', ..., 'ccm:metadatacontributer_creator', 'ccm:metadatacontributer_validator'] (optional)

    try:
        # Search for contributors
        api_response = api_instance.search_contributor(repository, search_word, contributor_kind, fields=fields, contributor_properties=contributor_properties)
        print("The response of SEARCHV1Api->search_contributor:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SEARCHV1Api->search_contributor: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **search_word** | **str**| search word | 
 **contributor_kind** | **str**| contributor kind | [default to PERSON]
 **fields** | [**List[str]**](str.md)| define which authority fields should be searched: [&#39;firstname&#39;, &#39;lastname&#39;, &#39;email&#39;, &#39;uuid&#39;, &#39;url&#39;] | [optional] 
 **contributor_properties** | [**List[str]**](str.md)| define which contributor props should be searched: [&#39;ccm:lifecyclecontributer_author&#39;, &#39;ccm:lifecyclecontributer_publisher&#39;, ..., &#39;ccm:metadatacontributer_creator&#39;, &#39;ccm:metadatacontributer_validator&#39;] | [optional] 

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

# **search_facets**
> SearchResultNode search_facets(repository, metadataset, query, search_parameters_facets)

Search in facets.

Perform queries based on metadata sets.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.search_parameters_facets import SearchParametersFacets
from edu_sharing_client.models.search_result_node import SearchResultNode
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
    api_instance = edu_sharing_client.SEARCHV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    metadataset = '-default-' # str | ID of metadataset (or \"-default-\" for default metadata set) (default to '-default-')
    query = 'query_example' # str | ID of query
    search_parameters_facets = edu_sharing_client.SearchParametersFacets() # SearchParametersFacets | facet parameters

    try:
        # Search in facets.
        api_response = api_instance.search_facets(repository, metadataset, query, search_parameters_facets)
        print("The response of SEARCHV1Api->search_facets:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SEARCHV1Api->search_facets: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **metadataset** | **str**| ID of metadataset (or \&quot;-default-\&quot; for default metadata set) | [default to &#39;-default-&#39;]
 **query** | **str**| ID of query | 
 **search_parameters_facets** | [**SearchParametersFacets**](SearchParametersFacets.md)| facet parameters | 

### Return type

[**SearchResultNode**](SearchResultNode.md)

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
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **search_fingerprint**
> SearchResultNode search_fingerprint(repository, nodeid, max_items=max_items, skip_count=skip_count, sort_properties=sort_properties, sort_ascending=sort_ascending, property_filter=property_filter)

Perform queries based on metadata sets.

Perform queries based on metadata sets.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.search_result_node import SearchResultNode
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
    api_instance = edu_sharing_client.SEARCHV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    nodeid = 'nodeid_example' # str | nodeid
    max_items = 10 # int | maximum items per page (optional) (default to 10)
    skip_count = 0 # int | skip a number of items (optional) (default to 0)
    sort_properties = ['sort_properties_example'] # List[str] | sort properties (optional)
    sort_ascending = [True] # List[bool] | sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index (optional)
    property_filter = ['property_filter_example'] # List[str] | property filter for result nodes (or \"-all-\" for all properties) (optional)

    try:
        # Perform queries based on metadata sets.
        api_response = api_instance.search_fingerprint(repository, nodeid, max_items=max_items, skip_count=skip_count, sort_properties=sort_properties, sort_ascending=sort_ascending, property_filter=property_filter)
        print("The response of SEARCHV1Api->search_fingerprint:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SEARCHV1Api->search_fingerprint: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **nodeid** | **str**| nodeid | 
 **max_items** | **int**| maximum items per page | [optional] [default to 10]
 **skip_count** | **int**| skip a number of items | [optional] [default to 0]
 **sort_properties** | [**List[str]**](str.md)| sort properties | [optional] 
 **sort_ascending** | [**List[bool]**](bool.md)| sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index | [optional] 
 **property_filter** | [**List[str]**](str.md)| property filter for result nodes (or \&quot;-all-\&quot; for all properties) | [optional] 

### Return type

[**SearchResultNode**](SearchResultNode.md)

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

# **search_lrmi**
> SearchResultLrmi search_lrmi(repository, metadataset, query, search_parameters, content_type=content_type, max_items=max_items, skip_count=skip_count, sort_properties=sort_properties, sort_ascending=sort_ascending, property_filter=property_filter)

Perform queries based on metadata sets.

Perform queries based on metadata sets.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.search_parameters import SearchParameters
from edu_sharing_client.models.search_result_lrmi import SearchResultLrmi
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
    api_instance = edu_sharing_client.SEARCHV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    metadataset = '-default-' # str | ID of metadataset (or \"-default-\" for default metadata set) (default to '-default-')
    query = 'query_example' # str | ID of query
    search_parameters = edu_sharing_client.SearchParameters() # SearchParameters | search parameters
    content_type = 'content_type_example' # str | Type of element (optional)
    max_items = 10 # int | maximum items per page (optional) (default to 10)
    skip_count = 0 # int | skip a number of items (optional) (default to 0)
    sort_properties = ['sort_properties_example'] # List[str] | sort properties (optional)
    sort_ascending = [True] # List[bool] | sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index (optional)
    property_filter = ['property_filter_example'] # List[str] | property filter for result nodes (or \"-all-\" for all properties) (optional)

    try:
        # Perform queries based on metadata sets.
        api_response = api_instance.search_lrmi(repository, metadataset, query, search_parameters, content_type=content_type, max_items=max_items, skip_count=skip_count, sort_properties=sort_properties, sort_ascending=sort_ascending, property_filter=property_filter)
        print("The response of SEARCHV1Api->search_lrmi:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SEARCHV1Api->search_lrmi: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **metadataset** | **str**| ID of metadataset (or \&quot;-default-\&quot; for default metadata set) | [default to &#39;-default-&#39;]
 **query** | **str**| ID of query | 
 **search_parameters** | [**SearchParameters**](SearchParameters.md)| search parameters | 
 **content_type** | **str**| Type of element | [optional] 
 **max_items** | **int**| maximum items per page | [optional] [default to 10]
 **skip_count** | **int**| skip a number of items | [optional] [default to 0]
 **sort_properties** | [**List[str]**](str.md)| sort properties | [optional] 
 **sort_ascending** | [**List[bool]**](bool.md)| sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index | [optional] 
 **property_filter** | [**List[str]**](str.md)| property filter for result nodes (or \&quot;-all-\&quot; for all properties) | [optional] 

### Return type

[**SearchResultLrmi**](SearchResultLrmi.md)

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

