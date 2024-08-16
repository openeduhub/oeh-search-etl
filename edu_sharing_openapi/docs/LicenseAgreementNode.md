# LicenseAgreementNode


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**language** | **str** |  | [optional] 
**value** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.license_agreement_node import LicenseAgreementNode

# TODO update the JSON string below
json = "{}"
# create an instance of LicenseAgreementNode from a JSON string
license_agreement_node_instance = LicenseAgreementNode.from_json(json)
# print the JSON string representation of the object
print(LicenseAgreementNode.to_json())

# convert the object into a dict
license_agreement_node_dict = license_agreement_node_instance.to_dict()
# create an instance of LicenseAgreementNode from a dict
license_agreement_node_from_dict = LicenseAgreementNode.from_dict(license_agreement_node_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


