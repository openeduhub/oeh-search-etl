# Connector


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**icon** | **str** |  | [optional] 
**show_new** | **bool** | false | 
**parameters** | **List[str]** |  | [optional] 
**filetypes** | [**List[ConnectorFileType]**](ConnectorFileType.md) |  | [optional] 
**only_desktop** | **bool** |  | [optional] 
**has_view_mode** | **bool** |  | [optional] 

## Example

```python
from edu_sharing_client.models.connector import Connector

# TODO update the JSON string below
json = "{}"
# create an instance of Connector from a JSON string
connector_instance = Connector.from_json(json)
# print the JSON string representation of the object
print(Connector.to_json())

# convert the object into a dict
connector_dict = connector_instance.to_dict()
# create an instance of Connector from a dict
connector_from_dict = Connector.from_dict(connector_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


