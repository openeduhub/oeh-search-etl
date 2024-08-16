# Group


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**properties** | **Dict[str, List[str]]** |  | [optional] 
**editable** | **bool** |  | [optional] 
**signup_method** | **str** |  | [optional] 
**ref** | [**NodeRef**](NodeRef.md) |  | [optional] 
**aspects** | **List[str]** |  | [optional] 
**organizations** | [**List[Organization]**](Organization.md) |  | [optional] 
**authority_name** | **str** |  | 
**authority_type** | **str** |  | [optional] 
**group_name** | **str** |  | [optional] 
**profile** | [**GroupProfile**](GroupProfile.md) |  | [optional] 

## Example

```python
from edu_sharing_client.models.group import Group

# TODO update the JSON string below
json = "{}"
# create an instance of Group from a JSON string
group_instance = Group.from_json(json)
# print the JSON string representation of the object
print(Group.to_json())

# convert the object into a dict
group_dict = group_instance.to_dict()
# create an instance of Group from a dict
group_from_dict = Group.from_dict(group_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


