# ConnectorFileType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ccressourceversion** | **str** |  | [optional] 
**ccressourcetype** | **str** |  | [optional] 
**ccresourcesubtype** | **str** |  | [optional] 
**editor_type** | **str** |  | [optional] 
**mimetype** | **str** |  | [optional] 
**filetype** | **str** |  | [optional] 
**creatable** | **bool** |  | [optional] 
**editable** | **bool** |  | [optional] 

## Example

```python
from edu_sharing_client.models.connector_file_type import ConnectorFileType

# TODO update the JSON string below
json = "{}"
# create an instance of ConnectorFileType from a JSON string
connector_file_type_instance = ConnectorFileType.from_json(json)
# print the JSON string representation of the object
print(ConnectorFileType.to_json())

# convert the object into a dict
connector_file_type_dict = connector_file_type_instance.to_dict()
# create an instance of ConnectorFileType from a dict
connector_file_type_from_dict = ConnectorFileType.from_dict(connector_file_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


