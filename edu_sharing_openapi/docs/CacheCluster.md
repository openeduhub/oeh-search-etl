# CacheCluster


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**instances** | [**List[CacheMember]**](CacheMember.md) |  | [optional] 
**cache_infos** | [**List[CacheInfo]**](CacheInfo.md) |  | [optional] 
**local_member** | **str** |  | [optional] 
**free_memory** | **int** |  | [optional] 
**total_memory** | **int** |  | [optional] 
**max_memory** | **int** |  | [optional] 
**available_processors** | **int** |  | [optional] 
**time_stamp** | **datetime** |  | [optional] 
**group_name** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.cache_cluster import CacheCluster

# TODO update the JSON string below
json = "{}"
# create an instance of CacheCluster from a JSON string
cache_cluster_instance = CacheCluster.from_json(json)
# print the JSON string representation of the object
print(CacheCluster.to_json())

# convert the object into a dict
cache_cluster_dict = cache_cluster_instance.to_dict()
# create an instance of CacheCluster from a dict
cache_cluster_from_dict = CacheCluster.from_dict(cache_cluster_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


