# ACL


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**inherited** | **bool** |  | 
**permissions** | [**List[ACE]**](ACE.md) |  | 

## Example

```python
from edu_sharing_client.models.acl import ACL

# TODO update the JSON string below
json = "{}"
# create an instance of ACL from a JSON string
acl_instance = ACL.from_json(json)
# print the JSON string representation of the object
print(ACL.to_json())

# convert the object into a dict
acl_dict = acl_instance.to_dict()
# create an instance of ACL from a dict
acl_from_dict = ACL.from_dict(acl_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


