# General


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**referenced_in_name** | **str** |  | [optional] 
**referenced_in_type** | **str** |  | [optional] 
**referenced_in_instance** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.general import General

# TODO update the JSON string below
json = "{}"
# create an instance of General from a JSON string
general_instance = General.from_json(json)
# print the JSON string representation of the object
print(General.to_json())

# convert the object into a dict
general_dict = general_instance.to_dict()
# create an instance of General from a dict
general_from_dict = General.from_dict(general_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


