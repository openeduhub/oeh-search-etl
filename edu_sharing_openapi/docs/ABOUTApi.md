# edu_sharing_client.ABOUTApi

All URIs are relative to *https://stable.demo.edu-sharing.net/edu-sharing/rest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**about**](ABOUTApi.md#about) | **GET** /_about | Discover the API.
[**licenses**](ABOUTApi.md#licenses) | **GET** /_about/licenses | License information.
[**status**](ABOUTApi.md#status) | **GET** /_about/status/{mode} | status of repo services


# **about**
> About about()

Discover the API.

Get all services provided by this API.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.about import About
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
    api_instance = edu_sharing_client.ABOUTApi(api_client)

    try:
        # Discover the API.
        api_response = api_instance.about()
        print("The response of ABOUTApi->about:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ABOUTApi->about: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**About**](About.md)

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

# **licenses**
> Licenses licenses()

License information.

Get information about used 3rd-party licenses.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.licenses import Licenses
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
    api_instance = edu_sharing_client.ABOUTApi(api_client)

    try:
        # License information.
        api_response = api_instance.licenses()
        print("The response of ABOUTApi->licenses:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ABOUTApi->licenses: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**Licenses**](Licenses.md)

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

# **status**
> str status(mode, timeout_seconds=timeout_seconds)

status of repo services

returns http status 200 when ok

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
    api_instance = edu_sharing_client.ABOUTApi(api_client)
    mode = 'mode_example' # str | 
    timeout_seconds = 10 # int |  (optional) (default to 10)

    try:
        # status of repo services
        api_response = api_instance.status(mode, timeout_seconds=timeout_seconds)
        print("The response of ABOUTApi->status:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ABOUTApi->status: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **mode** | **str**|  | 
 **timeout_seconds** | **int**|  | [optional] [default to 10]

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

