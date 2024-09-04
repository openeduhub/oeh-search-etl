# SharingInfo


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**password_matches** | **bool** |  | [optional] 
**password** | **bool** |  | [optional] 
**expired** | **bool** |  | [optional] 
**invited_by** | [**Person**](Person.md) |  | [optional] 
**node** | [**Node**](Node.md) |  | [optional] 

## Example

```python
from edu_sharing_client.models.sharing_info import SharingInfo

# TODO update the JSON string below
json = "{}"
# create an instance of SharingInfo from a JSON string
sharing_info_instance = SharingInfo.from_json(json)
# print the JSON string representation of the object
print(SharingInfo.to_json())

# convert the object into a dict
sharing_info_dict = sharing_info_instance.to_dict()
# create an instance of SharingInfo from a dict
sharing_info_from_dict = SharingInfo.from_dict(sharing_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


