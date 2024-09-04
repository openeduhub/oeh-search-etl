# LTIPlatformConfiguration


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**product_family_code** | **str** |  | [optional] 
**version** | **str** |  | [optional] 
**messages_supported** | [**List[Message]**](Message.md) |  | [optional] 
**variables** | **List[str]** |  | [optional] 

## Example

```python
from edu_sharing_client.models.lti_platform_configuration import LTIPlatformConfiguration

# TODO update the JSON string below
json = "{}"
# create an instance of LTIPlatformConfiguration from a JSON string
lti_platform_configuration_instance = LTIPlatformConfiguration.from_json(json)
# print the JSON string representation of the object
print(LTIPlatformConfiguration.to_json())

# convert the object into a dict
lti_platform_configuration_dict = lti_platform_configuration_instance.to_dict()
# create an instance of LTIPlatformConfiguration from a dict
lti_platform_configuration_from_dict = LTIPlatformConfiguration.from_dict(lti_platform_configuration_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


