# User


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**properties** | **Dict[str, List[str]]** |  | [optional] 
**editable** | **bool** |  | [optional] 
**status** | [**UserStatus**](UserStatus.md) |  | [optional] 
**organizations** | [**List[Organization]**](Organization.md) |  | [optional] 
**quota** | [**UserQuota**](UserQuota.md) |  | [optional] 
**authority_name** | **str** |  | 
**authority_type** | **str** |  | [optional] 
**user_name** | **str** |  | [optional] 
**profile** | [**UserProfile**](UserProfile.md) |  | [optional] 
**home_folder** | [**NodeRef**](NodeRef.md) |  | 
**shared_folders** | [**List[NodeRef]**](NodeRef.md) |  | [optional] 

## Example

```python
from edu_sharing_client.models.user import User

# TODO update the JSON string below
json = "{}"
# create an instance of User from a JSON string
user_instance = User.from_json(json)
# print the JSON string representation of the object
print(User.to_json())

# convert the object into a dict
user_dict = user_instance.to_dict()
# create an instance of User from a dict
user_from_dict = User.from_dict(user_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


