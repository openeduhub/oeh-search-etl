# ServiceVersion


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**repository** | **str** |  | [optional] 
**renderservice** | **str** |  | [optional] 
**major** | **int** |  | 
**minor** | **int** |  | 

## Example

```python
from edu_sharing_client.models.service_version import ServiceVersion

# TODO update the JSON string below
json = "{}"
# create an instance of ServiceVersion from a JSON string
service_version_instance = ServiceVersion.from_json(json)
# print the JSON string representation of the object
print(ServiceVersion.to_json())

# convert the object into a dict
service_version_dict = service_version_instance.to_dict()
# create an instance of ServiceVersion from a dict
service_version_from_dict = ServiceVersion.from_dict(service_version_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


