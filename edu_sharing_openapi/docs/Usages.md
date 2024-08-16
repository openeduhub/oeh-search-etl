# Usages


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**usages** | [**List[Usage]**](Usage.md) |  | [optional] 

## Example

```python
from edu_sharing_client.models.usages import Usages

# TODO update the JSON string below
json = "{}"
# create an instance of Usages from a JSON string
usages_instance = Usages.from_json(json)
# print the JSON string representation of the object
print(Usages.to_json())

# convert the object into a dict
usages_dict = usages_instance.to_dict()
# create an instance of Usages from a dict
usages_from_dict = Usages.from_dict(usages_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


