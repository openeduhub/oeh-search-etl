# UserProfileAppAuth


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**primary_affiliation** | **str** |  | [optional] 
**skills** | **List[str]** |  | [optional] 
**types** | **List[str]** |  | [optional] 
**extended_attributes** | **Dict[str, List[str]]** |  | [optional] 
**vcard** | **str** |  | [optional] 
**type** | **List[str]** |  | [optional] 
**first_name** | **str** |  | [optional] 
**last_name** | **str** |  | [optional] 
**email** | **str** |  | [optional] 
**avatar** | **str** |  | [optional] 
**about** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.user_profile_app_auth import UserProfileAppAuth

# TODO update the JSON string below
json = "{}"
# create an instance of UserProfileAppAuth from a JSON string
user_profile_app_auth_instance = UserProfileAppAuth.from_json(json)
# print the JSON string representation of the object
print(UserProfileAppAuth.to_json())

# convert the object into a dict
user_profile_app_auth_dict = user_profile_app_auth_instance.to_dict()
# create an instance of UserProfileAppAuth from a dict
user_profile_app_auth_from_dict = UserProfileAppAuth.from_dict(user_profile_app_auth_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


