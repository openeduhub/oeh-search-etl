# NodeRemote


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**node** | [**Node**](Node.md) |  | 
**remote** | [**Node**](Node.md) |  | 

## Example

```python
from edu_sharing_client.models.node_remote import NodeRemote

# TODO update the JSON string below
json = "{}"
# create an instance of NodeRemote from a JSON string
node_remote_instance = NodeRemote.from_json(json)
# print the JSON string representation of the object
print(NodeRemote.to_json())

# convert the object into a dict
node_remote_dict = node_remote_instance.to_dict()
# create an instance of NodeRemote from a dict
node_remote_from_dict = NodeRemote.from_dict(node_remote_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


