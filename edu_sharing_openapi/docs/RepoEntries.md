# RepoEntries


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**repositories** | [**List[Repo]**](Repo.md) |  | 

## Example

```python
from edu_sharing_client.models.repo_entries import RepoEntries

# TODO update the JSON string below
json = "{}"
# create an instance of RepoEntries from a JSON string
repo_entries_instance = RepoEntries.from_json(json)
# print the JSON string representation of the object
print(RepoEntries.to_json())

# convert the object into a dict
repo_entries_dict = repo_entries_instance.to_dict()
# create an instance of RepoEntries from a dict
repo_entries_from_dict = RepoEntries.from_dict(repo_entries_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


