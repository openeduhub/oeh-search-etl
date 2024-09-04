# RepositoryVersionInfo


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**version** | [**Version**](Version.md) |  | [optional] 
**maven** | [**VersionMaven**](VersionMaven.md) |  | [optional] 
**git** | [**VersionGit**](VersionGit.md) |  | [optional] 
**build** | [**VersionBuild**](VersionBuild.md) |  | [optional] 

## Example

```python
from edu_sharing_client.models.repository_version_info import RepositoryVersionInfo

# TODO update the JSON string below
json = "{}"
# create an instance of RepositoryVersionInfo from a JSON string
repository_version_info_instance = RepositoryVersionInfo.from_json(json)
# print the JSON string representation of the object
print(RepositoryVersionInfo.to_json())

# convert the object into a dict
repository_version_info_dict = repository_version_info_instance.to_dict()
# create an instance of RepositoryVersionInfo from a dict
repository_version_info_from_dict = RepositoryVersionInfo.from_dict(repository_version_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


