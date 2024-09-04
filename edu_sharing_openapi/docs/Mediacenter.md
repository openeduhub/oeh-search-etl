# Mediacenter


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**properties** | **Dict[str, List[str]]** |  | [optional] 
**editable** | **bool** |  | [optional] 
**signup_method** | **str** |  | [optional] 
**ref** | [**NodeRef**](NodeRef.md) |  | [optional] 
**aspects** | **List[str]** |  | [optional] 
**organizations** | [**List[Organization]**](Organization.md) |  | [optional] 
**authority_name** | **str** |  | 
**authority_type** | **str** |  | [optional] 
**group_name** | **str** |  | [optional] 
**profile** | [**GroupProfile**](GroupProfile.md) |  | [optional] 
**administration_access** | **bool** |  | [optional] 

## Example

```python
from edu_sharing_client.models.mediacenter import Mediacenter

# TODO update the JSON string below
json = "{}"
# create an instance of Mediacenter from a JSON string
mediacenter_instance = Mediacenter.from_json(json)
# print the JSON string representation of the object
print(Mediacenter.to_json())

# convert the object into a dict
mediacenter_dict = mediacenter_instance.to_dict()
# create an instance of Mediacenter from a dict
mediacenter_from_dict = Mediacenter.from_dict(mediacenter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


