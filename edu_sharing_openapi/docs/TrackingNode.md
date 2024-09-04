# TrackingNode


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**counts** | **Dict[str, int]** |  | [optional] 
**var_date** | **str** |  | [optional] 
**fields** | **Dict[str, object]** |  | [optional] 
**groups** | **Dict[str, Dict[str, Dict[str, int]]]** |  | [optional] 
**node** | [**Node**](Node.md) |  | [optional] 
**authority** | [**TrackingAuthority**](TrackingAuthority.md) |  | [optional] 

## Example

```python
from edu_sharing_client.models.tracking_node import TrackingNode

# TODO update the JSON string below
json = "{}"
# create an instance of TrackingNode from a JSON string
tracking_node_instance = TrackingNode.from_json(json)
# print the JSON string representation of the object
print(TrackingNode.to_json())

# convert the object into a dict
tracking_node_dict = tracking_node_instance.to_dict()
# create an instance of TrackingNode from a dict
tracking_node_from_dict = TrackingNode.from_dict(tracking_node_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


