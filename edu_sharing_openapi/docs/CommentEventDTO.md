# CommentEventDTO


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**node** | [**NodeDataDTO**](NodeDataDTO.md) |  | [optional] 
**comment_content** | **str** |  | [optional] 
**comment_reference** | **str** |  | [optional] 
**event** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.comment_event_dto import CommentEventDTO

# TODO update the JSON string below
json = "{}"
# create an instance of CommentEventDTO from a JSON string
comment_event_dto_instance = CommentEventDTO.from_json(json)
# print the JSON string representation of the object
print(CommentEventDTO.to_json())

# convert the object into a dict
comment_event_dto_dict = comment_event_dto_instance.to_dict()
# create an instance of CommentEventDTO from a dict
comment_event_dto_from_dict = CommentEventDTO.from_dict(comment_event_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


