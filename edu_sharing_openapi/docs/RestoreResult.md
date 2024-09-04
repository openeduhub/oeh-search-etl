# RestoreResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**archive_node_id** | **str** |  | 
**node_id** | **str** |  | 
**parent** | **str** |  | 
**path** | **str** |  | 
**name** | **str** |  | 
**restore_status** | **str** |  | 

## Example

```python
from edu_sharing_client.models.restore_result import RestoreResult

# TODO update the JSON string below
json = "{}"
# create an instance of RestoreResult from a JSON string
restore_result_instance = RestoreResult.from_json(json)
# print the JSON string representation of the object
print(RestoreResult.to_json())

# convert the object into a dict
restore_result_dict = restore_result_instance.to_dict()
# create an instance of RestoreResult from a dict
restore_result_from_dict = RestoreResult.from_dict(restore_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


