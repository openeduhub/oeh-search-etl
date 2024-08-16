# NotificationEventDTO


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**timestamp** | **datetime** |  | [optional] 
**creator** | [**UserDataDTO**](UserDataDTO.md) |  | [optional] 
**receiver** | [**UserDataDTO**](UserDataDTO.md) |  | [optional] 
**status** | **str** |  | [optional] 
**id** | **str** |  | [optional] 
**var_class** | **str** |  | 

## Example

```python
from edu_sharing_client.models.notification_event_dto import NotificationEventDTO

# TODO update the JSON string below
json = "{}"
# create an instance of NotificationEventDTO from a JSON string
notification_event_dto_instance = NotificationEventDTO.from_json(json)
# print the JSON string representation of the object
print(NotificationEventDTO.to_json())

# convert the object into a dict
notification_event_dto_dict = notification_event_dto_instance.to_dict()
# create an instance of NotificationEventDTO from a dict
notification_event_dto_from_dict = NotificationEventDTO.from_dict(notification_event_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


