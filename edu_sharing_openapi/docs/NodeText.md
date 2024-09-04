# NodeText


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**text** | **str** |  | [optional] 
**html** | **str** |  | [optional] 
**raw** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.node_text import NodeText

# TODO update the JSON string below
json = "{}"
# create an instance of NodeText from a JSON string
node_text_instance = NodeText.from_json(json)
# print the JSON string representation of the object
print(NodeText.to_json())

# convert the object into a dict
node_text_dict = node_text_instance.to_dict()
# create an instance of NodeText from a dict
node_text_from_dict = NodeText.from_dict(node_text_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


