# edu_sharing_client.REGISTERV1Api

All URIs are relative to *https://stable.demo.edu-sharing.net/edu-sharing/rest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**activate**](REGISTERV1Api.md#activate) | **POST** /register/v1/activate/{key} | Activate a new user (by using a supplied key)
[**mail_exists**](REGISTERV1Api.md#mail_exists) | **GET** /register/v1/exists/{mail} | Check if the given mail is already successfully registered
[**recover_password**](REGISTERV1Api.md#recover_password) | **POST** /register/v1/recover/{mail} | Send a mail to recover/reset password
[**register**](REGISTERV1Api.md#register) | **POST** /register/v1/register | Register a new user
[**resend_mail**](REGISTERV1Api.md#resend_mail) | **POST** /register/v1/resend/{mail} | Resend a registration mail for a given mail address
[**reset_password**](REGISTERV1Api.md#reset_password) | **POST** /register/v1/reset/{key}/{password} | Send a mail to recover/reset password


# **activate**
> activate(key)

Activate a new user (by using a supplied key)

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
    api_instance = edu_sharing_client.REGISTERV1Api(api_client)
    key = 'key_example' # str | The key for the user to activate

    try:
        # Activate a new user (by using a supplied key)
        api_instance.activate(key)
    except Exception as e:
        print("Exception when calling REGISTERV1Api->activate: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **str**| The key for the user to activate | 

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

# **mail_exists**
> RegisterExists mail_exists(mail)

Check if the given mail is already successfully registered

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.register_exists import RegisterExists
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
    api_instance = edu_sharing_client.REGISTERV1Api(api_client)
    mail = 'mail_example' # str | The mail (authority) of the user to check

    try:
        # Check if the given mail is already successfully registered
        api_response = api_instance.mail_exists(mail)
        print("The response of REGISTERV1Api->mail_exists:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling REGISTERV1Api->mail_exists: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **mail** | **str**| The mail (authority) of the user to check | 

### Return type

[**RegisterExists**](RegisterExists.md)

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

# **recover_password**
> recover_password(mail)

Send a mail to recover/reset password

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
    api_instance = edu_sharing_client.REGISTERV1Api(api_client)
    mail = 'mail_example' # str | The mail (authority) of the user to recover

    try:
        # Send a mail to recover/reset password
        api_instance.recover_password(mail)
    except Exception as e:
        print("Exception when calling REGISTERV1Api->recover_password: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **mail** | **str**| The mail (authority) of the user to recover | 

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

# **register**
> register(register_information=register_information)

Register a new user

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.register_information import RegisterInformation
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
    api_instance = edu_sharing_client.REGISTERV1Api(api_client)
    register_information = edu_sharing_client.RegisterInformation() # RegisterInformation |  (optional)

    try:
        # Register a new user
        api_instance.register(register_information=register_information)
    except Exception as e:
        print("Exception when calling REGISTERV1Api->register: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **register_information** | [**RegisterInformation**](RegisterInformation.md)|  | [optional] 

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
**500** | Fatal error occured. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resend_mail**
> resend_mail(mail)

Resend a registration mail for a given mail address

The method will return false if there is no pending registration for the given mail

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
    api_instance = edu_sharing_client.REGISTERV1Api(api_client)
    mail = 'mail_example' # str | The mail a registration is pending for and should be resend to

    try:
        # Resend a registration mail for a given mail address
        api_instance.resend_mail(mail)
    except Exception as e:
        print("Exception when calling REGISTERV1Api->resend_mail: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **mail** | **str**| The mail a registration is pending for and should be resend to | 

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

# **reset_password**
> reset_password(key, password)

Send a mail to recover/reset password

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
    api_instance = edu_sharing_client.REGISTERV1Api(api_client)
    key = 'key_example' # str | The key for the password reset request
    password = 'password_example' # str | The new password for the user

    try:
        # Send a mail to recover/reset password
        api_instance.reset_password(key, password)
    except Exception as e:
        print("Exception when calling REGISTERV1Api->reset_password: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **str**| The key for the password reset request | 
 **password** | **str**| The new password for the user | 

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

