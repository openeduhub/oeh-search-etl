# GroupEntries


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**groups** | [**List[Group]**](Group.md) |  | 
**pagination** | [**Pagination**](Pagination.md) |  | 

## Example

```python
from edu_sharing_client.models.group_entries import GroupEntries

# TODO update the JSON string below
json = "{}"
# create an instance of GroupEntries from a JSON string
group_entries_instance = GroupEntries.from_json(json)
# print the JSON string representation of the object
print(GroupEntries.to_json())

# convert the object into a dict
group_entries_dict = group_entries_instance.to_dict()
# create an instance of GroupEntries from a dict
group_entries_from_dict = GroupEntries.from_dict(group_entries_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


