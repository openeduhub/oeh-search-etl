# Service


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**url** | **str** |  | [optional] 
**icon** | **str** |  | [optional] 
**logo** | **str** |  | [optional] 
**in_language** | **str** |  | [optional] 
**type** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**audience** | [**List[Audience]**](Audience.md) |  | [optional] 
**provider** | [**Provider**](Provider.md) |  | [optional] 
**start_date** | **str** |  | [optional] 
**interfaces** | [**List[Interface]**](Interface.md) |  | [optional] 
**about** | **List[str]** |  | [optional] 
**is_accessible_for_free** | **bool** |  | [optional] 

## Example

```python
from edu_sharing_client.models.service import Service

# TODO update the JSON string below
json = "{}"
# create an instance of Service from a JSON string
service_instance = Service.from_json(json)
# print the JSON string representation of the object
print(Service.to_json())

# convert the object into a dict
service_dict = service_instance.to_dict()
# create an instance of Service from a dict
service_from_dict = Service.from_dict(service_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


