# AboutService


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**instances** | [**List[ServiceInstance]**](ServiceInstance.md) |  | 

## Example

```python
from edu_sharing_client.models.about_service import AboutService

# TODO update the JSON string below
json = "{}"
# create an instance of AboutService from a JSON string
about_service_instance = AboutService.from_json(json)
# print the JSON string representation of the object
print(AboutService.to_json())

# convert the object into a dict
about_service_dict = about_service_instance.to_dict()
# create an instance of AboutService from a dict
about_service_from_dict = AboutService.from_dict(about_service_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


