# CollectionEntries


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**Pagination**](Pagination.md) |  | [optional] 
**collections** | [**List[Node]**](Node.md) |  | 

## Example

```python
from edu_sharing_client.models.collection_entries import CollectionEntries

# TODO update the JSON string below
json = "{}"
# create an instance of CollectionEntries from a JSON string
collection_entries_instance = CollectionEntries.from_json(json)
# print the JSON string representation of the object
print(CollectionEntries.to_json())

# convert the object into a dict
collection_entries_dict = collection_entries_instance.to_dict()
# create an instance of CollectionEntries from a dict
collection_entries_from_dict = CollectionEntries.from_dict(collection_entries_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


