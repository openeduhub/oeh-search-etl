# NodeDataDTO


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [optional] 
**aspects** | **List[str]** |  | [optional] 
**properties** | **Dict[str, object]** |  | [optional] 

## Example

```python
from edu_sharing_client.models.node_data_dto import NodeDataDTO

# TODO update the JSON string below
json = "{}"
# create an instance of NodeDataDTO from a JSON string
node_data_dto_instance = NodeDataDTO.from_json(json)
# print the JSON string representation of the object
print(NodeDataDTO.to_json())

# convert the object into a dict
node_data_dto_dict = node_data_dto_instance.to_dict()
# create an instance of NodeDataDTO from a dict
node_data_dto_from_dict = NodeDataDTO.from_dict(node_data_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


