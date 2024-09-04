# Usage


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**from_used** | **datetime** |  | [optional] 
**to_used** | **datetime** |  | [optional] 
**usage_counter** | **int** |  | [optional] 
**app_subtype** | **str** |  | [optional] 
**app_type** | **str** |  | [optional] 
**type** | **str** |  | [optional] 
**created** | **datetime** |  | [optional] 
**modified** | **datetime** |  | [optional] 
**app_user** | **str** |  | 
**app_user_mail** | **str** |  | 
**course_id** | **str** |  | 
**distinct_persons** | **int** |  | [optional] 
**app_id** | **str** |  | 
**node_id** | **str** |  | 
**parent_node_id** | **str** |  | 
**usage_version** | **str** |  | 
**usage_xml_params** | [**Parameters**](Parameters.md) |  | [optional] 
**usage_xml_params_raw** | **str** |  | [optional] 
**resource_id** | **str** |  | 
**guid** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.usage import Usage

# TODO update the JSON string below
json = "{}"
# create an instance of Usage from a JSON string
usage_instance = Usage.from_json(json)
# print the JSON string representation of the object
print(Usage.to_json())

# convert the object into a dict
usage_dict = usage_instance.to_dict()
# create an instance of Usage from a dict
usage_from_dict = Usage.from_dict(usage_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


