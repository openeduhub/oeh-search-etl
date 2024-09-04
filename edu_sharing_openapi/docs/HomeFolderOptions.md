# HomeFolderOptions


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**folders** | **str** |  | [optional] 
**private_files** | **str** |  | [optional] 
**cc_files** | **str** |  | [optional] 
**keep_folder_structure** | **bool** |  | [optional] 

## Example

```python
from edu_sharing_client.models.home_folder_options import HomeFolderOptions

# TODO update the JSON string below
json = "{}"
# create an instance of HomeFolderOptions from a JSON string
home_folder_options_instance = HomeFolderOptions.from_json(json)
# print the JSON string representation of the object
print(HomeFolderOptions.to_json())

# convert the object into a dict
home_folder_options_dict = home_folder_options_instance.to_dict()
# create an instance of HomeFolderOptions from a dict
home_folder_options_from_dict = HomeFolderOptions.from_dict(home_folder_options_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


