# CacheInfo


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**size** | **int** |  | [optional] 
**statistic_hits** | **int** |  | [optional] 
**name** | **str** |  | [optional] 
**backup_count** | **int** |  | [optional] 
**backup_entry_count** | **int** |  | [optional] 
**backup_entry_memory_cost** | **int** |  | [optional] 
**heap_cost** | **int** |  | [optional] 
**owned_entry_count** | **int** |  | [optional] 
**get_owned_entry_memory_cost** | **int** |  | [optional] 
**size_in_memory** | **int** |  | [optional] 
**member** | **str** |  | [optional] 
**group_name** | **str** |  | [optional] 
**max_size** | **int** |  | [optional] 

## Example

```python
from edu_sharing_client.models.cache_info import CacheInfo

# TODO update the JSON string below
json = "{}"
# create an instance of CacheInfo from a JSON string
cache_info_instance = CacheInfo.from_json(json)
# print the JSON string representation of the object
print(CacheInfo.to_json())

# convert the object into a dict
cache_info_dict = cache_info_instance.to_dict()
# create an instance of CacheInfo from a dict
cache_info_from_dict = CacheInfo.from_dict(cache_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


