# edu_sharing_client.MEDIACENTERV1Api

All URIs are relative to *https://stable.demo.edu-sharing.net/edu-sharing/rest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_mediacenter_group**](MEDIACENTERV1Api.md#add_mediacenter_group) | **PUT** /mediacenter/v1/mediacenter/{repository}/{mediacenter}/manages/{group} | add a group that is managed by the given mediacenter
[**create_mediacenter**](MEDIACENTERV1Api.md#create_mediacenter) | **POST** /mediacenter/v1/mediacenter/{repository}/{mediacenter} | create new mediacenter in repository.
[**delete_mediacenter**](MEDIACENTERV1Api.md#delete_mediacenter) | **DELETE** /mediacenter/v1/mediacenter/{repository}/{mediacenter} | delete a mediacenter group and it&#39;s admin group and proxy group
[**edit_mediacenter**](MEDIACENTERV1Api.md#edit_mediacenter) | **PUT** /mediacenter/v1/mediacenter/{repository}/{mediacenter} | edit a mediacenter in repository.
[**export_mediacenter_licensed_nodes**](MEDIACENTERV1Api.md#export_mediacenter_licensed_nodes) | **POST** /mediacenter/v1/mediacenter/{repository}/{mediacenter}/licenses/export | get nodes that are licensed by the given mediacenter
[**get_mediacenter_groups**](MEDIACENTERV1Api.md#get_mediacenter_groups) | **GET** /mediacenter/v1/mediacenter/{repository}/{mediacenter}/manages | get groups that are managed by the given mediacenter
[**get_mediacenter_licensed_nodes**](MEDIACENTERV1Api.md#get_mediacenter_licensed_nodes) | **POST** /mediacenter/v1/mediacenter/{repository}/{mediacenter}/licenses | get nodes that are licensed by the given mediacenter
[**get_mediacenters**](MEDIACENTERV1Api.md#get_mediacenters) | **GET** /mediacenter/v1/mediacenter/{repository} | get mediacenters in the repository.
[**import_mc_org_connections**](MEDIACENTERV1Api.md#import_mc_org_connections) | **POST** /mediacenter/v1/import/mc_org | Import Mediacenter Organisation Connection
[**import_mediacenters**](MEDIACENTERV1Api.md#import_mediacenters) | **POST** /mediacenter/v1/import/mediacenters | Import mediacenters
[**import_organisations**](MEDIACENTERV1Api.md#import_organisations) | **POST** /mediacenter/v1/import/organisations | Import Organisations
[**remove_mediacenter_group**](MEDIACENTERV1Api.md#remove_mediacenter_group) | **DELETE** /mediacenter/v1/mediacenter/{repository}/{mediacenter}/manages/{group} | delete a group that is managed by the given mediacenter


# **add_mediacenter_group**
> str add_mediacenter_group(repository, mediacenter, group)

add a group that is managed by the given mediacenter

although not restricted, it is recommended that the group is an edu-sharing organization (admin rights are required)

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
    api_instance = edu_sharing_client.MEDIACENTERV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    mediacenter = 'mediacenter_example' # str | authorityName of the mediacenter that should manage the group
    group = 'group_example' # str | authorityName of the group that should be managed by that mediacenter

    try:
        # add a group that is managed by the given mediacenter
        api_response = api_instance.add_mediacenter_group(repository, mediacenter, group)
        print("The response of MEDIACENTERV1Api->add_mediacenter_group:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MEDIACENTERV1Api->add_mediacenter_group: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **mediacenter** | **str**| authorityName of the mediacenter that should manage the group | 
 **group** | **str**| authorityName of the group that should be managed by that mediacenter | 

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
**409** | Duplicate Entity/Node conflict (Node with same name exists) |  -  |
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_mediacenter**
> Mediacenter create_mediacenter(repository, mediacenter, profile=profile)

create new mediacenter in repository.

admin rights are required.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.mediacenter import Mediacenter
from edu_sharing_client.models.profile import Profile
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
    api_instance = edu_sharing_client.MEDIACENTERV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    mediacenter = 'mediacenter_example' # str | mediacenter name
    profile = edu_sharing_client.Profile() # Profile |  (optional)

    try:
        # create new mediacenter in repository.
        api_response = api_instance.create_mediacenter(repository, mediacenter, profile=profile)
        print("The response of MEDIACENTERV1Api->create_mediacenter:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MEDIACENTERV1Api->create_mediacenter: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **mediacenter** | **str**| mediacenter name | 
 **profile** | [**Profile**](Profile.md)|  | [optional] 

### Return type

[**Mediacenter**](Mediacenter.md)

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

# **delete_mediacenter**
> delete_mediacenter(repository, mediacenter)

delete a mediacenter group and it's admin group and proxy group

admin rights are required.

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
    api_instance = edu_sharing_client.MEDIACENTERV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    mediacenter = 'mediacenter_example' # str | authorityName of the mediacenter that should manage the group

    try:
        # delete a mediacenter group and it's admin group and proxy group
        api_instance.delete_mediacenter(repository, mediacenter)
    except Exception as e:
        print("Exception when calling MEDIACENTERV1Api->delete_mediacenter: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **mediacenter** | **str**| authorityName of the mediacenter that should manage the group | 

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
**409** | Duplicate Entity/Node conflict (Node with same name exists) |  -  |
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **edit_mediacenter**
> Mediacenter edit_mediacenter(repository, mediacenter, profile=profile)

edit a mediacenter in repository.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.mediacenter import Mediacenter
from edu_sharing_client.models.profile import Profile
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
    api_instance = edu_sharing_client.MEDIACENTERV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    mediacenter = 'mediacenter_example' # str | mediacenter name
    profile = edu_sharing_client.Profile() # Profile |  (optional)

    try:
        # edit a mediacenter in repository.
        api_response = api_instance.edit_mediacenter(repository, mediacenter, profile=profile)
        print("The response of MEDIACENTERV1Api->edit_mediacenter:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MEDIACENTERV1Api->edit_mediacenter: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **mediacenter** | **str**| mediacenter name | 
 **profile** | [**Profile**](Profile.md)|  | [optional] 

### Return type

[**Mediacenter**](Mediacenter.md)

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

# **export_mediacenter_licensed_nodes**
> str export_mediacenter_licensed_nodes(repository, mediacenter, search_parameters, sort_properties=sort_properties, sort_ascending=sort_ascending, properties=properties)

get nodes that are licensed by the given mediacenter

e.g. cm:name

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.search_parameters import SearchParameters
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
    api_instance = edu_sharing_client.MEDIACENTERV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    mediacenter = 'mediacenter_example' # str | authorityName of the mediacenter that licenses nodes
    search_parameters = edu_sharing_client.SearchParameters() # SearchParameters | search parameters
    sort_properties = ['sort_properties_example'] # List[str] | sort properties (optional)
    sort_ascending = [True] # List[bool] | sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index (optional)
    properties = ['properties_example'] # List[str] | properties to fetch, use parent::<property> to include parent property values (optional)

    try:
        # get nodes that are licensed by the given mediacenter
        api_response = api_instance.export_mediacenter_licensed_nodes(repository, mediacenter, search_parameters, sort_properties=sort_properties, sort_ascending=sort_ascending, properties=properties)
        print("The response of MEDIACENTERV1Api->export_mediacenter_licensed_nodes:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MEDIACENTERV1Api->export_mediacenter_licensed_nodes: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **mediacenter** | **str**| authorityName of the mediacenter that licenses nodes | 
 **search_parameters** | [**SearchParameters**](SearchParameters.md)| search parameters | 
 **sort_properties** | [**List[str]**](str.md)| sort properties | [optional] 
 **sort_ascending** | [**List[bool]**](bool.md)| sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index | [optional] 
 **properties** | [**List[str]**](str.md)| properties to fetch, use parent::&lt;property&gt; to include parent property values | [optional] 

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
**409** | Duplicate Entity/Node conflict (Node with same name exists) |  -  |
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_mediacenter_groups**
> str get_mediacenter_groups(repository, mediacenter)

get groups that are managed by the given mediacenter

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
    api_instance = edu_sharing_client.MEDIACENTERV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    mediacenter = 'mediacenter_example' # str | authorityName of the mediacenter that should manage the group

    try:
        # get groups that are managed by the given mediacenter
        api_response = api_instance.get_mediacenter_groups(repository, mediacenter)
        print("The response of MEDIACENTERV1Api->get_mediacenter_groups:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MEDIACENTERV1Api->get_mediacenter_groups: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **mediacenter** | **str**| authorityName of the mediacenter that should manage the group | 

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
**409** | Duplicate Entity/Node conflict (Node with same name exists) |  -  |
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_mediacenter_licensed_nodes**
> str get_mediacenter_licensed_nodes(repository, mediacenter, searchword, search_parameters, max_items=max_items, skip_count=skip_count, sort_properties=sort_properties, sort_ascending=sort_ascending, property_filter=property_filter)

get nodes that are licensed by the given mediacenter

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.search_parameters import SearchParameters
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
    api_instance = edu_sharing_client.MEDIACENTERV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    mediacenter = 'mediacenter_example' # str | authorityName of the mediacenter that licenses nodes
    searchword = 'searchword_example' # str | searchword of licensed nodes
    search_parameters = edu_sharing_client.SearchParameters() # SearchParameters | search parameters
    max_items = 10 # int | maximum items per page (optional) (default to 10)
    skip_count = 0 # int | skip a number of items (optional) (default to 0)
    sort_properties = ['sort_properties_example'] # List[str] | sort properties (optional)
    sort_ascending = [True] # List[bool] | sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index (optional)
    property_filter = ['property_filter_example'] # List[str] | property filter for result nodes (or \"-all-\" for all properties) (optional)

    try:
        # get nodes that are licensed by the given mediacenter
        api_response = api_instance.get_mediacenter_licensed_nodes(repository, mediacenter, searchword, search_parameters, max_items=max_items, skip_count=skip_count, sort_properties=sort_properties, sort_ascending=sort_ascending, property_filter=property_filter)
        print("The response of MEDIACENTERV1Api->get_mediacenter_licensed_nodes:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MEDIACENTERV1Api->get_mediacenter_licensed_nodes: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **mediacenter** | **str**| authorityName of the mediacenter that licenses nodes | 
 **searchword** | **str**| searchword of licensed nodes | 
 **search_parameters** | [**SearchParameters**](SearchParameters.md)| search parameters | 
 **max_items** | **int**| maximum items per page | [optional] [default to 10]
 **skip_count** | **int**| skip a number of items | [optional] [default to 0]
 **sort_properties** | [**List[str]**](str.md)| sort properties | [optional] 
 **sort_ascending** | [**List[bool]**](bool.md)| sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index | [optional] 
 **property_filter** | [**List[str]**](str.md)| property filter for result nodes (or \&quot;-all-\&quot; for all properties) | [optional] 

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
**409** | Duplicate Entity/Node conflict (Node with same name exists) |  -  |
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_mediacenters**
> str get_mediacenters(repository)

get mediacenters in the repository.

Only shows the one available/managing the current user (only admin can access all)

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
    api_instance = edu_sharing_client.MEDIACENTERV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')

    try:
        # get mediacenters in the repository.
        api_response = api_instance.get_mediacenters(repository)
        print("The response of MEDIACENTERV1Api->get_mediacenters:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MEDIACENTERV1Api->get_mediacenters: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]

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
**409** | Duplicate Entity/Node conflict (Node with same name exists) |  -  |
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **import_mc_org_connections**
> McOrgConnectResult import_mc_org_connections(mc_orgs, remove_schools_from_mc=remove_schools_from_mc)

Import Mediacenter Organisation Connection

Import Mediacenter Organisation Connection.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.mc_org_connect_result import McOrgConnectResult
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
    api_instance = edu_sharing_client.MEDIACENTERV1Api(api_client)
    mc_orgs = None # object | Mediacenter Organisation Connection csv to import
    remove_schools_from_mc = False # bool | removeSchoolsFromMC (optional) (default to False)

    try:
        # Import Mediacenter Organisation Connection
        api_response = api_instance.import_mc_org_connections(mc_orgs, remove_schools_from_mc=remove_schools_from_mc)
        print("The response of MEDIACENTERV1Api->import_mc_org_connections:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MEDIACENTERV1Api->import_mc_org_connections: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **mc_orgs** | [**object**](object.md)| Mediacenter Organisation Connection csv to import | 
 **remove_schools_from_mc** | **bool**| removeSchoolsFromMC | [optional] [default to False]

### Return type

[**McOrgConnectResult**](McOrgConnectResult.md)

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

# **import_mediacenters**
> MediacentersImportResult import_mediacenters(mediacenters)

Import mediacenters

Import mediacenters.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.mediacenters_import_result import MediacentersImportResult
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
    api_instance = edu_sharing_client.MEDIACENTERV1Api(api_client)
    mediacenters = None # object | Mediacenters csv to import

    try:
        # Import mediacenters
        api_response = api_instance.import_mediacenters(mediacenters)
        print("The response of MEDIACENTERV1Api->import_mediacenters:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MEDIACENTERV1Api->import_mediacenters: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **mediacenters** | [**object**](object.md)| Mediacenters csv to import | 

### Return type

[**MediacentersImportResult**](MediacentersImportResult.md)

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

# **import_organisations**
> OrganisationsImportResult import_organisations(organisations)

Import Organisations

Import Organisations.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.organisations_import_result import OrganisationsImportResult
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
    api_instance = edu_sharing_client.MEDIACENTERV1Api(api_client)
    organisations = None # object | Organisations csv to import

    try:
        # Import Organisations
        api_response = api_instance.import_organisations(organisations)
        print("The response of MEDIACENTERV1Api->import_organisations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MEDIACENTERV1Api->import_organisations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organisations** | [**object**](object.md)| Organisations csv to import | 

### Return type

[**OrganisationsImportResult**](OrganisationsImportResult.md)

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

# **remove_mediacenter_group**
> str remove_mediacenter_group(repository, mediacenter, group)

delete a group that is managed by the given mediacenter

admin rights are required.

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
    api_instance = edu_sharing_client.MEDIACENTERV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    mediacenter = 'mediacenter_example' # str | authorityName of the mediacenter that should manage the group
    group = 'group_example' # str | authorityName of the group that should not longer be managed by that mediacenter

    try:
        # delete a group that is managed by the given mediacenter
        api_response = api_instance.remove_mediacenter_group(repository, mediacenter, group)
        print("The response of MEDIACENTERV1Api->remove_mediacenter_group:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MEDIACENTERV1Api->remove_mediacenter_group: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **mediacenter** | **str**| authorityName of the mediacenter that should manage the group | 
 **group** | **str**| authorityName of the group that should not longer be managed by that mediacenter | 

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
**409** | Duplicate Entity/Node conflict (Node with same name exists) |  -  |
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

