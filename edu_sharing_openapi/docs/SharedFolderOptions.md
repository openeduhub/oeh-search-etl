# SharedFolderOptions


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**folders** | **str** |  | [optional] 
**private_files** | **str** |  | [optional] 
**cc_files** | **str** |  | [optional] 
**move** | **bool** |  | [optional] 

## Example

```python
from edu_sharing_client.models.shared_folder_options import SharedFolderOptions

# TODO update the JSON string below
json = "{}"
# create an instance of SharedFolderOptions from a JSON string
shared_folder_options_instance = SharedFolderOptions.from_json(json)
# print the JSON string representation of the object
print(SharedFolderOptions.to_json())

# convert the object into a dict
shared_folder_options_dict = shared_folder_options_instance.to_dict()
# create an instance of SharedFolderOptions from a dict
shared_folder_options_from_dict = SharedFolderOptions.from_dict(shared_folder_options_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


