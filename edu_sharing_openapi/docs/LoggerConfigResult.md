# LoggerConfigResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**level** | **str** |  | [optional] 
**appender** | **List[str]** |  | [optional] 
**config** | **bool** |  | [optional] 

## Example

```python
from edu_sharing_client.models.logger_config_result import LoggerConfigResult

# TODO update the JSON string below
json = "{}"
# create an instance of LoggerConfigResult from a JSON string
logger_config_result_instance = LoggerConfigResult.from_json(json)
# print the JSON string representation of the object
print(LoggerConfigResult.to_json())

# convert the object into a dict
logger_config_result_dict = logger_config_result_instance.to_dict()
# create an instance of LoggerConfigResult from a dict
logger_config_result_from_dict = LoggerConfigResult.from_dict(logger_config_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


