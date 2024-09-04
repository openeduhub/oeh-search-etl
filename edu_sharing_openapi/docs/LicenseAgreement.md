# LicenseAgreement


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**node_id** | [**List[LicenseAgreementNode]**](LicenseAgreementNode.md) |  | [optional] 

## Example

```python
from edu_sharing_client.models.license_agreement import LicenseAgreement

# TODO update the JSON string below
json = "{}"
# create an instance of LicenseAgreement from a JSON string
license_agreement_instance = LicenseAgreement.from_json(json)
# print the JSON string representation of the object
print(LicenseAgreement.to_json())

# convert the object into a dict
license_agreement_dict = license_agreement_instance.to_dict()
# create an instance of LicenseAgreement from a dict
license_agreement_from_dict = LicenseAgreement.from_dict(license_agreement_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


