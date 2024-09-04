# NodeData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**timestamp** | **str** |  | [optional] 
**counts** | **Dict[str, int]** |  | [optional] 

## Example

```python
from edu_sharing_client.models.node_data import NodeData

# TODO update the JSON string below
json = "{}"
# create an instance of NodeData from a JSON string
node_data_instance = NodeData.from_json(json)
# print the JSON string representation of the object
print(NodeData.to_json())

# convert the object into a dict
node_data_dict = node_data_instance.to_dict()
# create an instance of NodeData from a dict
node_data_from_dict = NodeData.from_dict(node_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


