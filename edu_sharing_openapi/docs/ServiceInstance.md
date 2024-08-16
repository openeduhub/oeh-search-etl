# ServiceInstance


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**version** | [**ServiceVersion**](ServiceVersion.md) |  | 
**endpoint** | **str** |  | 

## Example

```python
from edu_sharing_client.models.service_instance import ServiceInstance

# TODO update the JSON string below
json = "{}"
# create an instance of ServiceInstance from a JSON string
service_instance_instance = ServiceInstance.from_json(json)
# print the JSON string representation of the object
print(ServiceInstance.to_json())

# convert the object into a dict
service_instance_dict = service_instance_instance.to_dict()
# create an instance of ServiceInstance from a dict
service_instance_from_dict = ServiceInstance.from_dict(service_instance_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


