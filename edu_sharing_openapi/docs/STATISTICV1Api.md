# edu_sharing_client.STATISTICV1Api

All URIs are relative to *https://stable.demo.edu-sharing.net/edu-sharing/rest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get**](STATISTICV1Api.md#get) | **POST** /statistic/v1/facets/{context} | Get statistics of repository.
[**get_global_statistics**](STATISTICV1Api.md#get_global_statistics) | **GET** /statistic/v1/public | Get stats.
[**get_node_data**](STATISTICV1Api.md#get_node_data) | **GET** /statistic/v1/statistics/nodes/node/{id} | get the range of nodes which had tracked actions since a given timestamp
[**get_nodes_altered_in_range1**](STATISTICV1Api.md#get_nodes_altered_in_range1) | **GET** /statistic/v1/statistics/nodes/altered | get the range of nodes which had tracked actions since a given timestamp
[**get_statistics_node**](STATISTICV1Api.md#get_statistics_node) | **POST** /statistic/v1/statistics/nodes | get statistics for node actions
[**get_statistics_user**](STATISTICV1Api.md#get_statistics_user) | **POST** /statistic/v1/statistics/users | get statistics for user actions (login, logout)


# **get**
> Statistics get(context, filter, properties=properties)

Get statistics of repository.

Statistics.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.filter import Filter
from edu_sharing_client.models.statistics import Statistics
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
    api_instance = edu_sharing_client.STATISTICV1Api(api_client)
    context = '-root-' # str | context, the node where to start (default to '-root-')
    filter = edu_sharing_client.Filter() # Filter | filter
    properties = ['properties_example'] # List[str] | properties (optional)

    try:
        # Get statistics of repository.
        api_response = api_instance.get(context, filter, properties=properties)
        print("The response of STATISTICV1Api->get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling STATISTICV1Api->get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **context** | **str**| context, the node where to start | [default to &#39;-root-&#39;]
 **filter** | [**Filter**](Filter.md)| filter | 
 **properties** | [**List[str]**](str.md)| properties | [optional] 

### Return type

[**Statistics**](Statistics.md)

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

# **get_global_statistics**
> StatisticsGlobal get_global_statistics(group=group, sub_group=sub_group)

Get stats.

Get global statistics for this repository.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.statistics_global import StatisticsGlobal
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
    api_instance = edu_sharing_client.STATISTICV1Api(api_client)
    group = 'group_example' # str | primary property to build facets and count+group values (optional)
    sub_group = ['sub_group_example'] # List[str] | additional properties to build facets and count+sub-group values (optional)

    try:
        # Get stats.
        api_response = api_instance.get_global_statistics(group=group, sub_group=sub_group)
        print("The response of STATISTICV1Api->get_global_statistics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling STATISTICV1Api->get_global_statistics: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group** | **str**| primary property to build facets and count+group values | [optional] 
 **sub_group** | [**List[str]**](str.md)| additional properties to build facets and count+sub-group values | [optional] 

### Return type

[**StatisticsGlobal**](StatisticsGlobal.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK. |  -  |
**401** | Authorization failed. |  -  |
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_node_data**
> str get_node_data(id, date_from)

get the range of nodes which had tracked actions since a given timestamp

requires admin

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
    api_instance = edu_sharing_client.STATISTICV1Api(api_client)
    id = 'id_example' # str | node id to fetch data for
    date_from = 56 # int | date range from

    try:
        # get the range of nodes which had tracked actions since a given timestamp
        api_response = api_instance.get_node_data(id, date_from)
        print("The response of STATISTICV1Api->get_node_data:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling STATISTICV1Api->get_node_data: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| node id to fetch data for | 
 **date_from** | **int**| date range from | 

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

# **get_nodes_altered_in_range1**
> str get_nodes_altered_in_range1(date_from)

get the range of nodes which had tracked actions since a given timestamp

requires admin

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
    api_instance = edu_sharing_client.STATISTICV1Api(api_client)
    date_from = 56 # int | date range from

    try:
        # get the range of nodes which had tracked actions since a given timestamp
        api_response = api_instance.get_nodes_altered_in_range1(date_from)
        print("The response of STATISTICV1Api->get_nodes_altered_in_range1:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling STATISTICV1Api->get_nodes_altered_in_range1: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **date_from** | **int**| date range from | 

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

# **get_statistics_node**
> str get_statistics_node(grouping, date_from, date_to, mediacenter=mediacenter, additional_fields=additional_fields, group_field=group_field, request_body=request_body)

get statistics for node actions

requires either toolpermission TOOLPERMISSION_GLOBAL_STATISTICS_NODES for global stats or to be admin of the requested mediacenter

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
    api_instance = edu_sharing_client.STATISTICV1Api(api_client)
    grouping = 'grouping_example' # str | Grouping type (by date)
    date_from = 56 # int | date range from
    date_to = 56 # int | date range to
    mediacenter = 'mediacenter_example' # str | the mediacenter to filter for statistics (optional)
    additional_fields = ['additional_fields_example'] # List[str] | additionals fields of the custom json object stored in each query that should be returned (optional)
    group_field = ['group_field_example'] # List[str] | grouping fields of the custom json object stored in each query (currently only meant to be combined with no grouping by date) (optional)
    request_body = {'key': 'request_body_example'} # Dict[str, str] | filters for the custom json object stored in each entry (optional)

    try:
        # get statistics for node actions
        api_response = api_instance.get_statistics_node(grouping, date_from, date_to, mediacenter=mediacenter, additional_fields=additional_fields, group_field=group_field, request_body=request_body)
        print("The response of STATISTICV1Api->get_statistics_node:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling STATISTICV1Api->get_statistics_node: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **grouping** | **str**| Grouping type (by date) | 
 **date_from** | **int**| date range from | 
 **date_to** | **int**| date range to | 
 **mediacenter** | **str**| the mediacenter to filter for statistics | [optional] 
 **additional_fields** | [**List[str]**](str.md)| additionals fields of the custom json object stored in each query that should be returned | [optional] 
 **group_field** | [**List[str]**](str.md)| grouping fields of the custom json object stored in each query (currently only meant to be combined with no grouping by date) | [optional] 
 **request_body** | [**Dict[str, str]**](str.md)| filters for the custom json object stored in each entry | [optional] 

### Return type

**str**

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

# **get_statistics_user**
> str get_statistics_user(grouping, date_from, date_to, mediacenter=mediacenter, additional_fields=additional_fields, group_field=group_field, request_body=request_body)

get statistics for user actions (login, logout)

requires either toolpermission TOOLPERMISSION_GLOBAL_STATISTICS_USER for global stats or to be admin of the requested mediacenter

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
    api_instance = edu_sharing_client.STATISTICV1Api(api_client)
    grouping = 'grouping_example' # str | Grouping type (by date)
    date_from = 56 # int | date range from
    date_to = 56 # int | date range to
    mediacenter = 'mediacenter_example' # str | the mediacenter to filter for statistics (optional)
    additional_fields = ['additional_fields_example'] # List[str] | additionals fields of the custom json object stored in each query that should be returned (optional)
    group_field = ['group_field_example'] # List[str] | grouping fields of the custom json object stored in each query (currently only meant to be combined with no grouping by date) (optional)
    request_body = {'key': 'request_body_example'} # Dict[str, str] | filters for the custom json object stored in each entry (optional)

    try:
        # get statistics for user actions (login, logout)
        api_response = api_instance.get_statistics_user(grouping, date_from, date_to, mediacenter=mediacenter, additional_fields=additional_fields, group_field=group_field, request_body=request_body)
        print("The response of STATISTICV1Api->get_statistics_user:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling STATISTICV1Api->get_statistics_user: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **grouping** | **str**| Grouping type (by date) | 
 **date_from** | **int**| date range from | 
 **date_to** | **int**| date range to | 
 **mediacenter** | **str**| the mediacenter to filter for statistics | [optional] 
 **additional_fields** | [**List[str]**](str.md)| additionals fields of the custom json object stored in each query that should be returned | [optional] 
 **group_field** | [**List[str]**](str.md)| grouping fields of the custom json object stored in each query (currently only meant to be combined with no grouping by date) | [optional] 
 **request_body** | [**Dict[str, str]**](str.md)| filters for the custom json object stored in each entry | [optional] 

### Return type

**str**

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

