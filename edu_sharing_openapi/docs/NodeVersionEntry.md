# NodeVersionEntry


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**version** | [**NodeVersion**](NodeVersion.md) |  | 

## Example

```python
from edu_sharing_client.models.node_version_entry import NodeVersionEntry

# TODO update the JSON string below
json = "{}"
# create an instance of NodeVersionEntry from a JSON string
node_version_entry_instance = NodeVersionEntry.from_json(json)
# print the JSON string representation of the object
print(NodeVersionEntry.to_json())

# convert the object into a dict
node_version_entry_dict = node_version_entry_instance.to_dict()
# create an instance of NodeVersionEntry from a dict
node_version_entry_from_dict = NodeVersionEntry.from_dict(node_version_entry_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


