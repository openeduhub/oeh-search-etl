# Contributor


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_property** | **str** |  | [optional] 
**firstname** | **str** |  | [optional] 
**lastname** | **str** |  | [optional] 
**email** | **str** |  | [optional] 
**vcard** | **str** |  | [optional] 
**org** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.contributor import Contributor

# TODO update the JSON string below
json = "{}"
# create an instance of Contributor from a JSON string
contributor_instance = Contributor.from_json(json)
# print the JSON string representation of the object
print(Contributor.to_json())

# convert the object into a dict
contributor_dict = contributor_instance.to_dict()
# create an instance of Contributor from a dict
contributor_from_dict = Contributor.from_dict(contributor_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


