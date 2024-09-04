# MenuEntry


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**position** | **int** |  | [optional] 
**icon** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**url** | **str** |  | [optional] 
**is_disabled** | **bool** |  | [optional] 
**open_in_new** | **bool** |  | [optional] 
**is_separate** | **bool** |  | [optional] 
**is_separate_bottom** | **bool** |  | [optional] 
**only_desktop** | **bool** |  | [optional] 
**only_web** | **bool** |  | [optional] 
**path** | **str** |  | [optional] 
**scope** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.menu_entry import MenuEntry

# TODO update the JSON string below
json = "{}"
# create an instance of MenuEntry from a JSON string
menu_entry_instance = MenuEntry.from_json(json)
# print the JSON string representation of the object
print(MenuEntry.to_json())

# convert the object into a dict
menu_entry_dict = menu_entry_instance.to_dict()
# create an instance of MenuEntry from a dict
menu_entry_from_dict = MenuEntry.from_dict(menu_entry_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


