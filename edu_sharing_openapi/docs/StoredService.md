# StoredService


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
**id** | **str** |  | [optional] 
**is_accessible_for_free** | **bool** |  | [optional] 

## Example

```python
from edu_sharing_client.models.stored_service import StoredService

# TODO update the JSON string below
json = "{}"
# create an instance of StoredService from a JSON string
stored_service_instance = StoredService.from_json(json)
# print the JSON string representation of the object
print(StoredService.to_json())

# convert the object into a dict
stored_service_dict = stored_service_instance.to_dict()
# create an instance of StoredService from a dict
stored_service_from_dict = StoredService.from_dict(stored_service_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


