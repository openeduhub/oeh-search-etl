# ReferenceEntries


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**Pagination**](Pagination.md) |  | [optional] 
**references** | [**List[CollectionReference]**](CollectionReference.md) |  | 

## Example

```python
from edu_sharing_client.models.reference_entries import ReferenceEntries

# TODO update the JSON string below
json = "{}"
# create an instance of ReferenceEntries from a JSON string
reference_entries_instance = ReferenceEntries.from_json(json)
# print the JSON string representation of the object
print(ReferenceEntries.to_json())

# convert the object into a dict
reference_entries_dict = reference_entries_instance.to_dict()
# create an instance of ReferenceEntries from a dict
reference_entries_from_dict = ReferenceEntries.from_dict(reference_entries_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


