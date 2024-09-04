# Mainnav


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**icon** | [**Icon**](Icon.md) |  | [optional] 
**main_menu_style** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.mainnav import Mainnav

# TODO update the JSON string below
json = "{}"
# create an instance of Mainnav from a JSON string
mainnav_instance = Mainnav.from_json(json)
# print the JSON string representation of the object
print(Mainnav.to_json())

# convert the object into a dict
mainnav_dict = mainnav_instance.to_dict()
# create an instance of Mainnav from a dict
mainnav_from_dict = Mainnav.from_dict(mainnav_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


