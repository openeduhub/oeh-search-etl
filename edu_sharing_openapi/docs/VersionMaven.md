# VersionMaven


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**bom** | **Dict[str, str]** |  | [optional] 
**project** | [**VersionProject**](VersionProject.md) |  | [optional] 

## Example

```python
from edu_sharing_client.models.version_maven import VersionMaven

# TODO update the JSON string below
json = "{}"
# create an instance of VersionMaven from a JSON string
version_maven_instance = VersionMaven.from_json(json)
# print the JSON string representation of the object
print(VersionMaven.to_json())

# convert the object into a dict
version_maven_dict = version_maven_instance.to_dict()
# create an instance of VersionMaven from a dict
version_maven_from_dict = VersionMaven.from_dict(version_maven_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


