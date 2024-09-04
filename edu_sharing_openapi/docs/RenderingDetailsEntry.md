# RenderingDetailsEntry


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**details_snippet** | **str** |  | 
**mime_type** | **str** |  | 
**node** | [**Node**](Node.md) |  | 

## Example

```python
from edu_sharing_client.models.rendering_details_entry import RenderingDetailsEntry

# TODO update the JSON string below
json = "{}"
# create an instance of RenderingDetailsEntry from a JSON string
rendering_details_entry_instance = RenderingDetailsEntry.from_json(json)
# print the JSON string representation of the object
print(RenderingDetailsEntry.to_json())

# convert the object into a dict
rendering_details_entry_dict = rendering_details_entry_instance.to_dict()
# create an instance of RenderingDetailsEntry from a dict
rendering_details_entry_from_dict = RenderingDetailsEntry.from_dict(rendering_details_entry_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


