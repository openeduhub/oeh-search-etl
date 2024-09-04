# GroupSignupDetails


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**signup_method** | **str** |  | [optional] 
**signup_password** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.group_signup_details import GroupSignupDetails

# TODO update the JSON string below
json = "{}"
# create an instance of GroupSignupDetails from a JSON string
group_signup_details_instance = GroupSignupDetails.from_json(json)
# print the JSON string representation of the object
print(GroupSignupDetails.to_json())

# convert the object into a dict
group_signup_details_dict = group_signup_details_instance.to_dict()
# create an instance of GroupSignupDetails from a dict
group_signup_details_from_dict = GroupSignupDetails.from_dict(group_signup_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


