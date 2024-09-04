# ManualRegistrationData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tool_name** | **str** |  | [optional] 
**tool_url** | **str** |  | [optional] 
**tool_description** | **str** |  | [optional] 
**keyset_url** | **str** |  | [optional] 
**login_initiation_url** | **str** |  | [optional] 
**redirection_urls** | **List[str]** |  | [optional] 
**custom_parameters** | **List[str]** | JSON Object where each value is a string. Custom parameters to be included in each launch to this tool. If a custom parameter is also defined at the message level, the message level value takes precedence. The value of the custom parameters may be substitution parameters as described in the LTI Core [LTI-13] specification.  | [optional] 
**logo_url** | **str** |  | [optional] 
**target_link_uri** | **str** | The default target link uri to use unless defined otherwise in the message or link definition | 
**target_link_uri_deep_link** | **str** | The target link uri to use for DeepLing Message | [optional] 
**client_name** | **str** | Name of the Tool to be presented to the End-User. Localized representations may be included as described in Section 2.1 of the [OIDC-Reg] specification.  | 

## Example

```python
from edu_sharing_client.models.manual_registration_data import ManualRegistrationData

# TODO update the JSON string below
json = "{}"
# create an instance of ManualRegistrationData from a JSON string
manual_registration_data_instance = ManualRegistrationData.from_json(json)
# print the JSON string representation of the object
print(ManualRegistrationData.to_json())

# convert the object into a dict
manual_registration_data_dict = manual_registration_data_instance.to_dict()
# create an instance of ManualRegistrationData from a dict
manual_registration_data_from_dict = ManualRegistrationData.from_dict(manual_registration_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


