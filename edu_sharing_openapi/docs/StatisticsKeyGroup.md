# StatisticsKeyGroup


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**key** | **str** |  | [optional] 
**display_name** | **str** |  | [optional] 
**count** | **int** |  | [optional] 
**sub_groups** | [**List[StatisticsSubGroup]**](StatisticsSubGroup.md) |  | [optional] 

## Example

```python
from edu_sharing_client.models.statistics_key_group import StatisticsKeyGroup

# TODO update the JSON string below
json = "{}"
# create an instance of StatisticsKeyGroup from a JSON string
statistics_key_group_instance = StatisticsKeyGroup.from_json(json)
# print the JSON string representation of the object
print(StatisticsKeyGroup.to_json())

# convert the object into a dict
statistics_key_group_dict = statistics_key_group_instance.to_dict()
# create an instance of StatisticsKeyGroup from a dict
statistics_key_group_from_dict = StatisticsKeyGroup.from_dict(statistics_key_group_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


