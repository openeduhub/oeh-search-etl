# Preview


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**is_icon** | **bool** |  | 
**is_generated** | **bool** |  | [optional] 
**type** | **str** |  | [optional] 
**mimetype** | **str** |  | [optional] 
**data** | **bytearray** |  | [optional] 
**url** | **str** |  | 
**width** | **int** |  | 
**height** | **int** |  | 

## Example

```python
from edu_sharing_client.models.preview import Preview

# TODO update the JSON string below
json = "{}"
# create an instance of Preview from a JSON string
preview_instance = Preview.from_json(json)
# print the JSON string representation of the object
print(Preview.to_json())

# convert the object into a dict
preview_dict = preview_instance.to_dict()
# create an instance of Preview from a dict
preview_from_dict = Preview.from_dict(preview_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


