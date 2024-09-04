# OpenIdConfiguration


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**issuer** | **str** |  | [optional] 
**token_endpoint** | **str** |  | [optional] 
**token_endpoint_auth_methods_supported** | **List[str]** |  | [optional] 
**token_endpoint_auth_signing_alg_values_supported** | **List[str]** |  | [optional] 
**jwks_uri** | **str** |  | [optional] 
**authorization_endpoint** | **str** |  | [optional] 
**registration_endpoint** | **str** |  | [optional] 
**scopes_supported** | **List[str]** |  | [optional] 
**response_types_supported** | **List[str]** |  | [optional] 
**subject_types_supported** | **List[str]** |  | [optional] 
**id_token_signing_alg_values_supported** | **List[str]** |  | [optional] 
**claims_supported** | **List[str]** |  | [optional] 
**https__purl_imsglobal_org_spec_lti_platform_configuration** | [**LTIPlatformConfiguration**](LTIPlatformConfiguration.md) |  | [optional] 

## Example

```python
from edu_sharing_client.models.open_id_configuration import OpenIdConfiguration

# TODO update the JSON string below
json = "{}"
# create an instance of OpenIdConfiguration from a JSON string
open_id_configuration_instance = OpenIdConfiguration.from_json(json)
# print the JSON string representation of the object
print(OpenIdConfiguration.to_json())

# convert the object into a dict
open_id_configuration_dict = open_id_configuration_instance.to_dict()
# create an instance of OpenIdConfiguration from a dict
open_id_configuration_from_dict = OpenIdConfiguration.from_dict(open_id_configuration_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


