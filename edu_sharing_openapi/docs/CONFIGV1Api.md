# edu_sharing_client.CONFIGV1Api

All URIs are relative to *https://stable.demo.edu-sharing.net/edu-sharing/rest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_config1**](CONFIGV1Api.md#get_config1) | **GET** /config/v1/values | get repository config values
[**get_dynamic_value**](CONFIGV1Api.md#get_dynamic_value) | **GET** /config/v1/dynamic/{key} | Get a config entry (appropriate rights for the entry are required)
[**get_language**](CONFIGV1Api.md#get_language) | **GET** /config/v1/language | get override strings for the current language
[**get_language_defaults**](CONFIGV1Api.md#get_language_defaults) | **GET** /config/v1/language/defaults | get all inital language strings for angular
[**get_variables**](CONFIGV1Api.md#get_variables) | **GET** /config/v1/variables | get global config variables
[**set_dynamic_value**](CONFIGV1Api.md#set_dynamic_value) | **POST** /config/v1/dynamic/{key} | Set a config entry (admin rights required)


# **get_config1**
> Config get_config1()

get repository config values

Current is the actual (context-based) active config. Global is the default global config if no context is active (may be identical to the current)

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.config import Config
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
    api_instance = edu_sharing_client.CONFIGV1Api(api_client)

    try:
        # get repository config values
        api_response = api_instance.get_config1()
        print("The response of CONFIGV1Api->get_config1:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CONFIGV1Api->get_config1: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**Config**](Config.md)

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

# **get_dynamic_value**
> DynamicConfig get_dynamic_value(key)

Get a config entry (appropriate rights for the entry are required)

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.dynamic_config import DynamicConfig
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
    api_instance = edu_sharing_client.CONFIGV1Api(api_client)
    key = 'key_example' # str | Key of the config value that should be fetched

    try:
        # Get a config entry (appropriate rights for the entry are required)
        api_response = api_instance.get_dynamic_value(key)
        print("The response of CONFIGV1Api->get_dynamic_value:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CONFIGV1Api->get_dynamic_value: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **str**| Key of the config value that should be fetched | 

### Return type

[**DynamicConfig**](DynamicConfig.md)

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

# **get_language**
> Language get_language()

get override strings for the current language

Language strings

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.language import Language
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
    api_instance = edu_sharing_client.CONFIGV1Api(api_client)

    try:
        # get override strings for the current language
        api_response = api_instance.get_language()
        print("The response of CONFIGV1Api->get_language:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CONFIGV1Api->get_language: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**Language**](Language.md)

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

# **get_language_defaults**
> str get_language_defaults()

get all inital language strings for angular

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
    api_instance = edu_sharing_client.CONFIGV1Api(api_client)

    try:
        # get all inital language strings for angular
        api_response = api_instance.get_language_defaults()
        print("The response of CONFIGV1Api->get_language_defaults:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CONFIGV1Api->get_language_defaults: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

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

# **get_variables**
> Variables get_variables()

get global config variables

global config variables

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.variables import Variables
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
    api_instance = edu_sharing_client.CONFIGV1Api(api_client)

    try:
        # get global config variables
        api_response = api_instance.get_variables()
        print("The response of CONFIGV1Api->get_variables:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CONFIGV1Api->get_variables: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**Variables**](Variables.md)

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

# **set_dynamic_value**
> DynamicConfig set_dynamic_value(key, public, body)

Set a config entry (admin rights required)

the body must be a json encapsulated string

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.dynamic_config import DynamicConfig
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
    api_instance = edu_sharing_client.CONFIGV1Api(api_client)
    key = 'key_example' # str | Key of the config value that should be fetched
    public = True # bool | Is everyone allowed to read the value
    body = 'body_example' # str | Must be a json-encapsulated string

    try:
        # Set a config entry (admin rights required)
        api_response = api_instance.set_dynamic_value(key, public, body)
        print("The response of CONFIGV1Api->set_dynamic_value:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CONFIGV1Api->set_dynamic_value: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **str**| Key of the config value that should be fetched | 
 **public** | **bool**| Is everyone allowed to read the value | 
 **body** | **str**| Must be a json-encapsulated string | 

### Return type

[**DynamicConfig**](DynamicConfig.md)

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

