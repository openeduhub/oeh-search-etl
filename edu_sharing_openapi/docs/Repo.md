# Repo


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**repository_type** | **str** |  | [optional] 
**rendering_supported** | **bool** |  | [optional] 
**id** | **str** |  | [optional] 
**title** | **str** |  | [optional] 
**icon** | **str** |  | [optional] 
**logo** | **str** |  | [optional] 
**is_home_repo** | **bool** |  | [optional] 

## Example

```python
from edu_sharing_client.models.repo import Repo

# TODO update the JSON string below
json = "{}"
# create an instance of Repo from a JSON string
repo_instance = Repo.from_json(json)
# print the JSON string representation of the object
print(Repo.to_json())

# convert the object into a dict
repo_dict = repo_instance.to_dict()
# create an instance of Repo from a dict
repo_from_dict = Repo.from_dict(repo_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


