# NodeLTIDeepLink


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**lti_deep_link_return_url** | **str** |  | [optional] 
**jwt_deep_link_response** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.node_lti_deep_link import NodeLTIDeepLink

# TODO update the JSON string below
json = "{}"
# create an instance of NodeLTIDeepLink from a JSON string
node_lti_deep_link_instance = NodeLTIDeepLink.from_json(json)
# print the JSON string representation of the object
print(NodeLTIDeepLink.to_json())

# convert the object into a dict
node_lti_deep_link_dict = node_lti_deep_link_instance.to_dict()
# create an instance of NodeLTIDeepLink from a dict
node_lti_deep_link_from_dict = NodeLTIDeepLink.from_dict(node_lti_deep_link_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


