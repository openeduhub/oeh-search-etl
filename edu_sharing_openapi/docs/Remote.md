# Remote


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**repository** | [**Repo**](Repo.md) |  | [optional] 
**id** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.remote import Remote

# TODO update the JSON string below
json = "{}"
# create an instance of Remote from a JSON string
remote_instance = Remote.from_json(json)
# print the JSON string representation of the object
print(Remote.to_json())

# convert the object into a dict
remote_dict = remote_instance.to_dict()
# create an instance of Remote from a dict
remote_from_dict = Remote.from_dict(remote_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


