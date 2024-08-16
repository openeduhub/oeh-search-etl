# CreateUsage


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**app_id** | **str** |  | [optional] 
**course_id** | **str** |  | [optional] 
**resource_id** | **str** |  | [optional] 
**node_id** | **str** |  | [optional] 
**node_version** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.create_usage import CreateUsage

# TODO update the JSON string below
json = "{}"
# create an instance of CreateUsage from a JSON string
create_usage_instance = CreateUsage.from_json(json)
# print the JSON string representation of the object
print(CreateUsage.to_json())

# convert the object into a dict
create_usage_dict = create_usage_instance.to_dict()
# create an instance of CreateUsage from a dict
create_usage_from_dict = CreateUsage.from_dict(create_usage_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


