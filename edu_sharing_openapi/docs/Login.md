# Login


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**remote_authentications** | [**Dict[str, RemoteAuthDescription]**](RemoteAuthDescription.md) |  | [optional] 
**is_valid_login** | **bool** |  | 
**is_admin** | **bool** |  | 
**lti_session** | [**LTISession**](LTISession.md) |  | [optional] 
**current_scope** | **str** |  | 
**user_home** | **str** |  | [optional] 
**session_timeout** | **int** |  | 
**tool_permissions** | **List[str]** |  | [optional] 
**status_code** | **str** |  | [optional] 
**authority_name** | **str** |  | [optional] 
**is_guest** | **bool** |  | 

## Example

```python
from edu_sharing_client.models.login import Login

# TODO update the JSON string below
json = "{}"
# create an instance of Login from a JSON string
login_instance = Login.from_json(json)
# print the JSON string representation of the object
print(Login.to_json())

# convert the object into a dict
login_dict = login_instance.to_dict()
# create an instance of Login from a dict
login_from_dict = Login.from_dict(login_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


