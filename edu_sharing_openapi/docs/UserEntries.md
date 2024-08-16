# UserEntries


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**users** | [**List[UserSimple]**](UserSimple.md) |  | 
**pagination** | [**Pagination**](Pagination.md) |  | 

## Example

```python
from edu_sharing_client.models.user_entries import UserEntries

# TODO update the JSON string below
json = "{}"
# create an instance of UserEntries from a JSON string
user_entries_instance = UserEntries.from_json(json)
# print the JSON string representation of the object
print(UserEntries.to_json())

# convert the object into a dict
user_entries_dict = user_entries_instance.to_dict()
# create an instance of UserEntries from a dict
user_entries_from_dict = UserEntries.from_dict(user_entries_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


