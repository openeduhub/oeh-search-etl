# OpenIdRegistrationResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**client_id** | **str** |  | [optional] 
**response_types** | **List[str]** |  | [optional] 
**jwks_uri** | **str** |  | [optional] 
**initiate_login_uri** | **str** |  | [optional] 
**grant_types** | **List[str]** |  | [optional] 
**redirect_uris** | **List[str]** |  | [optional] 
**application_type** | **str** |  | [optional] 
**token_endpoint_auth_method** | **str** |  | [optional] 
**client_name** | **str** |  | [optional] 
**logo_uri** | **str** |  | [optional] 
**scope** | **str** |  | [optional] 
**https__purl_imsglobal_org_spec_lti_tool_configuration** | [**LTIToolConfiguration**](LTIToolConfiguration.md) |  | [optional] 

## Example

```python
from edu_sharing_client.models.open_id_registration_result import OpenIdRegistrationResult

# TODO update the JSON string below
json = "{}"
# create an instance of OpenIdRegistrationResult from a JSON string
open_id_registration_result_instance = OpenIdRegistrationResult.from_json(json)
# print the JSON string representation of the object
print(OpenIdRegistrationResult.to_json())

# convert the object into a dict
open_id_registration_result_dict = open_id_registration_result_instance.to_dict()
# create an instance of OpenIdRegistrationResult from a dict
open_id_registration_result_from_dict = OpenIdRegistrationResult.from_dict(open_id_registration_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


