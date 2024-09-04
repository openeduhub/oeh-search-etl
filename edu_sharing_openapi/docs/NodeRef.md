# NodeRef


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**repo** | **str** |  | 
**id** | **str** |  | 
**archived** | **bool** |  | 
**is_home_repo** | **bool** |  | [optional] 

## Example

```python
from edu_sharing_client.models.node_ref import NodeRef

# TODO update the JSON string below
json = "{}"
# create an instance of NodeRef from a JSON string
node_ref_instance = NodeRef.from_json(json)
# print the JSON string representation of the object
print(NodeRef.to_json())

# convert the object into a dict
node_ref_dict = node_ref_instance.to_dict()
# create an instance of NodeRef from a dict
node_ref_from_dict = NodeRef.from_dict(node_ref_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


