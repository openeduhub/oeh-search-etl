# NotificationIntervals


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**add_to_collection_event** | **str** |  | [optional] 
**propose_for_collection_event** | **str** |  | [optional] 
**comment_event** | **str** |  | [optional] 
**invite_event** | **str** |  | [optional] 
**node_issue_event** | **str** |  | [optional] 
**rating_event** | **str** |  | [optional] 
**workflow_event** | **str** |  | [optional] 
**metadata_suggestion_event** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.notification_intervals import NotificationIntervals

# TODO update the JSON string below
json = "{}"
# create an instance of NotificationIntervals from a JSON string
notification_intervals_instance = NotificationIntervals.from_json(json)
# print the JSON string representation of the object
print(NotificationIntervals.to_json())

# convert the object into a dict
notification_intervals_dict = notification_intervals_instance.to_dict()
# create an instance of NotificationIntervals from a dict
notification_intervals_from_dict = NotificationIntervals.from_dict(notification_intervals_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


