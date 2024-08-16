# edu_sharing_client.CLIENTUTILSV1Api

All URIs are relative to *https://stable.demo.edu-sharing.net/edu-sharing/rest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_website_information**](CLIENTUTILSV1Api.md#get_website_information) | **GET** /clientUtils/v1/getWebsiteInformation | Read generic information about a webpage


# **get_website_information**
> WebsiteInformation get_website_information(url=url)

Read generic information about a webpage

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.website_information import WebsiteInformation
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
    api_instance = edu_sharing_client.CLIENTUTILSV1Api(api_client)
    url = 'url_example' # str | full url with http or https (optional)

    try:
        # Read generic information about a webpage
        api_response = api_instance.get_website_information(url=url)
        print("The response of CLIENTUTILSV1Api->get_website_information:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CLIENTUTILSV1Api->get_website_information: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **url** | **str**| full url with http or https | [optional] 

### Return type

[**WebsiteInformation**](WebsiteInformation.md)

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

