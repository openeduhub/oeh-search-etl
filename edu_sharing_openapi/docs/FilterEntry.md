# FilterEntry


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_property** | **str** |  | 
**values** | **List[str]** |  | 

## Example

```python
from edu_sharing_client.models.filter_entry import FilterEntry

# TODO update the JSON string below
json = "{}"
# create an instance of FilterEntry from a JSON string
filter_entry_instance = FilterEntry.from_json(json)
# print the JSON string representation of the object
print(FilterEntry.to_json())

# convert the object into a dict
filter_entry_dict = filter_entry_instance.to_dict()
# create an instance of FilterEntry from a dict
filter_entry_from_dict = FilterEntry.from_dict(filter_entry_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


