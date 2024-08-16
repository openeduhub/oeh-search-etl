# LTIToolConfiguration


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**version** | **str** |  | [optional] 
**deployment_id** | **str** |  | [optional] 
**target_link_uri** | **str** |  | [optional] 
**domain** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**claims** | **List[str]** |  | [optional] 

## Example

```python
from edu_sharing_client.models.lti_tool_configuration import LTIToolConfiguration

# TODO update the JSON string below
json = "{}"
# create an instance of LTIToolConfiguration from a JSON string
lti_tool_configuration_instance = LTIToolConfiguration.from_json(json)
# print the JSON string representation of the object
print(LTIToolConfiguration.to_json())

# convert the object into a dict
lti_tool_configuration_dict = lti_tool_configuration_instance.to_dict()
# create an instance of LTIToolConfiguration from a dict
lti_tool_configuration_from_dict = LTIToolConfiguration.from_dict(lti_tool_configuration_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


