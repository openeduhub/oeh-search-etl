# Suggestions


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**values** | [**List[Suggestion]**](Suggestion.md) |  | 

## Example

```python
from edu_sharing_client.models.suggestions import Suggestions

# TODO update the JSON string below
json = "{}"
# create an instance of Suggestions from a JSON string
suggestions_instance = Suggestions.from_json(json)
# print the JSON string representation of the object
print(Suggestions.to_json())

# convert the object into a dict
suggestions_dict = suggestions_instance.to_dict()
# create an instance of Suggestions from a dict
suggestions_from_dict = Suggestions.from_dict(suggestions_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


