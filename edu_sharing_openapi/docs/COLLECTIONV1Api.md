# edu_sharing_client.COLLECTIONV1Api

All URIs are relative to *https://stable.demo.edu-sharing.net/edu-sharing/rest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_to_collection**](COLLECTIONV1Api.md#add_to_collection) | **PUT** /collection/v1/collections/{repository}/{collection}/references/{node} | Add a node to a collection.
[**change_icon_of_collection**](COLLECTIONV1Api.md#change_icon_of_collection) | **POST** /collection/v1/collections/{repository}/{collection}/icon | Writes Preview Image of a collection.
[**create_collection**](COLLECTIONV1Api.md#create_collection) | **POST** /collection/v1/collections/{repository}/{collection}/children | Create a new collection.
[**delete_collection**](COLLECTIONV1Api.md#delete_collection) | **DELETE** /collection/v1/collections/{repository}/{collection} | Delete a collection.
[**delete_from_collection**](COLLECTIONV1Api.md#delete_from_collection) | **DELETE** /collection/v1/collections/{repository}/{collection}/references/{node} | Delete a node from a collection.
[**get_collection**](COLLECTIONV1Api.md#get_collection) | **GET** /collection/v1/collections/{repository}/{collectionId} | Get a collection.
[**get_collections_containing_proposals**](COLLECTIONV1Api.md#get_collections_containing_proposals) | **GET** /collection/v1/collections/{repository}/children/proposals/collections | Get all collections containing proposals with a given state (via search index)
[**get_collections_proposals**](COLLECTIONV1Api.md#get_collections_proposals) | **GET** /collection/v1/collections/{repository}/{collection}/children/proposals | Get proposed objects for collection (requires edit permissions on collection).
[**get_collections_references**](COLLECTIONV1Api.md#get_collections_references) | **GET** /collection/v1/collections/{repository}/{collection}/children/references | Get references objects for collection.
[**get_collections_subcollections**](COLLECTIONV1Api.md#get_collections_subcollections) | **GET** /collection/v1/collections/{repository}/{collection}/children/collections | Get child collections for collection (or root).
[**remove_icon_of_collection**](COLLECTIONV1Api.md#remove_icon_of_collection) | **DELETE** /collection/v1/collections/{repository}/{collection}/icon | Deletes Preview Image of a collection.
[**search_collections**](COLLECTIONV1Api.md#search_collections) | **GET** /collection/v1/collections/{repository}/search | Search collections.
[**set_collection_order**](COLLECTIONV1Api.md#set_collection_order) | **POST** /collection/v1/collections/{repository}/{collection}/order | Set order of nodes in a collection. In order to work as expected, provide a list of all nodes in this collection
[**set_pinned_collections**](COLLECTIONV1Api.md#set_pinned_collections) | **POST** /collection/v1/collections/{repository}/pinning | Set pinned collections.
[**update_collection**](COLLECTIONV1Api.md#update_collection) | **PUT** /collection/v1/collections/{repository}/{collection} | Update a collection.


# **add_to_collection**
> NodeEntry add_to_collection(repository, collection, node, source_repo=source_repo, allow_duplicate=allow_duplicate, as_proposal=as_proposal)

Add a node to a collection.

Add a node to a collection.

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
    api_instance = edu_sharing_client.COLLECTIONV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    collection = 'collection_example' # str | ID of collection
    node = 'node_example' # str | ID of node
    source_repo = 'source_repo_example' # str | ID of source repository (optional)
    allow_duplicate = False # bool | Allow that a node that already is inside the collection can be added again (optional) (default to False)
    as_proposal = False # bool | Mark this node only as a proposal (not really adding but just marking it). This can also be used for collections where you don't have permissions (optional) (default to False)

    try:
        # Add a node to a collection.
        api_response = api_instance.add_to_collection(repository, collection, node, source_repo=source_repo, allow_duplicate=allow_duplicate, as_proposal=as_proposal)
        print("The response of COLLECTIONV1Api->add_to_collection:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling COLLECTIONV1Api->add_to_collection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **collection** | **str**| ID of collection | 
 **node** | **str**| ID of node | 
 **source_repo** | **str**| ID of source repository | [optional] 
 **allow_duplicate** | **bool**| Allow that a node that already is inside the collection can be added again | [optional] [default to False]
 **as_proposal** | **bool**| Mark this node only as a proposal (not really adding but just marking it). This can also be used for collections where you don&#39;t have permissions | [optional] [default to False]

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

# **change_icon_of_collection**
> CollectionEntry change_icon_of_collection(repository, collection, mimetype, file=file)

Writes Preview Image of a collection.

Writes Preview Image of a collection.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.collection_entry import CollectionEntry
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
    api_instance = edu_sharing_client.COLLECTIONV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    collection = 'collection_example' # str | ID of collection
    mimetype = 'mimetype_example' # str | MIME-Type
    file = None # object |  (optional)

    try:
        # Writes Preview Image of a collection.
        api_response = api_instance.change_icon_of_collection(repository, collection, mimetype, file=file)
        print("The response of COLLECTIONV1Api->change_icon_of_collection:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling COLLECTIONV1Api->change_icon_of_collection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **collection** | **str**| ID of collection | 
 **mimetype** | **str**| MIME-Type | 
 **file** | [**object**](object.md)|  | [optional] 

### Return type

[**CollectionEntry**](CollectionEntry.md)

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

# **create_collection**
> CollectionEntry create_collection(repository, collection, node)

Create a new collection.

Create a new collection.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.collection_entry import CollectionEntry
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
    api_instance = edu_sharing_client.COLLECTIONV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    collection = 'collection_example' # str | ID of parent collection (or \"-root-\" for level0 collections)
    node = edu_sharing_client.Node() # Node | collection

    try:
        # Create a new collection.
        api_response = api_instance.create_collection(repository, collection, node)
        print("The response of COLLECTIONV1Api->create_collection:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling COLLECTIONV1Api->create_collection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **collection** | **str**| ID of parent collection (or \&quot;-root-\&quot; for level0 collections) | 
 **node** | [**Node**](Node.md)| collection | 

### Return type

[**CollectionEntry**](CollectionEntry.md)

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

# **delete_collection**
> delete_collection(repository, collection)

Delete a collection.

Delete a collection.

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
    api_instance = edu_sharing_client.COLLECTIONV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    collection = 'collection_example' # str | ID of collection

    try:
        # Delete a collection.
        api_instance.delete_collection(repository, collection)
    except Exception as e:
        print("Exception when calling COLLECTIONV1Api->delete_collection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **collection** | **str**| ID of collection | 

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

# **delete_from_collection**
> delete_from_collection(repository, collection, node)

Delete a node from a collection.

Delete a node from a collection.

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
    api_instance = edu_sharing_client.COLLECTIONV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    collection = 'collection_example' # str | ID of collection
    node = 'node_example' # str | ID of node

    try:
        # Delete a node from a collection.
        api_instance.delete_from_collection(repository, collection, node)
    except Exception as e:
        print("Exception when calling COLLECTIONV1Api->delete_from_collection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **collection** | **str**| ID of collection | 
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

# **get_collection**
> CollectionEntry get_collection(repository, collection_id, track=track)

Get a collection.

Get a collection.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.collection_entry import CollectionEntry
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
    api_instance = edu_sharing_client.COLLECTIONV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    collection_id = 'collection_id_example' # str | ID of collection
    track = True # bool | track this as a view of the collection (default: true) (optional)

    try:
        # Get a collection.
        api_response = api_instance.get_collection(repository, collection_id, track=track)
        print("The response of COLLECTIONV1Api->get_collection:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling COLLECTIONV1Api->get_collection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **collection_id** | **str**| ID of collection | 
 **track** | **bool**| track this as a view of the collection (default: true) | [optional] 

### Return type

[**CollectionEntry**](CollectionEntry.md)

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

# **get_collections_containing_proposals**
> CollectionProposalEntries get_collections_containing_proposals(repository, status=status, fetch_counts=fetch_counts, max_items=max_items, skip_count=skip_count, sort_properties=sort_properties, sort_ascending=sort_ascending)

Get all collections containing proposals with a given state (via search index)

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.collection_proposal_entries import CollectionProposalEntries
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
    api_instance = edu_sharing_client.COLLECTIONV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    status = PENDING # str | status of the proposals to search for (optional) (default to PENDING)
    fetch_counts = True # bool | fetch counts of collections (materials and subcollections). This parameter will decrease performance so only enable if if you need this data (optional) (default to True)
    max_items = 50 # int | maximum items per page (optional) (default to 50)
    skip_count = 0 # int | skip a number of items (optional) (default to 0)
    sort_properties = ['sort_properties_example'] # List[str] | sort properties (optional)
    sort_ascending = [True] # List[bool] | sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index (optional)

    try:
        # Get all collections containing proposals with a given state (via search index)
        api_response = api_instance.get_collections_containing_proposals(repository, status=status, fetch_counts=fetch_counts, max_items=max_items, skip_count=skip_count, sort_properties=sort_properties, sort_ascending=sort_ascending)
        print("The response of COLLECTIONV1Api->get_collections_containing_proposals:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling COLLECTIONV1Api->get_collections_containing_proposals: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **status** | **str**| status of the proposals to search for | [optional] [default to PENDING]
 **fetch_counts** | **bool**| fetch counts of collections (materials and subcollections). This parameter will decrease performance so only enable if if you need this data | [optional] [default to True]
 **max_items** | **int**| maximum items per page | [optional] [default to 50]
 **skip_count** | **int**| skip a number of items | [optional] [default to 0]
 **sort_properties** | [**List[str]**](str.md)| sort properties | [optional] 
 **sort_ascending** | [**List[bool]**](bool.md)| sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index | [optional] 

### Return type

[**CollectionProposalEntries**](CollectionProposalEntries.md)

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

# **get_collections_proposals**
> AbstractEntries get_collections_proposals(repository, collection, status)

Get proposed objects for collection (requires edit permissions on collection).

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.abstract_entries import AbstractEntries
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
    api_instance = edu_sharing_client.COLLECTIONV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    collection = 'collection_example' # str | ID of parent collection
    status = 'status_example' # str | Only show elements with given status

    try:
        # Get proposed objects for collection (requires edit permissions on collection).
        api_response = api_instance.get_collections_proposals(repository, collection, status)
        print("The response of COLLECTIONV1Api->get_collections_proposals:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling COLLECTIONV1Api->get_collections_proposals: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **collection** | **str**| ID of parent collection | 
 **status** | **str**| Only show elements with given status | 

### Return type

[**AbstractEntries**](AbstractEntries.md)

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

# **get_collections_references**
> ReferenceEntries get_collections_references(repository, collection, max_items=max_items, skip_count=skip_count, sort_properties=sort_properties, sort_ascending=sort_ascending, property_filter=property_filter)

Get references objects for collection.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.reference_entries import ReferenceEntries
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
    api_instance = edu_sharing_client.COLLECTIONV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    collection = 'collection_example' # str | ID of parent collection
    max_items = 500 # int | maximum items per page (optional) (default to 500)
    skip_count = 0 # int | skip a number of items (optional) (default to 0)
    sort_properties = ['sort_properties_example'] # List[str] | sort properties (optional)
    sort_ascending = [True] # List[bool] | sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index (optional)
    property_filter = ['property_filter_example'] # List[str] | property filter for result nodes (or \"-all-\" for all properties) (optional)

    try:
        # Get references objects for collection.
        api_response = api_instance.get_collections_references(repository, collection, max_items=max_items, skip_count=skip_count, sort_properties=sort_properties, sort_ascending=sort_ascending, property_filter=property_filter)
        print("The response of COLLECTIONV1Api->get_collections_references:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling COLLECTIONV1Api->get_collections_references: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **collection** | **str**| ID of parent collection | 
 **max_items** | **int**| maximum items per page | [optional] [default to 500]
 **skip_count** | **int**| skip a number of items | [optional] [default to 0]
 **sort_properties** | [**List[str]**](str.md)| sort properties | [optional] 
 **sort_ascending** | [**List[bool]**](bool.md)| sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index | [optional] 
 **property_filter** | [**List[str]**](str.md)| property filter for result nodes (or \&quot;-all-\&quot; for all properties) | [optional] 

### Return type

[**ReferenceEntries**](ReferenceEntries.md)

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

# **get_collections_subcollections**
> CollectionEntries get_collections_subcollections(repository, collection, scope, fetch_counts=fetch_counts, max_items=max_items, skip_count=skip_count, sort_properties=sort_properties, sort_ascending=sort_ascending, property_filter=property_filter)

Get child collections for collection (or root).

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.collection_entries import CollectionEntries
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
    api_instance = edu_sharing_client.COLLECTIONV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    collection = 'collection_example' # str | ID of parent collection (or \"-root-\" for level0 collections)
    scope = MY # str | scope (only relevant if parent == -root-) (default to MY)
    fetch_counts = True # bool | fetch counts of collections (materials and subcollections). This parameter will decrease performance so only enable if if you need this data (optional) (default to True)
    max_items = 500 # int | maximum items per page (optional) (default to 500)
    skip_count = 0 # int | skip a number of items (optional) (default to 0)
    sort_properties = ['sort_properties_example'] # List[str] | sort properties (optional)
    sort_ascending = [True] # List[bool] | sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index (optional)
    property_filter = ['property_filter_example'] # List[str] | property filter for result nodes (or \"-all-\" for all properties) (optional)

    try:
        # Get child collections for collection (or root).
        api_response = api_instance.get_collections_subcollections(repository, collection, scope, fetch_counts=fetch_counts, max_items=max_items, skip_count=skip_count, sort_properties=sort_properties, sort_ascending=sort_ascending, property_filter=property_filter)
        print("The response of COLLECTIONV1Api->get_collections_subcollections:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling COLLECTIONV1Api->get_collections_subcollections: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **collection** | **str**| ID of parent collection (or \&quot;-root-\&quot; for level0 collections) | 
 **scope** | **str**| scope (only relevant if parent &#x3D;&#x3D; -root-) | [default to MY]
 **fetch_counts** | **bool**| fetch counts of collections (materials and subcollections). This parameter will decrease performance so only enable if if you need this data | [optional] [default to True]
 **max_items** | **int**| maximum items per page | [optional] [default to 500]
 **skip_count** | **int**| skip a number of items | [optional] [default to 0]
 **sort_properties** | [**List[str]**](str.md)| sort properties | [optional] 
 **sort_ascending** | [**List[bool]**](bool.md)| sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index | [optional] 
 **property_filter** | [**List[str]**](str.md)| property filter for result nodes (or \&quot;-all-\&quot; for all properties) | [optional] 

### Return type

[**CollectionEntries**](CollectionEntries.md)

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

# **remove_icon_of_collection**
> remove_icon_of_collection(repository, collection)

Deletes Preview Image of a collection.

Deletes Preview Image of a collection.

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
    api_instance = edu_sharing_client.COLLECTIONV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    collection = 'collection_example' # str | ID of collection

    try:
        # Deletes Preview Image of a collection.
        api_instance.remove_icon_of_collection(repository, collection)
    except Exception as e:
        print("Exception when calling COLLECTIONV1Api->remove_icon_of_collection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **collection** | **str**| ID of collection | 

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

# **search_collections**
> CollectionEntries search_collections(repository, query, max_items=max_items, skip_count=skip_count, sort_properties=sort_properties, sort_ascending=sort_ascending)

Search collections.

Search collections.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.collection_entries import CollectionEntries
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
    api_instance = edu_sharing_client.COLLECTIONV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    query = 'query_example' # str | query string
    max_items = 500 # int | maximum items per page (optional) (default to 500)
    skip_count = 0 # int | skip a number of items (optional) (default to 0)
    sort_properties = ['sort_properties_example'] # List[str] | sort properties (optional)
    sort_ascending = [True] # List[bool] | sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index (optional)

    try:
        # Search collections.
        api_response = api_instance.search_collections(repository, query, max_items=max_items, skip_count=skip_count, sort_properties=sort_properties, sort_ascending=sort_ascending)
        print("The response of COLLECTIONV1Api->search_collections:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling COLLECTIONV1Api->search_collections: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **query** | **str**| query string | 
 **max_items** | **int**| maximum items per page | [optional] [default to 500]
 **skip_count** | **int**| skip a number of items | [optional] [default to 0]
 **sort_properties** | [**List[str]**](str.md)| sort properties | [optional] 
 **sort_ascending** | [**List[bool]**](bool.md)| sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index | [optional] 

### Return type

[**CollectionEntries**](CollectionEntries.md)

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

# **set_collection_order**
> set_collection_order(repository, collection, request_body=request_body)

Set order of nodes in a collection. In order to work as expected, provide a list of all nodes in this collection

Current order will be overriden. Requires full permissions for the parent collection

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
    api_instance = edu_sharing_client.COLLECTIONV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    collection = 'collection_example' # str | ID of collection
    request_body = ['request_body_example'] # List[str] | List of nodes in the order to be saved. If empty, custom order of the collection will be disabled (optional)

    try:
        # Set order of nodes in a collection. In order to work as expected, provide a list of all nodes in this collection
        api_instance.set_collection_order(repository, collection, request_body=request_body)
    except Exception as e:
        print("Exception when calling COLLECTIONV1Api->set_collection_order: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **collection** | **str**| ID of collection | 
 **request_body** | [**List[str]**](str.md)| List of nodes in the order to be saved. If empty, custom order of the collection will be disabled | [optional] 

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

# **set_pinned_collections**
> set_pinned_collections(repository, request_body)

Set pinned collections.

Remove all currently pinned collections and set them in the order send. Requires TOOLPERMISSION_COLLECTION_PINNING

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
    api_instance = edu_sharing_client.COLLECTIONV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    request_body = ['request_body_example'] # List[str] | List of collections that should be pinned

    try:
        # Set pinned collections.
        api_instance.set_pinned_collections(repository, request_body)
    except Exception as e:
        print("Exception when calling COLLECTIONV1Api->set_pinned_collections: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **request_body** | [**List[str]**](str.md)| List of collections that should be pinned | 

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

# **update_collection**
> update_collection(repository, collection, node)

Update a collection.

Update a collection.

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
    api_instance = edu_sharing_client.COLLECTIONV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    collection = 'collection_example' # str | ID of collection
    node = edu_sharing_client.Node() # Node | collection node

    try:
        # Update a collection.
        api_instance.update_collection(repository, collection, node)
    except Exception as e:
        print("Exception when calling COLLECTIONV1Api->update_collection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **collection** | **str**| ID of collection | 
 **node** | [**Node**](Node.md)| collection node | 

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

