# ProfileSettings


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**show_email** | **bool** | false | 

## Example

```python
from edu_sharing_client.models.profile_settings import ProfileSettings

# TODO update the JSON string below
json = "{}"
# create an instance of ProfileSettings from a JSON string
profile_settings_instance = ProfileSettings.from_json(json)
# print the JSON string representation of the object
print(ProfileSettings.to_json())

# convert the object into a dict
profile_settings_dict = profile_settings_instance.to_dict()
# create an instance of ProfileSettings from a dict
profile_settings_from_dict = ProfileSettings.from_dict(profile_settings_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


