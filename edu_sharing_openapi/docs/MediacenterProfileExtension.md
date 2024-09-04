# MediacenterProfileExtension


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**location** | **str** |  | [optional] 
**district_abbreviation** | **str** |  | [optional] 
**main_url** | **str** |  | [optional] 
**catalogs** | [**List[Catalog]**](Catalog.md) |  | [optional] 
**content_status** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.mediacenter_profile_extension import MediacenterProfileExtension

# TODO update the JSON string below
json = "{}"
# create an instance of MediacenterProfileExtension from a JSON string
mediacenter_profile_extension_instance = MediacenterProfileExtension.from_json(json)
# print the JSON string representation of the object
print(MediacenterProfileExtension.to_json())

# convert the object into a dict
mediacenter_profile_extension_dict = mediacenter_profile_extension_instance.to_dict()
# create an instance of MediacenterProfileExtension from a dict
mediacenter_profile_extension_from_dict = MediacenterProfileExtension.from_dict(mediacenter_profile_extension_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


