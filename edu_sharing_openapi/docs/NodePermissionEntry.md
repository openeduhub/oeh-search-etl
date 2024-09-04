# NodePermissionEntry


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**permissions** | [**NodePermissions**](NodePermissions.md) |  | 

## Example

```python
from edu_sharing_client.models.node_permission_entry import NodePermissionEntry

# TODO update the JSON string below
json = "{}"
# create an instance of NodePermissionEntry from a JSON string
node_permission_entry_instance = NodePermissionEntry.from_json(json)
# print the JSON string representation of the object
print(NodePermissionEntry.to_json())

# convert the object into a dict
node_permission_entry_dict = node_permission_entry_instance.to_dict()
# create an instance of NodePermissionEntry from a dict
node_permission_entry_from_dict = NodePermissionEntry.from_dict(node_permission_entry_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


