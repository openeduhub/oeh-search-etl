# Application


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**title** | **str** |  | [optional] 
**webserver_url** | **str** |  | [optional] 
**client_base_url** | **str** |  | [optional] 
**type** | **str** |  | [optional] 
**subtype** | **str** |  | [optional] 
**repository_type** | **str** |  | [optional] 
**xml** | **str** |  | [optional] 
**file** | **str** |  | [optional] 
**content_url** | **str** |  | [optional] 
**config_url** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.application import Application

# TODO update the JSON string below
json = "{}"
# create an instance of Application from a JSON string
application_instance = Application.from_json(json)
# print the JSON string representation of the object
print(Application.to_json())

# convert the object into a dict
application_dict = application_instance.to_dict()
# create an instance of Application from a dict
application_from_dict = Application.from_dict(application_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


