# RemoteAuthDescription


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | **str** |  | [optional] 
**token** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.remote_auth_description import RemoteAuthDescription

# TODO update the JSON string below
json = "{}"
# create an instance of RemoteAuthDescription from a JSON string
remote_auth_description_instance = RemoteAuthDescription.from_json(json)
# print the JSON string representation of the object
print(RemoteAuthDescription.to_json())

# convert the object into a dict
remote_auth_description_dict = remote_auth_description_instance.to_dict()
# create an instance of RemoteAuthDescription from a dict
remote_auth_description_from_dict = RemoteAuthDescription.from_dict(remote_auth_description_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


