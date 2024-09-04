# ProposeForCollectionEventDTO


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**node** | [**NodeDataDTO**](NodeDataDTO.md) |  | [optional] 
**collection** | [**CollectionDTO**](CollectionDTO.md) |  | [optional] 

## Example

```python
from edu_sharing_client.models.propose_for_collection_event_dto import ProposeForCollectionEventDTO

# TODO update the JSON string below
json = "{}"
# create an instance of ProposeForCollectionEventDTO from a JSON string
propose_for_collection_event_dto_instance = ProposeForCollectionEventDTO.from_json(json)
# print the JSON string representation of the object
print(ProposeForCollectionEventDTO.to_json())

# convert the object into a dict
propose_for_collection_event_dto_dict = propose_for_collection_event_dto_instance.to_dict()
# create an instance of ProposeForCollectionEventDTO from a dict
propose_for_collection_event_dto_from_dict = ProposeForCollectionEventDTO.from_dict(propose_for_collection_event_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


