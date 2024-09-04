# WorkflowEventDTO


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**node** | [**NodeDataDTO**](NodeDataDTO.md) |  | [optional] 
**workflow_status** | **str** |  | [optional] 
**user_comment** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.workflow_event_dto import WorkflowEventDTO

# TODO update the JSON string below
json = "{}"
# create an instance of WorkflowEventDTO from a JSON string
workflow_event_dto_instance = WorkflowEventDTO.from_json(json)
# print the JSON string representation of the object
print(WorkflowEventDTO.to_json())

# convert the object into a dict
workflow_event_dto_dict = workflow_event_dto_instance.to_dict()
# create an instance of WorkflowEventDTO from a dict
workflow_event_dto_from_dict = WorkflowEventDTO.from_dict(workflow_event_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


