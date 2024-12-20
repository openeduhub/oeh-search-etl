# NodeStats


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **Dict[str, int]** |  | [optional] 

## Example

```python
from edu_sharing_client.models.node_stats import NodeStats

# TODO update the JSON string below
json = "{}"
# create an instance of NodeStats from a JSON string
node_stats_instance = NodeStats.from_json(json)
# print the JSON string representation of the object
print(NodeStats.to_json())

# convert the object into a dict
node_stats_dict = node_stats_instance.to_dict()
# create an instance of NodeStats from a dict
node_stats_from_dict = NodeStats.from_dict(node_stats_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

