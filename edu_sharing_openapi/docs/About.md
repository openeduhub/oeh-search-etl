# About


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**plugins** | [**List[PluginInfo]**](PluginInfo.md) |  | [optional] 
**features** | [**List[FeatureInfo]**](FeatureInfo.md) |  | [optional] 
**themes_url** | **str** |  | [optional] 
**last_cache_update** | **int** |  | [optional] 
**version** | [**ServiceVersion**](ServiceVersion.md) |  | 
**services** | [**List[AboutService]**](AboutService.md) |  | 

## Example

```python
from edu_sharing_client.models.about import About

# TODO update the JSON string below
json = "{}"
# create an instance of About from a JSON string
about_instance = About.from_json(json)
# print the JSON string representation of the object
print(About.to_json())

# convert the object into a dict
about_dict = about_instance.to_dict()
# create an instance of About from a dict
about_from_dict = About.from_dict(about_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


