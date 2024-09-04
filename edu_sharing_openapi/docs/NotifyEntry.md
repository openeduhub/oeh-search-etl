# NotifyEntry


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_date** | **int** |  | 
**permissions** | [**ACL**](ACL.md) |  | 
**user** | [**User**](User.md) |  | 
**action** | **str** |  | 

## Example

```python
from edu_sharing_client.models.notify_entry import NotifyEntry

# TODO update the JSON string below
json = "{}"
# create an instance of NotifyEntry from a JSON string
notify_entry_instance = NotifyEntry.from_json(json)
# print the JSON string representation of the object
print(NotifyEntry.to_json())

# convert the object into a dict
notify_entry_dict = notify_entry_instance.to_dict()
# create an instance of NotifyEntry from a dict
notify_entry_from_dict = NotifyEntry.from_dict(notify_entry_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


