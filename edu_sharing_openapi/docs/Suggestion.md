# Suggestion


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**replacement_string** | **str** |  | 
**display_string** | **str** |  | 
**key** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.suggestion import Suggestion

# TODO update the JSON string below
json = "{}"
# create an instance of Suggestion from a JSON string
suggestion_instance = Suggestion.from_json(json)
# print the JSON string representation of the object
print(Suggestion.to_json())

# convert the object into a dict
suggestion_dict = suggestion_instance.to_dict()
# create an instance of Suggestion from a dict
suggestion_from_dict = Suggestion.from_dict(suggestion_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


