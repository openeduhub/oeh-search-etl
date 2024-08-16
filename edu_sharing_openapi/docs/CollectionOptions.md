# CollectionOptions


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**private_collections** | **str** |  | [optional] 
**public_collections** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.collection_options import CollectionOptions

# TODO update the JSON string below
json = "{}"
# create an instance of CollectionOptions from a JSON string
collection_options_instance = CollectionOptions.from_json(json)
# print the JSON string representation of the object
print(CollectionOptions.to_json())

# convert the object into a dict
collection_options_dict = collection_options_instance.to_dict()
# create an instance of CollectionOptions from a dict
collection_options_from_dict = CollectionOptions.from_dict(collection_options_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


