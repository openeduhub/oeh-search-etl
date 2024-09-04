# NodeVersionRef


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**node** | [**NodeRef**](NodeRef.md) |  | 
**major** | **int** |  | 
**minor** | **int** |  | 

## Example

```python
from edu_sharing_client.models.node_version_ref import NodeVersionRef

# TODO update the JSON string below
json = "{}"
# create an instance of NodeVersionRef from a JSON string
node_version_ref_instance = NodeVersionRef.from_json(json)
# print the JSON string representation of the object
print(NodeVersionRef.to_json())

# convert the object into a dict
node_version_ref_dict = node_version_ref_instance.to_dict()
# create an instance of NodeVersionRef from a dict
node_version_ref_from_dict = NodeVersionRef.from_dict(node_version_ref_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


