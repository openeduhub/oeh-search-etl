# NodeEntries


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**nodes** | [**List[Node]**](Node.md) |  | 
**pagination** | [**Pagination**](Pagination.md) |  | 

## Example

```python
from edu_sharing_client.models.node_entries import NodeEntries

# TODO update the JSON string below
json = "{}"
# create an instance of NodeEntries from a JSON string
node_entries_instance = NodeEntries.from_json(json)
# print the JSON string representation of the object
print(NodeEntries.to_json())

# convert the object into a dict
node_entries_dict = node_entries_instance.to_dict()
# create an instance of NodeEntries from a dict
node_entries_from_dict = NodeEntries.from_dict(node_entries_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


