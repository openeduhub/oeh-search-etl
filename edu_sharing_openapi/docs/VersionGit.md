# VersionGit


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**branch** | **str** |  | [optional] 
**commit** | [**VersionGitCommit**](VersionGitCommit.md) |  | [optional] 

## Example

```python
from edu_sharing_client.models.version_git import VersionGit

# TODO update the JSON string below
json = "{}"
# create an instance of VersionGit from a JSON string
version_git_instance = VersionGit.from_json(json)
# print the JSON string representation of the object
print(VersionGit.to_json())

# convert the object into a dict
version_git_dict = version_git_instance.to_dict()
# create an instance of VersionGit from a dict
version_git_from_dict = VersionGit.from_dict(version_git_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


