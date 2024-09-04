# ValueParameters


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**query** | **str** |  | 
**var_property** | **str** |  | 
**pattern** | **str** | prefix of the value (or \&quot;-all-\&quot; for all values) | 

## Example

```python
from edu_sharing_client.models.value_parameters import ValueParameters

# TODO update the JSON string below
json = "{}"
# create an instance of ValueParameters from a JSON string
value_parameters_instance = ValueParameters.from_json(json)
# print the JSON string representation of the object
print(ValueParameters.to_json())

# convert the object into a dict
value_parameters_dict = value_parameters_instance.to_dict()
# create an instance of ValueParameters from a dict
value_parameters_from_dict = ValueParameters.from_dict(value_parameters_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


