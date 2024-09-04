# StatisticsSubGroup


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**count** | [**List[SubGroupItem]**](SubGroupItem.md) |  | [optional] 

## Example

```python
from edu_sharing_client.models.statistics_sub_group import StatisticsSubGroup

# TODO update the JSON string below
json = "{}"
# create an instance of StatisticsSubGroup from a JSON string
statistics_sub_group_instance = StatisticsSubGroup.from_json(json)
# print the JSON string representation of the object
print(StatisticsSubGroup.to_json())

# convert the object into a dict
statistics_sub_group_dict = statistics_sub_group_instance.to_dict()
# create an instance of StatisticsSubGroup from a dict
statistics_sub_group_from_dict = StatisticsSubGroup.from_dict(statistics_sub_group_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


