# SimpleEdit


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**global_groups** | [**List[SimpleEditGlobalGroups]**](SimpleEditGlobalGroups.md) |  | [optional] 
**organization** | [**SimpleEditOrganization**](SimpleEditOrganization.md) |  | [optional] 
**organization_filter** | **str** |  | [optional] 
**licenses** | **List[str]** |  | [optional] 

## Example

```python
from edu_sharing_client.models.simple_edit import SimpleEdit

# TODO update the JSON string below
json = "{}"
# create an instance of SimpleEdit from a JSON string
simple_edit_instance = SimpleEdit.from_json(json)
# print the JSON string representation of the object
print(SimpleEdit.to_json())

# convert the object into a dict
simple_edit_dict = simple_edit_instance.to_dict()
# create an instance of SimpleEdit from a dict
simple_edit_from_dict = SimpleEdit.from_dict(simple_edit_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


