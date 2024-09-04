# edu_sharing_client.KNOWLEDGEV1Api

All URIs are relative to *https://stable.demo.edu-sharing.net/edu-sharing/rest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_analyzing_job_status**](KNOWLEDGEV1Api.md#get_analyzing_job_status) | **GET** /knowledge/v1/analyze/jobs/{job} | Get analyzing job status.
[**run_analyzing_job**](KNOWLEDGEV1Api.md#run_analyzing_job) | **POST** /knowledge/v1/analyze/jobs | Run analyzing job.


# **get_analyzing_job_status**
> JobEntry get_analyzing_job_status(job)

Get analyzing job status.

Get analyzing job status.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.job_entry import JobEntry
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
    api_instance = edu_sharing_client.KNOWLEDGEV1Api(api_client)
    job = 'job_example' # str | ID of job ticket

    try:
        # Get analyzing job status.
        api_response = api_instance.get_analyzing_job_status(job)
        print("The response of KNOWLEDGEV1Api->get_analyzing_job_status:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling KNOWLEDGEV1Api->get_analyzing_job_status: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **job** | **str**| ID of job ticket | 

### Return type

[**JobEntry**](JobEntry.md)

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
**403** | The current user has insufficient rights to access the ticket. |  -  |
**404** | Job not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **run_analyzing_job**
> JobEntry run_analyzing_job(repository, node)

Run analyzing job.

Run analyzing job for a node.

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.job_entry import JobEntry
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
    api_instance = edu_sharing_client.KNOWLEDGEV1Api(api_client)
    repository = '-home-' # str | ID of repository (or \"-home-\" for home repository) (default to '-home-')
    node = 'node_example' # str | ID of node

    try:
        # Run analyzing job.
        api_response = api_instance.run_analyzing_job(repository, node)
        print("The response of KNOWLEDGEV1Api->run_analyzing_job:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling KNOWLEDGEV1Api->run_analyzing_job: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository** | **str**| ID of repository (or \&quot;-home-\&quot; for home repository) | [default to &#39;-home-&#39;]
 **node** | **str**| ID of node | 

### Return type

[**JobEntry**](JobEntry.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**202** | Accepted. |  -  |
**401** | Authorization failed. |  -  |
**403** | The current user has insufficient rights to read the node or to perform an analyzing job. |  -  |
**404** | Repository or node not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

