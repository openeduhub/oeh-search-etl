# ConfigPublish


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**license_mandatory** | **bool** |  | [optional] 
**author_mandatory** | **bool** |  | [optional] 

## Example

```python
from edu_sharing_client.models.config_publish import ConfigPublish

# TODO update the JSON string below
json = "{}"
# create an instance of ConfigPublish from a JSON string
config_publish_instance = ConfigPublish.from_json(json)
# print the JSON string representation of the object
print(ConfigPublish.to_json())

# convert the object into a dict
config_publish_dict = config_publish_instance.to_dict()
# create an instance of ConfigPublish from a dict
config_publish_from_dict = ConfigPublish.from_dict(config_publish_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


