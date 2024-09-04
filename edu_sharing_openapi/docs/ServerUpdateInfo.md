# ServerUpdateInfo


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**order** | **int** |  | [optional] 
**auto** | **bool** |  | [optional] 
**testable** | **bool** |  | [optional] 
**executed_at** | **int** |  | [optional] 

## Example

```python
from edu_sharing_client.models.server_update_info import ServerUpdateInfo

# TODO update the JSON string below
json = "{}"
# create an instance of ServerUpdateInfo from a JSON string
server_update_info_instance = ServerUpdateInfo.from_json(json)
# print the JSON string representation of the object
print(ServerUpdateInfo.to_json())

# convert the object into a dict
server_update_info_dict = server_update_info_instance.to_dict()
# create an instance of ServerUpdateInfo from a dict
server_update_info_from_dict = ServerUpdateInfo.from_dict(server_update_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


