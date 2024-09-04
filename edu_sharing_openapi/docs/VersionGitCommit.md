# VersionGitCommit


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**timestamp** | [**VersionTimestamp**](VersionTimestamp.md) |  | [optional] 

## Example

```python
from edu_sharing_client.models.version_git_commit import VersionGitCommit

# TODO update the JSON string below
json = "{}"
# create an instance of VersionGitCommit from a JSON string
version_git_commit_instance = VersionGitCommit.from_json(json)
# print the JSON string representation of the object
print(VersionGitCommit.to_json())

# convert the object into a dict
version_git_commit_dict = version_git_commit_instance.to_dict()
# create an instance of VersionGitCommit from a dict
version_git_commit_from_dict = VersionGitCommit.from_dict(version_git_commit_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


