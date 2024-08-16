# UserEntry


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**edit_profile** | **bool** |  | [optional] 
**person** | [**User**](User.md) |  | 

## Example

```python
from edu_sharing_client.models.user_entry import UserEntry

# TODO update the JSON string below
json = "{}"
# create an instance of UserEntry from a JSON string
user_entry_instance = UserEntry.from_json(json)
# print the JSON string representation of the object
print(UserEntry.to_json())

# convert the object into a dict
user_entry_dict = user_entry_instance.to_dict()
# create an instance of UserEntry from a dict
user_entry_from_dict = UserEntry.from_dict(user_entry_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


