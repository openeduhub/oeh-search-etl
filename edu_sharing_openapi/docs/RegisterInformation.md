# RegisterInformation


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**vcard** | **str** |  | [optional] 
**first_name** | **str** |  | [optional] 
**last_name** | **str** |  | [optional] 
**email** | **str** |  | [optional] 
**password** | **str** |  | [optional] 
**organization** | **str** |  | [optional] 
**allow_notifications** | **bool** |  | [optional] 
**authority_name** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.register_information import RegisterInformation

# TODO update the JSON string below
json = "{}"
# create an instance of RegisterInformation from a JSON string
register_information_instance = RegisterInformation.from_json(json)
# print the JSON string representation of the object
print(RegisterInformation.to_json())

# convert the object into a dict
register_information_dict = register_information_instance.to_dict()
# create an instance of RegisterInformation from a dict
register_information_from_dict = RegisterInformation.from_dict(register_information_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


