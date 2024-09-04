# AdminStatistics


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**active_sessions** | **int** |  | [optional] 
**number_of_previews** | **int** |  | [optional] 
**max_memory** | **int** |  | [optional] 
**allocated_memory** | **int** |  | [optional] 
**preview_cache_size** | **int** |  | [optional] 
**active_locks** | [**List[Node]**](Node.md) |  | [optional] 

## Example

```python
from edu_sharing_client.models.admin_statistics import AdminStatistics

# TODO update the JSON string below
json = "{}"
# create an instance of AdminStatistics from a JSON string
admin_statistics_instance = AdminStatistics.from_json(json)
# print the JSON string representation of the object
print(AdminStatistics.to_json())

# convert the object into a dict
admin_statistics_dict = admin_statistics_instance.to_dict()
# create an instance of AdminStatistics from a dict
admin_statistics_from_dict = AdminStatistics.from_dict(admin_statistics_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


