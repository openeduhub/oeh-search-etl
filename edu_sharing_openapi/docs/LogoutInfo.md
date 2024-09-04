# LogoutInfo


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | **str** |  | [optional] 
**destroy_session** | **bool** |  | [optional] 
**ajax** | **bool** |  | [optional] 
**next** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.logout_info import LogoutInfo

# TODO update the JSON string below
json = "{}"
# create an instance of LogoutInfo from a JSON string
logout_info_instance = LogoutInfo.from_json(json)
# print the JSON string representation of the object
print(LogoutInfo.to_json())

# convert the object into a dict
logout_info_dict = logout_info_instance.to_dict()
# create an instance of LogoutInfo from a dict
logout_info_from_dict = LogoutInfo.from_dict(logout_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


