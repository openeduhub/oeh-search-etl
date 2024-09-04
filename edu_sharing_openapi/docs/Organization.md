# Organization


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**properties** | **Dict[str, List[str]]** |  | [optional] 
**editable** | **bool** |  | [optional] 
**signup_method** | **str** |  | [optional] 
**ref** | [**NodeRef**](NodeRef.md) |  | [optional] 
**aspects** | **List[str]** |  | [optional] 
**authority_name** | **str** |  | 
**authority_type** | **str** |  | [optional] 
**group_name** | **str** |  | [optional] 
**profile** | [**GroupProfile**](GroupProfile.md) |  | [optional] 
**administration_access** | **bool** |  | [optional] 
**shared_folder** | [**NodeRef**](NodeRef.md) |  | [optional] 

## Example

```python
from edu_sharing_client.models.organization import Organization

# TODO update the JSON string below
json = "{}"
# create an instance of Organization from a JSON string
organization_instance = Organization.from_json(json)
# print the JSON string representation of the object
print(Organization.to_json())

# convert the object into a dict
organization_dict = organization_instance.to_dict()
# create an instance of Organization from a dict
organization_from_dict = Organization.from_dict(organization_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


