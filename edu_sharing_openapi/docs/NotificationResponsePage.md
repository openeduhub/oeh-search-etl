# NotificationResponsePage


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | [**List[NotificationEventDTO]**](NotificationEventDTO.md) |  | [optional] 
**pageable** | [**Pageable**](Pageable.md) |  | [optional] 
**total_elements** | **int** |  | [optional] 
**total_pages** | **int** |  | [optional] 
**last** | **bool** |  | [optional] 
**number_of_elements** | **int** |  | [optional] 
**first** | **bool** |  | [optional] 
**size** | **int** |  | [optional] 
**number** | **int** |  | [optional] 
**sort** | [**Sort**](Sort.md) |  | [optional] 
**empty** | **bool** |  | [optional] 

## Example

```python
from edu_sharing_client.models.notification_response_page import NotificationResponsePage

# TODO update the JSON string below
json = "{}"
# create an instance of NotificationResponsePage from a JSON string
notification_response_page_instance = NotificationResponsePage.from_json(json)
# print the JSON string representation of the object
print(NotificationResponsePage.to_json())

# convert the object into a dict
notification_response_page_dict = notification_response_page_instance.to_dict()
# create an instance of NotificationResponsePage from a dict
notification_response_page_from_dict = NotificationResponsePage.from_dict(notification_response_page_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


