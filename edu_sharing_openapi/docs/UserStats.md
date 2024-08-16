# UserStats


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**node_count** | **int** |  | [optional] 
**node_count_cc** | **int** |  | [optional] 
**collection_count** | **int** |  | [optional] 

## Example

```python
from edu_sharing_client.models.user_stats import UserStats

# TODO update the JSON string below
json = "{}"
# create an instance of UserStats from a JSON string
user_stats_instance = UserStats.from_json(json)
# print the JSON string representation of the object
print(UserStats.to_json())

# convert the object into a dict
user_stats_dict = user_stats_instance.to_dict()
# create an instance of UserStats from a dict
user_stats_from_dict = UserStats.from_dict(user_stats_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


