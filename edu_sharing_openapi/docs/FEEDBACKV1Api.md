# edu_sharing_client.FEEDBACKV1Api

All URIs are relative to *https://stable.demo.edu-sharing.net/edu-sharing/rest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_feedback**](FEEDBACKV1Api.md#add_feedback) | **PUT** /feedback/v1/feedback/{repository}/{node}/add | Give feedback on a node
[**get_feedbacks**](FEEDBACKV1Api.md#get_feedbacks) | **GET** /feedback/v1/feedback/{repository}/{node}/list | Get given feedback on a node


# **add_feedback**
> FeedbackResult add_feedback(repository, node, request_body)

Give feedback on a node

Adds feedback to the given node. Depending on the internal config, the current user will be obscured to prevent back-tracing to the original id

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.feedback_result import FeedbackResult
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
    api_instance = edu_sharing_client.FEEDBACKV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node
    request_body = None # Dict[str, List[str]] | feedback data, key/value pairs

    try:
        # Give feedback on a node
        api_response = api_instance.add_feedback(repository, node, request_body)
        print("The response of FEEDBACKV1Api->add_feedback:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FEEDBACKV1Api->add_feedback: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 
 **request_body** | [**Dict[str, List[str]]**](List.md)| feedback data, key/value pairs | 

### Return type

[**FeedbackResult**](FeedbackResult.md)

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

# **get_feedbacks**
> List[FeedbackData] get_feedbacks(repository, node)

Get given feedback on a node

Get all given feedback for a node. Requires Coordinator permissions on node

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.feedback_data import FeedbackData
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
    api_instance = edu_sharing_client.FEEDBACKV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node

    try:
        # Get given feedback on a node
        api_response = api_instance.get_feedbacks(repository, node)
        print("The response of FEEDBACKV1Api->get_feedbacks:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FEEDBACKV1Api->get_feedbacks: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 

### Return type

[**List[FeedbackData]**](FeedbackData.md)

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

