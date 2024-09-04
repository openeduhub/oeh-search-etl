# ACE


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**editable** | **bool** |  | [optional] 
**authority** | [**Authority**](Authority.md) |  | 
**user** | [**UserProfile**](UserProfile.md) |  | [optional] 
**group** | [**GroupProfile**](GroupProfile.md) |  | [optional] 
**permissions** | **List[str]** |  | 

## Example

```python
from edu_sharing_client.models.ace import ACE

# TODO update the JSON string below
json = "{}"
# create an instance of ACE from a JSON string
ace_instance = ACE.from_json(json)
# print the JSON string representation of the object
print(ACE.to_json())

# convert the object into a dict
ace_dict = ace_instance.to_dict()
# create an instance of ACE from a dict
ace_from_dict = ACE.from_dict(ace_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


