# DynamicConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**node_id** | **str** |  | [optional] 
**value** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.dynamic_config import DynamicConfig

# TODO update the JSON string below
json = "{}"
# create an instance of DynamicConfig from a JSON string
dynamic_config_instance = DynamicConfig.from_json(json)
# print the JSON string representation of the object
print(DynamicConfig.to_json())

# convert the object into a dict
dynamic_config_dict = dynamic_config_instance.to_dict()
# create an instance of DynamicConfig from a dict
dynamic_config_from_dict = DynamicConfig.from_dict(dynamic_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


