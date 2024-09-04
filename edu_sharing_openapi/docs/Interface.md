# Interface


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | **str** |  | [optional] 
**set** | **str** |  | [optional] 
**metadata_prefix** | **str** |  | [optional] 
**documentation** | **str** |  | [optional] 
**format** | **str** |  | [optional] 
**type** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.interface import Interface

# TODO update the JSON string below
json = "{}"
# create an instance of Interface from a JSON string
interface_instance = Interface.from_json(json)
# print the JSON string representation of the object
print(Interface.to_json())

# convert the object into a dict
interface_dict = interface_instance.to_dict()
# create an instance of Interface from a dict
interface_from_dict = Interface.from_dict(interface_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


