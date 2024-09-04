# Suggest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**text** | **str** | suggested text | 
**highlighted** | **str** | suggested text with corrected words highlighted | [optional] 
**score** | **float** | score of the suggestion | 

## Example

```python
from edu_sharing_client.models.suggest import Suggest

# TODO update the JSON string below
json = "{}"
# create an instance of Suggest from a JSON string
suggest_instance = Suggest.from_json(json)
# print the JSON string representation of the object
print(Suggest.to_json())

# convert the object into a dict
suggest_dict = suggest_instance.to_dict()
# create an instance of Suggest from a dict
suggest_from_dict = Suggest.from_dict(suggest_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


