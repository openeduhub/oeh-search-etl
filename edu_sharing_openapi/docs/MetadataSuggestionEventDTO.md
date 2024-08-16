# MetadataSuggestionEventDTO


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**node** | [**NodeDataDTO**](NodeDataDTO.md) |  | [optional] 
**caption_id** | **str** |  | [optional] 
**caption** | **str** |  | [optional] 
**parent_id** | **str** |  | [optional] 
**parent_caption** | **str** |  | [optional] 
**widget** | [**WidgetDataDTO**](WidgetDataDTO.md) |  | [optional] 

## Example

```python
from edu_sharing_client.models.metadata_suggestion_event_dto import MetadataSuggestionEventDTO

# TODO update the JSON string below
json = "{}"
# create an instance of MetadataSuggestionEventDTO from a JSON string
metadata_suggestion_event_dto_instance = MetadataSuggestionEventDTO.from_json(json)
# print the JSON string representation of the object
print(MetadataSuggestionEventDTO.to_json())

# convert the object into a dict
metadata_suggestion_event_dto_dict = metadata_suggestion_event_dto_instance.to_dict()
# create an instance of MetadataSuggestionEventDTO from a dict
metadata_suggestion_event_dto_from_dict = MetadataSuggestionEventDTO.from_dict(metadata_suggestion_event_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


