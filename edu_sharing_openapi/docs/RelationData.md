# RelationData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**node** | [**Node**](Node.md) |  | [optional] 
**creator** | [**User**](User.md) |  | [optional] 
**timestamp** | **datetime** |  | [optional] 
**type** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.relation_data import RelationData

# TODO update the JSON string below
json = "{}"
# create an instance of RelationData from a JSON string
relation_data_instance = RelationData.from_json(json)
# print the JSON string representation of the object
print(RelationData.to_json())

# convert the object into a dict
relation_data_dict = relation_data_instance.to_dict()
# create an instance of RelationData from a dict
relation_data_from_dict = RelationData.from_dict(relation_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


