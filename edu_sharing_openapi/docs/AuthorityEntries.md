# AuthorityEntries


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**authorities** | [**List[Authority]**](Authority.md) |  | 
**pagination** | [**Pagination**](Pagination.md) |  | 

## Example

```python
from edu_sharing_client.models.authority_entries import AuthorityEntries

# TODO update the JSON string below
json = "{}"
# create an instance of AuthorityEntries from a JSON string
authority_entries_instance = AuthorityEntries.from_json(json)
# print the JSON string representation of the object
print(AuthorityEntries.to_json())

# convert the object into a dict
authority_entries_dict = authority_entries_instance.to_dict()
# create an instance of AuthorityEntries from a dict
authority_entries_from_dict = AuthorityEntries.from_dict(authority_entries_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


