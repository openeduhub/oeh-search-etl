# edu_sharing_client.IAMV1Api

All URIs are relative to *https://stable.demo.edu-sharing.net/edu-sharing/rest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_membership**](IAMV1Api.md#add_membership) | **PUT** /iam/v1/groups/{repository}/{group}/members/{member} | Add member to the group.
[**add_node_list**](IAMV1Api.md#add_node_list) | **PUT** /iam/v1/people/{repository}/{person}/nodeList/{list}/{node} | Add a node to node a list of a user
[**change_group_profile**](IAMV1Api.md#change_group_profile) | **PUT** /iam/v1/groups/{repository}/{group}/profile | Set profile of the group.
[**change_user_avatar**](IAMV1Api.md#change_user_avatar) | **PUT** /iam/v1/people/{repository}/{person}/avatar | Set avatar of the user.
[**change_user_password**](IAMV1Api.md#change_user_password) | **PUT** /iam/v1/people/{repository}/{person}/credential | Change/Set password of the user.
[**change_user_profile**](IAMV1Api.md#change_user_profile) | **PUT** /iam/v1/people/{repository}/{person}/profile | Set profile of the user.
[**confirm_signup**](IAMV1Api.md#confirm_signup) | **PUT** /iam/v1/groups/{repository}/{group}/signup/list/{user} | put the pending user into the group
[**create_group**](IAMV1Api.md#create_group) | **POST** /iam/v1/groups/{repository}/{group} | Create a new group.
[**create_user**](IAMV1Api.md#create_user) | **POST** /iam/v1/people/{repository}/{person} | Create a new user.
[**delete_group**](IAMV1Api.md#delete_group) | **DELETE** /iam/v1/groups/{repository}/{group} | Delete the group.
[**delete_membership**](IAMV1Api.md#delete_membership) | **DELETE** /iam/v1/groups/{repository}/{group}/members/{member} | Delete member from the group.
[**delete_user**](IAMV1Api.md#delete_user) | **DELETE** /iam/v1/people/{repository}/{person} | Delete the user.
[**get_group**](IAMV1Api.md#get_group) | **GET** /iam/v1/groups/{repository}/{group} | Get the group.
[**get_membership**](IAMV1Api.md#get_membership) | **GET** /iam/v1/groups/{repository}/{group}/members | Get all members of the group.
[**get_node_list**](IAMV1Api.md#get_node_list) | **GET** /iam/v1/people/{repository}/{person}/nodeList/{list} | Get a specific node list for a user
[**get_preferences**](IAMV1Api.md#get_preferences) | **GET** /iam/v1/people/{repository}/{person}/preferences | Get preferences stored for user
[**get_profile_settings**](IAMV1Api.md#get_profile_settings) | **GET** /iam/v1/people/{repository}/{person}/profileSettings | Get profileSettings configuration
[**get_recently_invited**](IAMV1Api.md#get_recently_invited) | **GET** /iam/v1/authorities/{repository}/recent | Get recently invited authorities.
[**get_subgroup_by_type**](IAMV1Api.md#get_subgroup_by_type) | **GET** /iam/v1/groups/{repository}/{group}/type/{type} | Get a subgroup by the specified type
[**get_user**](IAMV1Api.md#get_user) | **GET** /iam/v1/people/{repository}/{person} | Get the user.
[**get_user_groups**](IAMV1Api.md#get_user_groups) | **GET** /iam/v1/people/{repository}/{person}/memberships | Get all groups the given user is member of.
[**get_user_stats**](IAMV1Api.md#get_user_stats) | **GET** /iam/v1/people/{repository}/{person}/stats | Get the user stats.
[**reject_signup**](IAMV1Api.md#reject_signup) | **DELETE** /iam/v1/groups/{repository}/{group}/signup/list/{user} | reject the pending user
[**remove_node_list**](IAMV1Api.md#remove_node_list) | **DELETE** /iam/v1/people/{repository}/{person}/nodeList/{list}/{node} | Delete a node of a node list of a user
[**remove_user_avatar**](IAMV1Api.md#remove_user_avatar) | **DELETE** /iam/v1/people/{repository}/{person}/avatar | Remove avatar of the user.
[**search_authorities**](IAMV1Api.md#search_authorities) | **GET** /iam/v1/authorities/{repository} | Search authorities.
[**search_groups**](IAMV1Api.md#search_groups) | **GET** /iam/v1/groups/{repository} | Search groups.
[**search_user**](IAMV1Api.md#search_user) | **GET** /iam/v1/people/{repository} | Search users.
[**set_preferences**](IAMV1Api.md#set_preferences) | **PUT** /iam/v1/people/{repository}/{person}/preferences | Set preferences for user
[**set_profile_settings**](IAMV1Api.md#set_profile_settings) | **PUT** /iam/v1/people/{repository}/{person}/profileSettings | Set profileSettings Configuration
[**signup_group**](IAMV1Api.md#signup_group) | **POST** /iam/v1/groups/{repository}/{group}/signup | let the current user signup to the given group
[**signup_group_details**](IAMV1Api.md#signup_group_details) | **POST** /iam/v1/groups/{repository}/{group}/signup/config |  requires admin rights
[**signup_group_list**](IAMV1Api.md#signup_group_list) | **GET** /iam/v1/groups/{repository}/{group}/signup/list | list pending users that want to join this group
[**update_user_status**](IAMV1Api.md#update_user_status) | **PUT** /iam/v1/people/{repository}/{person}/status/{status} | update the user status.


# **add_membership**
> add_membership(repository, group, member)

Add member to the group.

Add member to the group. (admin rights are required.)

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
    api_instance = edu_sharing_client.IAMV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    group = 'group_example' # str | groupname
    member = 'member_example' # str | authorityName of member

    try:
        # Add member to the group.
        api_instance.add_membership(repository, group, member)
    except Exception as e:
        print("Exception when calling IAMV1Api->add_membership: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **group** | **str**| groupname | 
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
**409** | Duplicate Entity/Node conflict (Node with same name exists) |  -  |
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_node_list**
> add_node_list(repository, person, list, node)

Add a node to node a list of a user

For guest users, the list will be temporary stored in the current session

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
    api_instance = edu_sharing_client.IAMV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    person = '-me-' # str | username (or \"-me-\" for current user) (default to '-me-')
    list = 'list_example' # str | list name. If this list does not exist, it will be created
    node = 'node_example' # str | ID of node

    try:
        # Add a node to node a list of a user
        api_instance.add_node_list(repository, person, list, node)
    except Exception as e:
        print("Exception when calling IAMV1Api->add_node_list: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **person** | **str**| username (or \&quot;-me-\&quot; for current user) | [default to &#39;-me-&#39;]
 **list** | **str**| list name. If this list does not exist, it will be created | 
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

# **change_group_profile**
> change_group_profile(repository, group, group_profile)

Set profile of the group.

Set profile of the group. (admin rights are required.)

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.group_profile import GroupProfile
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
    api_instance = edu_sharing_client.IAMV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    group = 'group_example' # str | groupname
    group_profile = edu_sharing_client.GroupProfile() # GroupProfile | properties

    try:
        # Set profile of the group.
        api_instance.change_group_profile(repository, group, group_profile)
    except Exception as e:
        print("Exception when calling IAMV1Api->change_group_profile: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **group** | **str**| groupname | 
 **group_profile** | [**GroupProfile**](GroupProfile.md)| properties | 

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

# **change_user_avatar**
> change_user_avatar(repository, person, avatar)

Set avatar of the user.

Set avatar of the user. (To set foreign avatars, admin rights are required.)

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
    api_instance = edu_sharing_client.IAMV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    person = '-me-' # str | username (or \"-me-\" for current user) (default to '-me-')
    avatar = None # object | avatar image

    try:
        # Set avatar of the user.
        api_instance.change_user_avatar(repository, person, avatar)
    except Exception as e:
        print("Exception when calling IAMV1Api->change_user_avatar: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **person** | **str**| username (or \&quot;-me-\&quot; for current user) | [default to &#39;-me-&#39;]
 **avatar** | [**object**](object.md)| avatar image | 

### Return type

void (empty response body)

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

# **change_user_password**
> change_user_password(repository, person, user_credential)

Change/Set password of the user.

Change/Set password of the user. (To change foreign passwords or set passwords, admin rights are required.)

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.user_credential import UserCredential
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
    api_instance = edu_sharing_client.IAMV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    person = '-me-' # str | username (or \"-me-\" for current user) (default to '-me-')
    user_credential = edu_sharing_client.UserCredential() # UserCredential | credential

    try:
        # Change/Set password of the user.
        api_instance.change_user_password(repository, person, user_credential)
    except Exception as e:
        print("Exception when calling IAMV1Api->change_user_password: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **person** | **str**| username (or \&quot;-me-\&quot; for current user) | [default to &#39;-me-&#39;]
 **user_credential** | [**UserCredential**](UserCredential.md)| credential | 

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

# **change_user_profile**
> change_user_profile(repository, person, user_profile_edit)

Set profile of the user.

Set profile of the user. (To set foreign profiles, admin rights are required.)

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.user_profile_edit import UserProfileEdit
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
    api_instance = edu_sharing_client.IAMV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    person = '-me-' # str | username (or \"-me-\" for current user) (default to '-me-')
    user_profile_edit = edu_sharing_client.UserProfileEdit() # UserProfileEdit | properties

    try:
        # Set profile of the user.
        api_instance.change_user_profile(repository, person, user_profile_edit)
    except Exception as e:
        print("Exception when calling IAMV1Api->change_user_profile: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **person** | **str**| username (or \&quot;-me-\&quot; for current user) | [default to &#39;-me-&#39;]
 **user_profile_edit** | [**UserProfileEdit**](UserProfileEdit.md)| properties | 

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

# **confirm_signup**
> str confirm_signup(repository, group, user)

put the pending user into the group

Requires admin rights or org administrator on this group

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
    api_instance = edu_sharing_client.IAMV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    group = 'group_example' # str | ID of group
    user = 'user_example' # str | ID of user

    try:
        # put the pending user into the group
        api_response = api_instance.confirm_signup(repository, group, user)
        print("The response of IAMV1Api->confirm_signup:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IAMV1Api->confirm_signup: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **group** | **str**| ID of group | 
 **user** | **str**| ID of user | 

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

# **create_group**
> Group create_group(repository, group, group_profile, parent=parent)

Create a new group.

Create a new group. (admin rights are required.)

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.group import Group
from edu_sharing_client.models.group_profile import GroupProfile
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
    api_instance = edu_sharing_client.IAMV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    group = 'group_example' # str | groupname
    group_profile = edu_sharing_client.GroupProfile() # GroupProfile | properties
    parent = 'parent_example' # str | parent (will be added to this parent, also for name hashing), may be null (optional)

    try:
        # Create a new group.
        api_response = api_instance.create_group(repository, group, group_profile, parent=parent)
        print("The response of IAMV1Api->create_group:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IAMV1Api->create_group: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **group** | **str**| groupname | 
 **group_profile** | [**GroupProfile**](GroupProfile.md)| properties | 
 **parent** | **str**| parent (will be added to this parent, also for name hashing), may be null | [optional] 

### Return type

[**Group**](Group.md)

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

# **create_user**
> User create_user(repository, person, user_profile_edit, password=password)

Create a new user.

Create a new user. (admin rights are required.)

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.user import User
from edu_sharing_client.models.user_profile_edit import UserProfileEdit
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
    api_instance = edu_sharing_client.IAMV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    person = 'person_example' # str | username
    user_profile_edit = edu_sharing_client.UserProfileEdit() # UserProfileEdit | profile
    password = 'password_example' # str | Password, leave empty if you don't want to set any (optional)

    try:
        # Create a new user.
        api_response = api_instance.create_user(repository, person, user_profile_edit, password=password)
        print("The response of IAMV1Api->create_user:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IAMV1Api->create_user: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **person** | **str**| username | 
 **user_profile_edit** | [**UserProfileEdit**](UserProfileEdit.md)| profile | 
 **password** | **str**| Password, leave empty if you don&#39;t want to set any | [optional] 

### Return type

[**User**](User.md)

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

# **delete_group**
> delete_group(repository, group)

Delete the group.

Delete the group. (admin rights are required.)

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
    api_instance = edu_sharing_client.IAMV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    group = 'group_example' # str | groupname

    try:
        # Delete the group.
        api_instance.delete_group(repository, group)
    except Exception as e:
        print("Exception when calling IAMV1Api->delete_group: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **group** | **str**| groupname | 

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

# **delete_membership**
> delete_membership(repository, group, member)

Delete member from the group.

Delete member from the group. (admin rights are required.)

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
    api_instance = edu_sharing_client.IAMV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    group = 'group_example' # str | groupname
    member = 'member_example' # str | authorityName of member

    try:
        # Delete member from the group.
        api_instance.delete_membership(repository, group, member)
    except Exception as e:
        print("Exception when calling IAMV1Api->delete_membership: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **group** | **str**| groupname | 
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

# **delete_user**
> delete_user(repository, person, force=force)

Delete the user.

Delete the user. (admin rights are required.)

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
    api_instance = edu_sharing_client.IAMV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    person = 'person_example' # str | username
    force = False # bool | force the deletion (if false then only persons which are previously marked for deletion are getting deleted) (optional) (default to False)

    try:
        # Delete the user.
        api_instance.delete_user(repository, person, force=force)
    except Exception as e:
        print("Exception when calling IAMV1Api->delete_user: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **person** | **str**| username | 
 **force** | **bool**| force the deletion (if false then only persons which are previously marked for deletion are getting deleted) | [optional] [default to False]

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

# **get_group**
> GroupEntry get_group(repository, group)

Get the group.

Get the group. (To get foreign profiles, admin rights are required.)

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.group_entry import GroupEntry
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
    api_instance = edu_sharing_client.IAMV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    group = 'group_example' # str | groupname

    try:
        # Get the group.
        api_response = api_instance.get_group(repository, group)
        print("The response of IAMV1Api->get_group:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IAMV1Api->get_group: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **group** | **str**| groupname | 

### Return type

[**GroupEntry**](GroupEntry.md)

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

# **get_membership**
> AuthorityEntries get_membership(repository, group, pattern=pattern, authority_type=authority_type, max_items=max_items, skip_count=skip_count, sort_properties=sort_properties, sort_ascending=sort_ascending)

Get all members of the group.

Get all members of the group. (admin rights are required.)

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.authority_entries import AuthorityEntries
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
    api_instance = edu_sharing_client.IAMV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    group = 'group_example' # str | authority name (begins with GROUP_)
    pattern = 'pattern_example' # str | pattern (optional)
    authority_type = 'authority_type_example' # str | authorityType either GROUP or USER, empty to show all (optional)
    max_items = 10 # int | maximum items per page (optional) (default to 10)
    skip_count = 0 # int | skip a number of items (optional) (default to 0)
    sort_properties = ['sort_properties_example'] # List[str] | sort properties (optional)
    sort_ascending = [True] # List[bool] | sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index (optional)

    try:
        # Get all members of the group.
        api_response = api_instance.get_membership(repository, group, pattern=pattern, authority_type=authority_type, max_items=max_items, skip_count=skip_count, sort_properties=sort_properties, sort_ascending=sort_ascending)
        print("The response of IAMV1Api->get_membership:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IAMV1Api->get_membership: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **group** | **str**| authority name (begins with GROUP_) | 
 **pattern** | **str**| pattern | [optional] 
 **authority_type** | **str**| authorityType either GROUP or USER, empty to show all | [optional] 
 **max_items** | **int**| maximum items per page | [optional] [default to 10]
 **skip_count** | **int**| skip a number of items | [optional] [default to 0]
 **sort_properties** | [**List[str]**](str.md)| sort properties | [optional] 
 **sort_ascending** | [**List[bool]**](bool.md)| sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index | [optional] 

### Return type

[**AuthorityEntries**](AuthorityEntries.md)

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

# **get_node_list**
> NodeEntries get_node_list(repository, person, list, property_filter=property_filter, sort_properties=sort_properties, sort_ascending=sort_ascending)

Get a specific node list for a user

For guest users, the list will be temporary stored in the current session

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
    api_instance = edu_sharing_client.IAMV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    person = '-me-' # str | username (or \"-me-\" for current user) (default to '-me-')
    list = 'list_example' # str | list name
    property_filter = ['property_filter_example'] # List[str] | property filter for result nodes (or \"-all-\" for all properties) (optional)
    sort_properties = ['sort_properties_example'] # List[str] | sort properties (optional)
    sort_ascending = [True] # List[bool] | sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index (optional)

    try:
        # Get a specific node list for a user
        api_response = api_instance.get_node_list(repository, person, list, property_filter=property_filter, sort_properties=sort_properties, sort_ascending=sort_ascending)
        print("The response of IAMV1Api->get_node_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IAMV1Api->get_node_list: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **person** | **str**| username (or \&quot;-me-\&quot; for current user) | [default to &#39;-me-&#39;]
 **list** | **str**| list name | 
 **property_filter** | [**List[str]**](str.md)| property filter for result nodes (or \&quot;-all-\&quot; for all properties) | [optional] 
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

# **get_preferences**
> Preferences get_preferences(repository, person)

Get preferences stored for user

Will fail for guest

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.preferences import Preferences
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
    api_instance = edu_sharing_client.IAMV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    person = '-me-' # str | username (or \"-me-\" for current user) (default to '-me-')

    try:
        # Get preferences stored for user
        api_response = api_instance.get_preferences(repository, person)
        print("The response of IAMV1Api->get_preferences:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IAMV1Api->get_preferences: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **person** | **str**| username (or \&quot;-me-\&quot; for current user) | [default to &#39;-me-&#39;]

### Return type

[**Preferences**](Preferences.md)

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

# **get_profile_settings**
> ProfileSettings get_profile_settings(repository, person)

Get profileSettings configuration

Will fail for guest

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.profile_settings import ProfileSettings
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
    api_instance = edu_sharing_client.IAMV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    person = '-me-' # str | username (or \"-me-\" for current user) (default to '-me-')

    try:
        # Get profileSettings configuration
        api_response = api_instance.get_profile_settings(repository, person)
        print("The response of IAMV1Api->get_profile_settings:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IAMV1Api->get_profile_settings: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **person** | **str**| username (or \&quot;-me-\&quot; for current user) | [default to &#39;-me-&#39;]

### Return type

[**ProfileSettings**](ProfileSettings.md)

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

# **get_recently_invited**
> AuthorityEntries get_recently_invited(repository)

Get recently invited authorities.

Get the authorities the current user has recently invited.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.authority_entries import AuthorityEntries
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
    api_instance = edu_sharing_client.IAMV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')

    try:
        # Get recently invited authorities.
        api_response = api_instance.get_recently_invited(repository)
        print("The response of IAMV1Api->get_recently_invited:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IAMV1Api->get_recently_invited: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]

### Return type

[**AuthorityEntries**](AuthorityEntries.md)

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

# **get_subgroup_by_type**
> AuthorityEntries get_subgroup_by_type(repository, group, type)

Get a subgroup by the specified type

Get a subgroup by the specified type

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.authority_entries import AuthorityEntries
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
    api_instance = edu_sharing_client.IAMV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    group = 'group_example' # str | authority name of the parent/primary group (begins with GROUP_)
    type = 'type_example' # str | group type to filter for, e.g. ORG_ADMINISTRATORS

    try:
        # Get a subgroup by the specified type
        api_response = api_instance.get_subgroup_by_type(repository, group, type)
        print("The response of IAMV1Api->get_subgroup_by_type:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IAMV1Api->get_subgroup_by_type: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **group** | **str**| authority name of the parent/primary group (begins with GROUP_) | 
 **type** | **str**| group type to filter for, e.g. ORG_ADMINISTRATORS | 

### Return type

[**AuthorityEntries**](AuthorityEntries.md)

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

# **get_user**
> UserEntry get_user(repository, person)

Get the user.

Get the user. (Not all information are feteched for foreign profiles if current user is not an admin)

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.user_entry import UserEntry
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
    api_instance = edu_sharing_client.IAMV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    person = '-me-' # str | username (or \"-me-\" for current user) (default to '-me-')

    try:
        # Get the user.
        api_response = api_instance.get_user(repository, person)
        print("The response of IAMV1Api->get_user:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IAMV1Api->get_user: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **person** | **str**| username (or \&quot;-me-\&quot; for current user) | [default to &#39;-me-&#39;]

### Return type

[**UserEntry**](UserEntry.md)

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

# **get_user_groups**
> GroupEntries get_user_groups(repository, person, pattern=pattern, max_items=max_items, skip_count=skip_count, sort_properties=sort_properties, sort_ascending=sort_ascending)

Get all groups the given user is member of.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.group_entries import GroupEntries
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
    api_instance = edu_sharing_client.IAMV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    person = 'person_example' # str | authority name
    pattern = 'pattern_example' # str | pattern (optional)
    max_items = 10 # int | maximum items per page (optional) (default to 10)
    skip_count = 0 # int | skip a number of items (optional) (default to 0)
    sort_properties = ['sort_properties_example'] # List[str] | sort properties (optional)
    sort_ascending = [True] # List[bool] | sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index (optional)

    try:
        # Get all groups the given user is member of.
        api_response = api_instance.get_user_groups(repository, person, pattern=pattern, max_items=max_items, skip_count=skip_count, sort_properties=sort_properties, sort_ascending=sort_ascending)
        print("The response of IAMV1Api->get_user_groups:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IAMV1Api->get_user_groups: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **person** | **str**| authority name | 
 **pattern** | **str**| pattern | [optional] 
 **max_items** | **int**| maximum items per page | [optional] [default to 10]
 **skip_count** | **int**| skip a number of items | [optional] [default to 0]
 **sort_properties** | [**List[str]**](str.md)| sort properties | [optional] 
 **sort_ascending** | [**List[bool]**](bool.md)| sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index | [optional] 

### Return type

[**GroupEntries**](GroupEntries.md)

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

# **get_user_stats**
> UserStats get_user_stats(repository, person)

Get the user stats.

Get the user stats (e.g. publicly created material count)

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.user_stats import UserStats
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
    api_instance = edu_sharing_client.IAMV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    person = '-me-' # str | username (or \"-me-\" for current user) (default to '-me-')

    try:
        # Get the user stats.
        api_response = api_instance.get_user_stats(repository, person)
        print("The response of IAMV1Api->get_user_stats:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IAMV1Api->get_user_stats: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **person** | **str**| username (or \&quot;-me-\&quot; for current user) | [default to &#39;-me-&#39;]

### Return type

[**UserStats**](UserStats.md)

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

# **reject_signup**
> str reject_signup(repository, group, user)

reject the pending user

Requires admin rights or org administrator on this group

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
    api_instance = edu_sharing_client.IAMV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    group = 'group_example' # str | ID of group
    user = 'user_example' # str | ID of user

    try:
        # reject the pending user
        api_response = api_instance.reject_signup(repository, group, user)
        print("The response of IAMV1Api->reject_signup:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IAMV1Api->reject_signup: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **group** | **str**| ID of group | 
 **user** | **str**| ID of user | 

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

# **remove_node_list**
> remove_node_list(repository, person, list, node)

Delete a node of a node list of a user

For guest users, the list will be temporary stored in the current session

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
    api_instance = edu_sharing_client.IAMV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    person = '-me-' # str | username (or \"-me-\" for current user) (default to '-me-')
    list = 'list_example' # str | list name
    node = 'node_example' # str | ID of node

    try:
        # Delete a node of a node list of a user
        api_instance.remove_node_list(repository, person, list, node)
    except Exception as e:
        print("Exception when calling IAMV1Api->remove_node_list: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **person** | **str**| username (or \&quot;-me-\&quot; for current user) | [default to &#39;-me-&#39;]
 **list** | **str**| list name | 
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

# **remove_user_avatar**
> remove_user_avatar(repository, person)

Remove avatar of the user.

Remove avatar of the user. (To Remove foreign avatars, admin rights are required.)

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
    api_instance = edu_sharing_client.IAMV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    person = '-me-' # str | username (or \"-me-\" for current user) (default to '-me-')

    try:
        # Remove avatar of the user.
        api_instance.remove_user_avatar(repository, person)
    except Exception as e:
        print("Exception when calling IAMV1Api->remove_user_avatar: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **person** | **str**| username (or \&quot;-me-\&quot; for current user) | [default to &#39;-me-&#39;]

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

# **search_authorities**
> AuthorityEntries search_authorities(repository, pattern, var_global=var_global, group_type=group_type, signup_method=signup_method, max_items=max_items, skip_count=skip_count)

Search authorities.

Search authorities.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.authority_entries import AuthorityEntries
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
    api_instance = edu_sharing_client.IAMV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    pattern = 'pattern_example' # str | pattern
    var_global = True # bool | global search context, defaults to true, otherwise just searches for users within the organizations (optional) (default to True)
    group_type = 'group_type_example' # str | find a specific groupType (does nothing for persons) (optional)
    signup_method = 'signup_method_example' # str | find a specific signupMethod for groups (or asterisk for all including one) (does nothing for persons) (optional)
    max_items = 10 # int | maximum items per page (optional) (default to 10)
    skip_count = 0 # int | skip a number of items (optional) (default to 0)

    try:
        # Search authorities.
        api_response = api_instance.search_authorities(repository, pattern, var_global=var_global, group_type=group_type, signup_method=signup_method, max_items=max_items, skip_count=skip_count)
        print("The response of IAMV1Api->search_authorities:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IAMV1Api->search_authorities: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **pattern** | **str**| pattern | 
 **var_global** | **bool**| global search context, defaults to true, otherwise just searches for users within the organizations | [optional] [default to True]
 **group_type** | **str**| find a specific groupType (does nothing for persons) | [optional] 
 **signup_method** | **str**| find a specific signupMethod for groups (or asterisk for all including one) (does nothing for persons) | [optional] 
 **max_items** | **int**| maximum items per page | [optional] [default to 10]
 **skip_count** | **int**| skip a number of items | [optional] [default to 0]

### Return type

[**AuthorityEntries**](AuthorityEntries.md)

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

# **search_groups**
> GroupEntries search_groups(repository, pattern, group_type=group_type, signup_method=signup_method, var_global=var_global, max_items=max_items, skip_count=skip_count, sort_properties=sort_properties, sort_ascending=sort_ascending)

Search groups.

Search groups. (admin rights are required.)

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.group_entries import GroupEntries
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
    api_instance = edu_sharing_client.IAMV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    pattern = 'pattern_example' # str | pattern
    group_type = 'group_type_example' # str | find a specific groupType (optional)
    signup_method = 'signup_method_example' # str | find a specific signupMethod for groups (or asterisk for all including one) (optional)
    var_global = True # bool | global search context, defaults to true, otherwise just searches for groups within the organizations (optional) (default to True)
    max_items = 10 # int | maximum items per page (optional) (default to 10)
    skip_count = 0 # int | skip a number of items (optional) (default to 0)
    sort_properties = ['sort_properties_example'] # List[str] | sort properties (optional)
    sort_ascending = [True] # List[bool] | sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index (optional)

    try:
        # Search groups.
        api_response = api_instance.search_groups(repository, pattern, group_type=group_type, signup_method=signup_method, var_global=var_global, max_items=max_items, skip_count=skip_count, sort_properties=sort_properties, sort_ascending=sort_ascending)
        print("The response of IAMV1Api->search_groups:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IAMV1Api->search_groups: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **pattern** | **str**| pattern | 
 **group_type** | **str**| find a specific groupType | [optional] 
 **signup_method** | **str**| find a specific signupMethod for groups (or asterisk for all including one) | [optional] 
 **var_global** | **bool**| global search context, defaults to true, otherwise just searches for groups within the organizations | [optional] [default to True]
 **max_items** | **int**| maximum items per page | [optional] [default to 10]
 **skip_count** | **int**| skip a number of items | [optional] [default to 0]
 **sort_properties** | [**List[str]**](str.md)| sort properties | [optional] 
 **sort_ascending** | [**List[bool]**](bool.md)| sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index | [optional] 

### Return type

[**GroupEntries**](GroupEntries.md)

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

# **search_user**
> UserEntries search_user(repository, pattern, var_global=var_global, status=status, max_items=max_items, skip_count=skip_count, sort_properties=sort_properties, sort_ascending=sort_ascending)

Search users.

Search users. (admin rights are required.)

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.user_entries import UserEntries
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
    api_instance = edu_sharing_client.IAMV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    pattern = 'pattern_example' # str | pattern
    var_global = True # bool | global search context, defaults to true, otherwise just searches for users within the organizations (optional) (default to True)
    status = 'status_example' # str | the user status (e.g. active), if not set, all users are returned (optional)
    max_items = 10 # int | maximum items per page (optional) (default to 10)
    skip_count = 0 # int | skip a number of items (optional) (default to 0)
    sort_properties = ['sort_properties_example'] # List[str] | sort properties (optional)
    sort_ascending = [True] # List[bool] | sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index (optional)

    try:
        # Search users.
        api_response = api_instance.search_user(repository, pattern, var_global=var_global, status=status, max_items=max_items, skip_count=skip_count, sort_properties=sort_properties, sort_ascending=sort_ascending)
        print("The response of IAMV1Api->search_user:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IAMV1Api->search_user: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **pattern** | **str**| pattern | 
 **var_global** | **bool**| global search context, defaults to true, otherwise just searches for users within the organizations | [optional] [default to True]
 **status** | **str**| the user status (e.g. active), if not set, all users are returned | [optional] 
 **max_items** | **int**| maximum items per page | [optional] [default to 10]
 **skip_count** | **int**| skip a number of items | [optional] [default to 0]
 **sort_properties** | [**List[str]**](str.md)| sort properties | [optional] 
 **sort_ascending** | [**List[bool]**](bool.md)| sort ascending, true if not set. Use multiple values to change the direction according to the given property at the same index | [optional] 

### Return type

[**UserEntries**](UserEntries.md)

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

# **set_preferences**
> set_preferences(repository, person, body)

Set preferences for user

Will fail for guest

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
    api_instance = edu_sharing_client.IAMV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    person = '-me-' # str | username (or \"-me-\" for current user) (default to '-me-')
    body = 'body_example' # str | preferences (json string)

    try:
        # Set preferences for user
        api_instance.set_preferences(repository, person, body)
    except Exception as e:
        print("Exception when calling IAMV1Api->set_preferences: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **person** | **str**| username (or \&quot;-me-\&quot; for current user) | [default to &#39;-me-&#39;]
 **body** | **str**| preferences (json string) | 

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

# **set_profile_settings**
> set_profile_settings(repository, person, profile_settings)

Set profileSettings Configuration

Will fail for guest

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.profile_settings import ProfileSettings
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
    api_instance = edu_sharing_client.IAMV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    person = '-me-' # str | username (or \"-me-\" for current user) (default to '-me-')
    profile_settings = edu_sharing_client.ProfileSettings() # ProfileSettings | ProfileSetting Object

    try:
        # Set profileSettings Configuration
        api_instance.set_profile_settings(repository, person, profile_settings)
    except Exception as e:
        print("Exception when calling IAMV1Api->set_profile_settings: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **person** | **str**| username (or \&quot;-me-\&quot; for current user) | [default to &#39;-me-&#39;]
 **profile_settings** | [**ProfileSettings**](ProfileSettings.md)| ProfileSetting Object | 

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

# **signup_group**
> str signup_group(repository, group, password=password)

let the current user signup to the given group

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
    api_instance = edu_sharing_client.IAMV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    group = 'group_example' # str | ID of group
    password = 'password_example' # str | Password for signup (only required if signupMethod == password) (optional)

    try:
        # let the current user signup to the given group
        api_response = api_instance.signup_group(repository, group, password=password)
        print("The response of IAMV1Api->signup_group:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IAMV1Api->signup_group: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **group** | **str**| ID of group | 
 **password** | **str**| Password for signup (only required if signupMethod &#x3D;&#x3D; password) | [optional] 

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

# **signup_group_details**
> signup_group_details(repository, group, group_signup_details)

 requires admin rights

set group signup options

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.group_signup_details import GroupSignupDetails
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
    api_instance = edu_sharing_client.IAMV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    group = 'group_example' # str | ID of group
    group_signup_details = edu_sharing_client.GroupSignupDetails() # GroupSignupDetails | Details to edit

    try:
        #  requires admin rights
        api_instance.signup_group_details(repository, group, group_signup_details)
    except Exception as e:
        print("Exception when calling IAMV1Api->signup_group_details: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **group** | **str**| ID of group | 
 **group_signup_details** | [**GroupSignupDetails**](GroupSignupDetails.md)| Details to edit | 

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

# **signup_group_list**
> str signup_group_list(repository, group)

list pending users that want to join this group

Requires admin rights or org administrator on this group

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
    api_instance = edu_sharing_client.IAMV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    group = 'group_example' # str | ID of group

    try:
        # list pending users that want to join this group
        api_response = api_instance.signup_group_list(repository, group)
        print("The response of IAMV1Api->signup_group_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IAMV1Api->signup_group_list: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **group** | **str**| ID of group | 

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

# **update_user_status**
> update_user_status(repository, person, status, notify)

update the user status.

update the user status. (admin rights are required.)

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
    api_instance = edu_sharing_client.IAMV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    person = 'person_example' # str | username
    status = 'status_example' # str | the new status to set
    notify = True # bool | notify the user via mail (default to True)

    try:
        # update the user status.
        api_instance.update_user_status(repository, person, status, notify)
    except Exception as e:
        print("Exception when calling IAMV1Api->update_user_status: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **person** | **str**| username | 
 **status** | **str**| the new status to set | 
 **notify** | **bool**| notify the user via mail | [default to True]

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

