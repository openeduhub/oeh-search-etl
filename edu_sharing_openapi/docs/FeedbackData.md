# FeedbackData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**authority** | **str** |  | [optional] 
**data** | **Dict[str, List[str]]** |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**modified_at** | **datetime** |  | [optional] 

## Example

```python
from edu_sharing_client.models.feedback_data import FeedbackData

# TODO update the JSON string below
json = "{}"
# create an instance of FeedbackData from a JSON string
feedback_data_instance = FeedbackData.from_json(json)
# print the JSON string representation of the object
print(FeedbackData.to_json())

# convert the object into a dict
feedback_data_dict = feedback_data_instance.to_dict()
# create an instance of FeedbackData from a dict
feedback_data_from_dict = FeedbackData.from_dict(feedback_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


