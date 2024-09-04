# InviteEventDTO


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**node** | [**NodeDataDTO**](NodeDataDTO.md) |  | [optional] 
**name** | **str** |  | [optional] 
**type** | **str** |  | [optional] 
**user_comment** | **str** |  | [optional] 
**permissions** | **List[str]** |  | [optional] 

## Example

```python
from edu_sharing_client.models.invite_event_dto import InviteEventDTO

# TODO update the JSON string below
json = "{}"
# create an instance of InviteEventDTO from a JSON string
invite_event_dto_instance = InviteEventDTO.from_json(json)
# print the JSON string representation of the object
print(InviteEventDTO.to_json())

# convert the object into a dict
invite_event_dto_dict = invite_event_dto_instance.to_dict()
# create an instance of InviteEventDTO from a dict
invite_event_dto_from_dict = InviteEventDTO.from_dict(invite_event_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


