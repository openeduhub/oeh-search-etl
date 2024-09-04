# PersonDeleteOptions


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cleanup_metadata** | **bool** |  | [optional] 
**home_folder** | [**HomeFolderOptions**](HomeFolderOptions.md) |  | [optional] 
**shared_folders** | [**SharedFolderOptions**](SharedFolderOptions.md) |  | [optional] 
**collections** | [**CollectionOptions**](CollectionOptions.md) |  | [optional] 
**ratings** | [**DeleteOption**](DeleteOption.md) |  | [optional] 
**comments** | [**DeleteOption**](DeleteOption.md) |  | [optional] 
**collection_feedback** | [**DeleteOption**](DeleteOption.md) |  | [optional] 
**statistics** | [**DeleteOption**](DeleteOption.md) |  | [optional] 
**stream** | [**DeleteOption**](DeleteOption.md) |  | [optional] 
**receiver** | **str** |  | [optional] 
**receiver_group** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.person_delete_options import PersonDeleteOptions

# TODO update the JSON string below
json = "{}"
# create an instance of PersonDeleteOptions from a JSON string
person_delete_options_instance = PersonDeleteOptions.from_json(json)
# print the JSON string representation of the object
print(PersonDeleteOptions.to_json())

# convert the object into a dict
person_delete_options_dict = person_delete_options_instance.to_dict()
# create an instance of PersonDeleteOptions from a dict
person_delete_options_from_dict = PersonDeleteOptions.from_dict(person_delete_options_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


