# AddToCollectionEventDTO


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**node** | [**NodeDataDTO**](NodeDataDTO.md) |  | [optional] 
**collection** | [**CollectionDTO**](CollectionDTO.md) |  | [optional] 

## Example

```python
from edu_sharing_client.models.add_to_collection_event_dto import AddToCollectionEventDTO

# TODO update the JSON string below
json = "{}"
# create an instance of AddToCollectionEventDTO from a JSON string
add_to_collection_event_dto_instance = AddToCollectionEventDTO.from_json(json)
# print the JSON string representation of the object
print(AddToCollectionEventDTO.to_json())

# convert the object into a dict
add_to_collection_event_dto_dict = add_to_collection_event_dto_instance.to_dict()
# create an instance of AddToCollectionEventDTO from a dict
add_to_collection_event_dto_from_dict = AddToCollectionEventDTO.from_dict(add_to_collection_event_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


