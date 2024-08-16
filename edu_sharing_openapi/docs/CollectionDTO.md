# CollectionDTO


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [optional] 
**aspects** | **List[str]** |  | [optional] 
**properties** | **Dict[str, object]** |  | [optional] 

## Example

```python
from edu_sharing_client.models.collection_dto import CollectionDTO

# TODO update the JSON string below
json = "{}"
# create an instance of CollectionDTO from a JSON string
collection_dto_instance = CollectionDTO.from_json(json)
# print the JSON string representation of the object
print(CollectionDTO.to_json())

# convert the object into a dict
collection_dto_dict = collection_dto_instance.to_dict()
# create an instance of CollectionDTO from a dict
collection_dto_from_dict = CollectionDTO.from_dict(collection_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


