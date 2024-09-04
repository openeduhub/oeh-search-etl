# NodeVersion


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**properties** | **Dict[str, List[str]]** |  | [optional] 
**version** | [**NodeVersionRef**](NodeVersionRef.md) |  | 
**comment** | **str** |  | 
**modified_at** | **str** |  | 
**modified_by** | [**Person**](Person.md) |  | 
**content_url** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.node_version import NodeVersion

# TODO update the JSON string below
json = "{}"
# create an instance of NodeVersion from a JSON string
node_version_instance = NodeVersion.from_json(json)
# print the JSON string representation of the object
print(NodeVersion.to_json())

# convert the object into a dict
node_version_dict = node_version_instance.to_dict()
# create an instance of NodeVersion from a dict
node_version_from_dict = NodeVersion.from_dict(node_version_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


