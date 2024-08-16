# NodePermissions


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**local_permissions** | [**ACL**](ACL.md) |  | 
**inherited_permissions** | [**List[ACE]**](ACE.md) |  | 

## Example

```python
from edu_sharing_client.models.node_permissions import NodePermissions

# TODO update the JSON string below
json = "{}"
# create an instance of NodePermissions from a JSON string
node_permissions_instance = NodePermissions.from_json(json)
# print the JSON string representation of the object
print(NodePermissions.to_json())

# convert the object into a dict
node_permissions_dict = node_permissions_instance.to_dict()
# create an instance of NodePermissions from a dict
node_permissions_from_dict = NodePermissions.from_dict(node_permissions_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


