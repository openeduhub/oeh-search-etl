# Level


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**syslog_equivalent** | **int** |  | [optional] 
**version2_level** | [**Level**](Level.md) |  | [optional] 

## Example

```python
from edu_sharing_client.models.level import Level

# TODO update the JSON string below
json = "{}"
# create an instance of Level from a JSON string
level_instance = Level.from_json(json)
# print the JSON string representation of the object
print(Level.to_json())

# convert the object into a dict
level_dict = level_instance.to_dict()
# create an instance of Level from a dict
level_from_dict = Level.from_dict(level_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


