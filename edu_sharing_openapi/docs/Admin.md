# Admin


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**statistics** | [**Statistics**](Statistics.md) |  | [optional] 
**editor_type** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.admin import Admin

# TODO update the JSON string below
json = "{}"
# create an instance of Admin from a JSON string
admin_instance = Admin.from_json(json)
# print the JSON string representation of the object
print(Admin.to_json())

# convert the object into a dict
admin_dict = admin_instance.to_dict()
# create an instance of Admin from a dict
admin_from_dict = Admin.from_dict(admin_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


