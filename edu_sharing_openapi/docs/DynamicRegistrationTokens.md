# DynamicRegistrationTokens


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**registration_links** | [**List[DynamicRegistrationToken]**](DynamicRegistrationToken.md) |  | [optional] 

## Example

```python
from edu_sharing_client.models.dynamic_registration_tokens import DynamicRegistrationTokens

# TODO update the JSON string below
json = "{}"
# create an instance of DynamicRegistrationTokens from a JSON string
dynamic_registration_tokens_instance = DynamicRegistrationTokens.from_json(json)
# print the JSON string representation of the object
print(DynamicRegistrationTokens.to_json())

# convert the object into a dict
dynamic_registration_tokens_dict = dynamic_registration_tokens_instance.to_dict()
# create an instance of DynamicRegistrationTokens from a dict
dynamic_registration_tokens_from_dict = DynamicRegistrationTokens.from_dict(dynamic_registration_tokens_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


