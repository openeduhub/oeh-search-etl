# NodeIssueEventDTO


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**node** | [**NodeDataDTO**](NodeDataDTO.md) |  | [optional] 
**reason** | **str** |  | [optional] 
**user_comment** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.node_issue_event_dto import NodeIssueEventDTO

# TODO update the JSON string below
json = "{}"
# create an instance of NodeIssueEventDTO from a JSON string
node_issue_event_dto_instance = NodeIssueEventDTO.from_json(json)
# print the JSON string representation of the object
print(NodeIssueEventDTO.to_json())

# convert the object into a dict
node_issue_event_dto_dict = node_issue_event_dto_instance.to_dict()
# create an instance of NodeIssueEventDTO from a dict
node_issue_event_dto_from_dict = NodeIssueEventDTO.from_dict(node_issue_event_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


