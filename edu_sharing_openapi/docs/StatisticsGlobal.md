# StatisticsGlobal


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**overall** | [**StatisticsGroup**](StatisticsGroup.md) |  | [optional] 
**groups** | [**List[StatisticsKeyGroup]**](StatisticsKeyGroup.md) |  | [optional] 
**user** | [**StatisticsUser**](StatisticsUser.md) |  | [optional] 

## Example

```python
from edu_sharing_client.models.statistics_global import StatisticsGlobal

# TODO update the JSON string below
json = "{}"
# create an instance of StatisticsGlobal from a JSON string
statistics_global_instance = StatisticsGlobal.from_json(json)
# print the JSON string representation of the object
print(StatisticsGlobal.to_json())

# convert the object into a dict
statistics_global_dict = statistics_global_instance.to_dict()
# create an instance of StatisticsGlobal from a dict
statistics_global_from_dict = StatisticsGlobal.from_dict(statistics_global_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


