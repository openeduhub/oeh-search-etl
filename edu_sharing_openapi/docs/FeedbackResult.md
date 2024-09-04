# FeedbackResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**node_id** | **str** |  | [optional] 
**was_updated** | **bool** |  | [optional] 

## Example

```python
from edu_sharing_client.models.feedback_result import FeedbackResult

# TODO update the JSON string below
json = "{}"
# create an instance of FeedbackResult from a JSON string
feedback_result_instance = FeedbackResult.from_json(json)
# print the JSON string representation of the object
print(FeedbackResult.to_json())

# convert the object into a dict
feedback_result_dict = feedback_result_instance.to_dict()
# create an instance of FeedbackResult from a dict
feedback_result_from_dict = FeedbackResult.from_dict(feedback_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


