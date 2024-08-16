# NodeShare


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**password** | **bool** |  | [optional] 
**token** | **str** |  | [optional] 
**email** | **str** |  | [optional] 
**expiry_date** | **int** |  | [optional] 
**invited_at** | **int** |  | [optional] 
**download_count** | **int** |  | [optional] 
**url** | **str** |  | [optional] 
**share_id** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.node_share import NodeShare

# TODO update the JSON string below
json = "{}"
# create an instance of NodeShare from a JSON string
node_share_instance = NodeShare.from_json(json)
# print the JSON string representation of the object
print(NodeShare.to_json())

# convert the object into a dict
node_share_dict = node_share_instance.to_dict()
# create an instance of NodeShare from a dict
node_share_from_dict = NodeShare.from_dict(node_share_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


