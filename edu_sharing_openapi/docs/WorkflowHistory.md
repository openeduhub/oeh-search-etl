# WorkflowHistory


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**time** | **int** |  | [optional] 
**editor** | [**UserSimple**](UserSimple.md) |  | [optional] 
**receiver** | [**List[Authority]**](Authority.md) |  | [optional] 
**status** | **str** |  | [optional] 
**comment** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.workflow_history import WorkflowHistory

# TODO update the JSON string below
json = "{}"
# create an instance of WorkflowHistory from a JSON string
workflow_history_instance = WorkflowHistory.from_json(json)
# print the JSON string representation of the object
print(WorkflowHistory.to_json())

# convert the object into a dict
workflow_history_dict = workflow_history_instance.to_dict()
# create an instance of WorkflowHistory from a dict
workflow_history_from_dict = WorkflowHistory.from_dict(workflow_history_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


