# OrganizationEntries


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**organizations** | [**List[Organization]**](Organization.md) |  | 
**pagination** | [**Pagination**](Pagination.md) |  | 
**can_create** | **bool** |  | [optional] 

## Example

```python
from edu_sharing_client.models.organization_entries import OrganizationEntries

# TODO update the JSON string below
json = "{}"
# create an instance of OrganizationEntries from a JSON string
organization_entries_instance = OrganizationEntries.from_json(json)
# print the JSON string representation of the object
print(OrganizationEntries.to_json())

# convert the object into a dict
organization_entries_dict = organization_entries_instance.to_dict()
# create an instance of OrganizationEntries from a dict
organization_entries_from_dict = OrganizationEntries.from_dict(organization_entries_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


