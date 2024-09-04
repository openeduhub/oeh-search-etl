# SearchParameters


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**permissions** | **List[str]** |  | [optional] 
**resolve_collections** | **bool** |  | [optional] 
**resolve_usernames** | **bool** |  | [optional] 
**return_suggestions** | **bool** |  | [optional] 
**excludes** | **List[str]** |  | [optional] 
**facets** | **List[str]** |  | [optional] 
**facet_min_count** | **int** |  | [optional] [default to 5]
**facet_limit** | **int** |  | [optional] [default to 10]
**facet_suggest** | **str** |  | [optional] 
**criteria** | [**List[MdsQueryCriteria]**](MdsQueryCriteria.md) |  | 

## Example

```python
from edu_sharing_client.models.search_parameters import SearchParameters

# TODO update the JSON string below
json = "{}"
# create an instance of SearchParameters from a JSON string
search_parameters_instance = SearchParameters.from_json(json)
# print the JSON string representation of the object
print(SearchParameters.to_json())

# convert the object into a dict
search_parameters_dict = search_parameters_instance.to_dict()
# create an instance of SearchParameters from a dict
search_parameters_from_dict = SearchParameters.from_dict(search_parameters_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


