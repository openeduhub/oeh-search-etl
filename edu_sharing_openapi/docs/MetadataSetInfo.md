# MetadataSetInfo


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**name** | **str** |  | 

## Example

```python
from edu_sharing_client.models.metadata_set_info import MetadataSetInfo

# TODO update the JSON string below
json = "{}"
# create an instance of MetadataSetInfo from a JSON string
metadata_set_info_instance = MetadataSetInfo.from_json(json)
# print the JSON string representation of the object
print(MetadataSetInfo.to_json())

# convert the object into a dict
metadata_set_info_dict = metadata_set_info_instance.to_dict()
# create an instance of MetadataSetInfo from a dict
metadata_set_info_from_dict = MetadataSetInfo.from_dict(metadata_set_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


