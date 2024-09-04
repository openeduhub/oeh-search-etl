# CollectionCounts


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**refs** | [**List[Element]**](Element.md) |  | [optional] 
**collections** | [**List[Element]**](Element.md) |  | [optional] 

## Example

```python
from edu_sharing_client.models.collection_counts import CollectionCounts

# TODO update the JSON string below
json = "{}"
# create an instance of CollectionCounts from a JSON string
collection_counts_instance = CollectionCounts.from_json(json)
# print the JSON string representation of the object
print(CollectionCounts.to_json())

# convert the object into a dict
collection_counts_dict = collection_counts_instance.to_dict()
# create an instance of CollectionCounts from a dict
collection_counts_from_dict = CollectionCounts.from_dict(collection_counts_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


