# NotificationConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**config_mode** | **str** |  | [optional] 
**default_interval** | **str** |  | [optional] 
**intervals** | [**NotificationIntervals**](NotificationIntervals.md) |  | [optional] 

## Example

```python
from edu_sharing_client.models.notification_config import NotificationConfig

# TODO update the JSON string below
json = "{}"
# create an instance of NotificationConfig from a JSON string
notification_config_instance = NotificationConfig.from_json(json)
# print the JSON string representation of the object
print(NotificationConfig.to_json())

# convert the object into a dict
notification_config_dict = notification_config_instance.to_dict()
# create an instance of NotificationConfig from a dict
notification_config_from_dict = NotificationConfig.from_dict(notification_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


