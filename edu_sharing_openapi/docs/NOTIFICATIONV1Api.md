# edu_sharing_client.NOTIFICATIONV1Api

All URIs are relative to *https://stable.demo.edu-sharing.net/edu-sharing/rest*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_notification**](NOTIFICATIONV1Api.md#delete_notification) | **DELETE** /notification/v1/notifications | Endpoint to delete notification by id
[**get_config2**](NOTIFICATIONV1Api.md#get_config2) | **GET** /notification/v1/config | get the config for notifications of the current user
[**get_notifications**](NOTIFICATIONV1Api.md#get_notifications) | **GET** /notification/v1/notifications | Retrieve stored notification, filtered by receiver and status
[**set_config1**](NOTIFICATIONV1Api.md#set_config1) | **PUT** /notification/v1/config | Update the config for notifications of the current user
[**update_notification_status**](NOTIFICATIONV1Api.md#update_notification_status) | **PUT** /notification/v1/notifications/status | Endpoint to update the notification status
[**update_notification_status_by_receiver_id**](NOTIFICATIONV1Api.md#update_notification_status_by_receiver_id) | **PUT** /notification/v1/notifications/receiver/status | Endpoint to update the notification status


# **delete_notification**
> delete_notification(id=id)

Endpoint to delete notification by id

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
    api_instance = edu_sharing_client.NOTIFICATIONV1Api(api_client)
    id = 'id_example' # str |  (optional)

    try:
        # Endpoint to delete notification by id
        api_instance.delete_notification(id=id)
    except Exception as e:
        print("Exception when calling NOTIFICATIONV1Api->delete_notification: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | deleted notification |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_config2**
> NotificationConfig get_config2()

get the config for notifications of the current user

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.notification_config import NotificationConfig
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
    api_instance = edu_sharing_client.NOTIFICATIONV1Api(api_client)

    try:
        # get the config for notifications of the current user
        api_response = api_instance.get_config2()
        print("The response of NOTIFICATIONV1Api->get_config2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NOTIFICATIONV1Api->get_config2: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**NotificationConfig**](NotificationConfig.md)

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

# **get_notifications**
> NotificationResponsePage get_notifications(receiver_id=receiver_id, status=status, page=page, size=size, sort=sort)

Retrieve stored notification, filtered by receiver and status

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.notification_response_page import NotificationResponsePage
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
    api_instance = edu_sharing_client.NOTIFICATIONV1Api(api_client)
    receiver_id = '-me-' # str |  (optional) (default to '-me-')
    status = ['status_example'] # List[str] | status (or conjunction) (optional)
    page = 0 # int | page number (optional) (default to 0)
    size = 25 # int | page size (optional) (default to 25)
    sort = ['sort_example'] # List[str] | Sorting criteria in the format: property(,asc|desc)(,ignoreCase). Default sort order is ascending. Multiple sort criteria are supported. (optional)

    try:
        # Retrieve stored notification, filtered by receiver and status
        api_response = api_instance.get_notifications(receiver_id=receiver_id, status=status, page=page, size=size, sort=sort)
        print("The response of NOTIFICATIONV1Api->get_notifications:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NOTIFICATIONV1Api->get_notifications: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **receiver_id** | **str**|  | [optional] [default to &#39;-me-&#39;]
 **status** | [**List[str]**](str.md)| status (or conjunction) | [optional] 
 **page** | **int**| page number | [optional] [default to 0]
 **size** | **int**| page size | [optional] [default to 25]
 **sort** | [**List[str]**](str.md)| Sorting criteria in the format: property(,asc|desc)(,ignoreCase). Default sort order is ascending. Multiple sort criteria are supported. | [optional] 

### Return type

[**NotificationResponsePage**](NotificationResponsePage.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | get the received notifications |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_config1**
> set_config1(notification_config=notification_config)

Update the config for notifications of the current user

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.notification_config import NotificationConfig
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
    api_instance = edu_sharing_client.NOTIFICATIONV1Api(api_client)
    notification_config = edu_sharing_client.NotificationConfig() # NotificationConfig |  (optional)

    try:
        # Update the config for notifications of the current user
        api_instance.set_config1(notification_config=notification_config)
    except Exception as e:
        print("Exception when calling NOTIFICATIONV1Api->set_config1: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **notification_config** | [**NotificationConfig**](NotificationConfig.md)|  | [optional] 

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

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_notification_status**
> NotificationEventDTO update_notification_status(id=id, status=status)

Endpoint to update the notification status

### Example


```python
import edu_sharing_client
from edu_sharing_client.models.notification_event_dto import NotificationEventDTO
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
    api_instance = edu_sharing_client.NOTIFICATIONV1Api(api_client)
    id = 'id_example' # str |  (optional)
    status = READ # str |  (optional) (default to READ)

    try:
        # Endpoint to update the notification status
        api_response = api_instance.update_notification_status(id=id, status=status)
        print("The response of NOTIFICATIONV1Api->update_notification_status:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NOTIFICATIONV1Api->update_notification_status: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | [optional] 
 **status** | **str**|  | [optional] [default to READ]

### Return type

[**NotificationEventDTO**](NotificationEventDTO.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | set notification status |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_notification_status_by_receiver_id**
> update_notification_status_by_receiver_id(receiver_id=receiver_id, old_status=old_status, new_status=new_status)

Endpoint to update the notification status

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
    api_instance = edu_sharing_client.NOTIFICATIONV1Api(api_client)
    receiver_id = 'receiver_id_example' # str |  (optional)
    old_status = ['old_status_example'] # List[str] | The old status (or conjunction) (optional)
    new_status = READ # str |  (optional) (default to READ)

    try:
        # Endpoint to update the notification status
        api_instance.update_notification_status_by_receiver_id(receiver_id=receiver_id, old_status=old_status, new_status=new_status)
    except Exception as e:
        print("Exception when calling NOTIFICATIONV1Api->update_notification_status_by_receiver_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **receiver_id** | **str**|  | [optional] 
 **old_status** | [**List[str]**](str.md)| The old status (or conjunction) | [optional] 
 **new_status** | **str**|  | [optional] [default to READ]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | set notification status |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

