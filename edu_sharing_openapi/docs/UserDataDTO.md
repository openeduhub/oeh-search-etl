# UserDataDTO


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**first_name** | **str** |  | [optional] 
**last_name** | **str** |  | [optional] 
**mailbox** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.user_data_dto import UserDataDTO

# TODO update the JSON string below
json = "{}"
# create an instance of UserDataDTO from a JSON string
user_data_dto_instance = UserDataDTO.from_json(json)
# print the JSON string representation of the object
print(UserDataDTO.to_json())

# convert the object into a dict
user_data_dto_dict = user_data_dto_instance.to_dict()
# create an instance of UserDataDTO from a dict
user_data_dto_from_dict = UserDataDTO.from_dict(user_data_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


