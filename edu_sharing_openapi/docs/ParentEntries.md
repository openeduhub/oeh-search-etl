# ParentEntries


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**scope** | **str** |  | [optional] 
**nodes** | [**List[Node]**](Node.md) |  | 
**pagination** | [**Pagination**](Pagination.md) |  | 

## Example

```python
from edu_sharing_client.models.parent_entries import ParentEntries

# TODO update the JSON string below
json = "{}"
# create an instance of ParentEntries from a JSON string
parent_entries_instance = ParentEntries.from_json(json)
# print the JSON string representation of the object
print(ParentEntries.to_json())

# convert the object into a dict
parent_entries_dict = parent_entries_instance.to_dict()
# create an instance of ParentEntries from a dict
parent_entries_from_dict = ParentEntries.from_dict(parent_entries_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


