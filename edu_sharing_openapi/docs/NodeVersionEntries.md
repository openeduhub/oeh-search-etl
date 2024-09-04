# NodeVersionEntries


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**versions** | [**List[NodeVersion]**](NodeVersion.md) |  | 

## Example

```python
from edu_sharing_client.models.node_version_entries import NodeVersionEntries

# TODO update the JSON string below
json = "{}"
# create an instance of NodeVersionEntries from a JSON string
node_version_entries_instance = NodeVersionEntries.from_json(json)
# print the JSON string representation of the object
print(NodeVersionEntries.to_json())

# convert the object into a dict
node_version_entries_dict = node_version_entries_instance.to_dict()
# create an instance of NodeVersionEntries from a dict
node_version_entries_from_dict = NodeVersionEntries.from_dict(node_version_entries_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


