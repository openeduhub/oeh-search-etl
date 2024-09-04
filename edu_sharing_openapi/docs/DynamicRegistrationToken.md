# DynamicRegistrationToken


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**token** | **str** |  | [optional] 
**url** | **str** |  | [optional] 
**registered_app_id** | **str** |  | [optional] 
**ts_created** | **int** |  | [optional] 
**ts_expiry** | **int** |  | [optional] 
**valid** | **bool** |  | [optional] 

## Example

```python
from edu_sharing_client.models.dynamic_registration_token import DynamicRegistrationToken

# TODO update the JSON string below
json = "{}"
# create an instance of DynamicRegistrationToken from a JSON string
dynamic_registration_token_instance = DynamicRegistrationToken.from_json(json)
# print the JSON string representation of the object
print(DynamicRegistrationToken.to_json())

# convert the object into a dict
dynamic_registration_token_dict = dynamic_registration_token_instance.to_dict()
# create an instance of DynamicRegistrationToken from a dict
dynamic_registration_token_from_dict = DynamicRegistrationToken.from_dict(dynamic_registration_token_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


