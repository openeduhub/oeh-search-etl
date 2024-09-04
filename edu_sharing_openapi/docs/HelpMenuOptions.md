# HelpMenuOptions


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**key** | **str** |  | [optional] 
**icon** | **str** |  | [optional] 
**url** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.help_menu_options import HelpMenuOptions

# TODO update the JSON string below
json = "{}"
# create an instance of HelpMenuOptions from a JSON string
help_menu_options_instance = HelpMenuOptions.from_json(json)
# print the JSON string representation of the object
print(HelpMenuOptions.to_json())

# convert the object into a dict
help_menu_options_dict = help_menu_options_instance.to_dict()
# create an instance of HelpMenuOptions from a dict
help_menu_options_from_dict = HelpMenuOptions.from_dict(help_menu_options_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


