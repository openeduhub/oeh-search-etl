# SuggestionParam


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**value_parameters** | [**ValueParameters**](ValueParameters.md) |  | [optional] 
**criteria** | [**List[MdsQueryCriteria]**](MdsQueryCriteria.md) |  | [optional] 

## Example

```python
from edu_sharing_client.models.suggestion_param import SuggestionParam

# TODO update the JSON string below
json = "{}"
# create an instance of SuggestionParam from a JSON string
suggestion_param_instance = SuggestionParam.from_json(json)
# print the JSON string representation of the object
print(SuggestionParam.to_json())

# convert the object into a dict
suggestion_param_dict = suggestion_param_instance.to_dict()
# create an instance of SuggestionParam from a dict
suggestion_param_from_dict = SuggestionParam.from_dict(suggestion_param_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


