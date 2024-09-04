# edu_sharing_client.ORGANIZATIONV1Api

All URIs are relative to *https://stable.demo.edu-sharing.net/edu-sharing/rest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_organizations**](ORGANIZATIONV1Api.md#create_organizations) | **PUT** /organization/v1/organizations/{repository}/{organization} | create organization in repository.
[**delete_organizations**](ORGANIZATIONV1Api.md#delete_organizations) | **DELETE** /organization/v1/organizations/{repository}/{organization} | Delete organization of repository.
[**get_organization**](ORGANIZATIONV1Api.md#get_organization) | **GET** /organization/v1/organizations/{repository}/{organization} | Get organization by id.
[**get_organizations**](ORGANIZATIONV1Api.md#get_organizations) | **GET** /organization/v1/organizations/{repository} | Get organizations of repository.
[**remove_from_organization**](ORGANIZATIONV1Api.md#remove_from_organization) | **DELETE** /organization/v1/organizations/{repository}/{organization}/member/{member} | Remove member from organization.


# **create_organizations**
> Organization create_organizations(repository, organization, eduscope=eduscope)

create organization in repository.

create organization in repository.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.organization import Organization
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
    api_instance = edu_sharing_client.ORGANIZATIONV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    organization = 'organization_example' # str | organization name
    eduscope = 'eduscope_example' # str | eduscope (may be null) (optional)

    try:
        # create organization in repository.
        api_response = api_instance.create_organizations(repository, organization, eduscope=eduscope)
        print("The response of ORGANIZATIONV1Api->create_organizations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ORGANIZATIONV1Api->create_organizations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **organization** | **str**| organization name | 
 **eduscope** | **str**| eduscope (may be null) | [optional] 

### Return type

[**Organization**](Organization.md)

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

# **delete_organizations**
> delete_organizations(repository, organization)

Delete organization of repository.

Delete organization of repository.

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
    api_instance = edu_sharing_client.ORGANIZATIONV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    organization = 'organization_example' # str | groupname

    try:
        # Delete organization of repository.
        api_instance.delete_organizations(repository, organization)
    except Exception as e:
        print("Exception when calling ORGANIZATIONV1Api->delete_organizations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **organization** | **str**| groupname | 

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

# **get_organization**
> Organization get_organization(repository, organization)

Get organization by id.

Get organization by id.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.organization import Organization
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
    api_instance = edu_sharing_client.ORGANIZATIONV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    organization = 'organization_example' # str | ID of organization

    try:
        # Get organization by id.
        api_response = api_instance.get_organization(repository, organization)
        print("The response of ORGANIZATIONV1Api->get_organization:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ORGANIZATIONV1Api->get_organization: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **organization** | **str**| ID of organization | 

### Return type

[**Organization**](Organization.md)

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

# **get_organizations**
> OrganizationEntries get_organizations(repository, pattern=pattern, max_items=max_items, skip_count=skip_count, sort_properties=sort_properties, sort_ascending=sort_ascending, only_memberships=only_memberships)

Get organizations of repository.

Get organizations of repository the current user is member. May returns an empty list.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.organization_entries import OrganizationEntries
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
    api_instance = edu_sharing_client.ORGANIZATIONV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    pattern = 'pattern_example' # str | pattern (optional)
    max_items = 10 # int | maximum items per page (optional) (default to 10)
    skip_count = 0 # int | skip a number of items (optional) (default to 0)
    sort_properties = ['sort_properties_example'] # List[str] | sort properties (optional)
    sort_ascending = [True] # List[bool] | sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index (optional)
    only_memberships = True # bool | search only in memberships, false can only be done by admin (optional) (default to True)

    try:
        # Get organizations of repository.
        api_response = api_instance.get_organizations(repository, pattern=pattern, max_items=max_items, skip_count=skip_count, sort_properties=sort_properties, sort_ascending=sort_ascending, only_memberships=only_memberships)
        print("The response of ORGANIZATIONV1Api->get_organizations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ORGANIZATIONV1Api->get_organizations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **pattern** | **str**| pattern | [optional] 
 **max_items** | **int**| maximum items per page | [optional] [default to 10]
 **skip_count** | **int**| skip a number of items | [optional] [default to 0]
 **sort_properties** | [**List[str]**](str.md)| sort properties | [optional] 
 **sort_ascending** | [**List[bool]**](bool.md)| sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index | [optional] 
 **only_memberships** | **bool**| search only in memberships, false can only be done by admin | [optional] [default to True]

### Return type

[**OrganizationEntries**](OrganizationEntries.md)

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

# **remove_from_organization**
> remove_from_organization(repository, organization, member)

Remove member from organization.

Remove member from organization.

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
    api_instance = edu_sharing_client.ORGANIZATIONV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    organization = 'organization_example' # str | groupname
    member = 'member_example' # str | authorityName of member

    try:
        # Remove member from organization.
        api_instance.remove_from_organization(repository, organization, member)
    except Exception as e:
        print("Exception when calling ORGANIZATIONV1Api->remove_from_organization: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **organization** | **str**| groupname | 
 **member** | **str**| authorityName of member | 

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

