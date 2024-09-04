# Authority


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**properties** | **Dict[str, List[str]]** |  | [optional] 
**editable** | **bool** |  | [optional] 
**authority_name** | **str** |  | 
**authority_type** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.authority import Authority

# TODO update the JSON string below
json = "{}"
# create an instance of Authority from a JSON string
authority_instance = Authority.from_json(json)
# print the JSON string representation of the object
print(Authority.to_json())

# convert the object into a dict
authority_dict = authority_instance.to_dict()
# create an instance of Authority from a dict
authority_from_dict = Authority.from_dict(authority_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


