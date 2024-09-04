# edu_sharing_client.AUTHENTICATIONV1Api

All URIs are relative to *https://stable.demo.edu-sharing.net/edu-sharing/rest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**authenticate**](AUTHENTICATIONV1Api.md#authenticate) | **POST** /authentication/v1/appauth/{userId} | authenticate user of an registered application.
[**has_access_to_scope**](AUTHENTICATIONV1Api.md#has_access_to_scope) | **GET** /authentication/v1/hasAccessToScope | Returns true if the current user has access to the given scope
[**login**](AUTHENTICATIONV1Api.md#login) | **GET** /authentication/v1/validateSession | Validates the Basic Auth Credentials and check if the session is a logged in user
[**login_to_scope**](AUTHENTICATIONV1Api.md#login_to_scope) | **POST** /authentication/v1/loginToScope | Validates the Basic Auth Credentials and check if the session is a logged in user
[**logout**](AUTHENTICATIONV1Api.md#logout) | **GET** /authentication/v1/destroySession | Destroys the current session and logout the user


# **authenticate**
> AuthenticationToken authenticate(user_id, user_profile_app_auth=user_profile_app_auth)

authenticate user of an registered application.

headers must be set: X-Edu-App-Id, X-Edu-App-Sig, X-Edu-App-Signed, X-Edu-App-Ts

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.authentication_token import AuthenticationToken
from edu_sharing_client.models.user_profile_app_auth import UserProfileAppAuth
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
    api_instance = edu_sharing_client.AUTHENTICATIONV1Api(api_client)
    user_id = 'user_id_example' # str | User Id
    user_profile_app_auth = edu_sharing_client.UserProfileAppAuth() # UserProfileAppAuth | User Profile (optional)

    try:
        # authenticate user of an registered application.
        api_response = api_instance.authenticate(user_id, user_profile_app_auth=user_profile_app_auth)
        print("The response of AUTHENTICATIONV1Api->authenticate:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AUTHENTICATIONV1Api->authenticate: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| User Id | 
 **user_profile_app_auth** | [**UserProfileAppAuth**](UserProfileAppAuth.md)| User Profile | [optional] 

### Return type

[**AuthenticationToken**](AuthenticationToken.md)

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

# **has_access_to_scope**
> has_access_to_scope(scope)

Returns true if the current user has access to the given scope

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
    api_instance = edu_sharing_client.AUTHENTICATIONV1Api(api_client)
    scope = 'scope_example' # str | scope

    try:
        # Returns true if the current user has access to the given scope
        api_instance.has_access_to_scope(scope)
    except Exception as e:
        print("Exception when calling AUTHENTICATIONV1Api->has_access_to_scope: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scope** | **str**| scope | 

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
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **login**
> Login login()

Validates the Basic Auth Credentials and check if the session is a logged in user

Use the Basic auth header field to transfer the credentials

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.login import Login
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
    api_instance = edu_sharing_client.AUTHENTICATIONV1Api(api_client)

    try:
        # Validates the Basic Auth Credentials and check if the session is a logged in user
        api_response = api_instance.login()
        print("The response of AUTHENTICATIONV1Api->login:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AUTHENTICATIONV1Api->login: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**Login**](Login.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **login_to_scope**
> Login login_to_scope(login_credentials)

Validates the Basic Auth Credentials and check if the session is a logged in user

Use the Basic auth header field to transfer the credentials

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.login import Login
from edu_sharing_client.models.login_credentials import LoginCredentials
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
    api_instance = edu_sharing_client.AUTHENTICATIONV1Api(api_client)
    login_credentials = edu_sharing_client.LoginCredentials() # LoginCredentials | credentials, example: test,test

    try:
        # Validates the Basic Auth Credentials and check if the session is a logged in user
        api_response = api_instance.login_to_scope(login_credentials)
        print("The response of AUTHENTICATIONV1Api->login_to_scope:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AUTHENTICATIONV1Api->login_to_scope: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **login_credentials** | [**LoginCredentials**](LoginCredentials.md)| credentials, example: test,test | 

### Return type

[**Login**](Login.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **logout**
> logout()

Destroys the current session and logout the user

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
    api_instance = edu_sharing_client.AUTHENTICATIONV1Api(api_client)

    try:
        # Destroys the current session and logout the user
        api_instance.logout()
    except Exception as e:
        print("Exception when calling AUTHENTICATIONV1Api->logout: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

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
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

