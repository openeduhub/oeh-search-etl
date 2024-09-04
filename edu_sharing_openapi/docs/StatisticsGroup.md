# StatisticsGroup


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **int** |  | [optional] 
**sub_groups** | [**List[StatisticsSubGroup]**](StatisticsSubGroup.md) |  | [optional] 

## Example

```python
from edu_sharing_client.models.statistics_group import StatisticsGroup

# TODO update the JSON string below
json = "{}"
# create an instance of StatisticsGroup from a JSON string
statistics_group_instance = StatisticsGroup.from_json(json)
# print the JSON string representation of the object
print(StatisticsGroup.to_json())

# convert the object into a dict
statistics_group_dict = statistics_group_instance.to_dict()
# create an instance of StatisticsGroup from a dict
statistics_group_from_dict = StatisticsGroup.from_dict(statistics_group_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


