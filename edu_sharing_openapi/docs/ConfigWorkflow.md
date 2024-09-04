# ConfigWorkflow


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**default_receiver** | **str** |  | [optional] 
**default_status** | **str** |  | [optional] 
**comment_required** | **bool** |  | [optional] 
**workflows** | [**List[ConfigWorkflowList]**](ConfigWorkflowList.md) |  | [optional] 

## Example

```python
from edu_sharing_client.models.config_workflow import ConfigWorkflow

# TODO update the JSON string below
json = "{}"
# create an instance of ConfigWorkflow from a JSON string
config_workflow_instance = ConfigWorkflow.from_json(json)
# print the JSON string representation of the object
print(ConfigWorkflow.to_json())

# convert the object into a dict
config_workflow_dict = config_workflow_instance.to_dict()
# create an instance of ConfigWorkflow from a dict
config_workflow_from_dict = ConfigWorkflow.from_dict(config_workflow_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


