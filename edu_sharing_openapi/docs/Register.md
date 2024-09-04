# Register


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**local** | **bool** |  | [optional] 
**recover_password** | **bool** |  | [optional] 
**login_url** | **str** |  | [optional] 
**recover_url** | **str** |  | [optional] 
**required_fields** | **List[str]** |  | [optional] 

## Example

```python
from edu_sharing_client.models.register import Register

# TODO update the JSON string below
json = "{}"
# create an instance of Register from a JSON string
register_instance = Register.from_json(json)
# print the JSON string representation of the object
print(Register.to_json())

# convert the object into a dict
register_dict = register_instance.to_dict()
# create an instance of Register from a dict
register_from_dict = Register.from_dict(register_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


