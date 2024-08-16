# NodeRelation


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**node** | [**Node**](Node.md) |  | [optional] 
**relations** | [**List[RelationData]**](RelationData.md) |  | [optional] 

## Example

```python
from edu_sharing_client.models.node_relation import NodeRelation

# TODO update the JSON string below
json = "{}"
# create an instance of NodeRelation from a JSON string
node_relation_instance = NodeRelation.from_json(json)
# print the JSON string representation of the object
print(NodeRelation.to_json())

# convert the object into a dict
node_relation_dict = node_relation_instance.to_dict()
# create an instance of NodeRelation from a dict
node_relation_from_dict = NodeRelation.from_dict(node_relation_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


