# VersionProject


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**artifact_id** | **str** |  | [optional] 
**group_id** | **str** |  | [optional] 
**version** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.version_project import VersionProject

# TODO update the JSON string below
json = "{}"
# create an instance of VersionProject from a JSON string
version_project_instance = VersionProject.from_json(json)
# print the JSON string representation of the object
print(VersionProject.to_json())

# convert the object into a dict
version_project_dict = version_project_instance.to_dict()
# create an instance of VersionProject from a dict
version_project_from_dict = VersionProject.from_dict(version_project_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


