# AuthenticationToken


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_id** | **str** |  | [optional] 
**ticket** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.authentication_token import AuthenticationToken

# TODO update the JSON string below
json = "{}"
# create an instance of AuthenticationToken from a JSON string
authentication_token_instance = AuthenticationToken.from_json(json)
# print the JSON string representation of the object
print(AuthenticationToken.to_json())

# convert the object into a dict
authentication_token_dict = authentication_token_instance.to_dict()
# create an instance of AuthenticationToken from a dict
authentication_token_from_dict = AuthenticationToken.from_dict(authentication_token_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


