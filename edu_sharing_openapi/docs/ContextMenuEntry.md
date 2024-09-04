# ContextMenuEntry


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
**mode** | **str** |  | [optional] 
**scopes** | **List[str]** |  | [optional] 
**ajax** | **bool** |  | [optional] 
**group** | **str** |  | [optional] 
**permission** | **str** |  | [optional] 
**toolpermission** | **str** |  | [optional] 
**is_directory** | **bool** |  | [optional] 
**show_as_action** | **bool** |  | [optional] 
**multiple** | **bool** |  | [optional] 
**change_strategy** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.context_menu_entry import ContextMenuEntry

# TODO update the JSON string below
json = "{}"
# create an instance of ContextMenuEntry from a JSON string
context_menu_entry_instance = ContextMenuEntry.from_json(json)
# print the JSON string representation of the object
print(ContextMenuEntry.to_json())

# convert the object into a dict
context_menu_entry_dict = context_menu_entry_instance.to_dict()
# create an instance of ContextMenuEntry from a dict
context_menu_entry_from_dict = ContextMenuEntry.from_dict(context_menu_entry_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


