# StatisticEntry


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_property** | **str** |  | 
**entities** | [**List[StatisticEntity]**](StatisticEntity.md) |  | 

## Example

```python
from edu_sharing_client.models.statistic_entry import StatisticEntry

# TODO update the JSON string below
json = "{}"
# create an instance of StatisticEntry from a JSON string
statistic_entry_instance = StatisticEntry.from_json(json)
# print the JSON string representation of the object
print(StatisticEntry.to_json())

# convert the object into a dict
statistic_entry_dict = statistic_entry_instance.to_dict()
# create an instance of StatisticEntry from a dict
statistic_entry_from_dict = StatisticEntry.from_dict(statistic_entry_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


