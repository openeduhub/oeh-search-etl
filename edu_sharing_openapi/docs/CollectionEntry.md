# CollectionEntry


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**collection** | [**Node**](Node.md) |  | 

## Example

```python
from edu_sharing_client.models.collection_entry import CollectionEntry

# TODO update the JSON string below
json = "{}"
# create an instance of CollectionEntry from a JSON string
collection_entry_instance = CollectionEntry.from_json(json)
# print the JSON string representation of the object
print(CollectionEntry.to_json())

# convert the object into a dict
collection_entry_dict = collection_entry_instance.to_dict()
# create an instance of CollectionEntry from a dict
collection_entry_from_dict = CollectionEntry.from_dict(collection_entry_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


