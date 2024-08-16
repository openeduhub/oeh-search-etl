# ConfigWorkflowList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**color** | **str** |  | [optional] 
**has_receiver** | **bool** |  | [optional] 
**next** | **List[str]** |  | [optional] 

## Example

```python
from edu_sharing_client.models.config_workflow_list import ConfigWorkflowList

# TODO update the JSON string below
json = "{}"
# create an instance of ConfigWorkflowList from a JSON string
config_workflow_list_instance = ConfigWorkflowList.from_json(json)
# print the JSON string representation of the object
print(ConfigWorkflowList.to_json())

# convert the object into a dict
config_workflow_list_dict = config_workflow_list_instance.to_dict()
# create an instance of ConfigWorkflowList from a dict
config_workflow_list_from_dict = ConfigWorkflowList.from_dict(config_workflow_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


