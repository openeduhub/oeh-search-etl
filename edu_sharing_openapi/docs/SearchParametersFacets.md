# SearchParametersFacets


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**facets** | **List[str]** |  | 
**facet_min_count** | **int** |  | [optional] [default to 5]
**facet_limit** | **int** |  | [optional] [default to 10]
**facet_suggest** | **str** |  | [optional] 
**criteria** | [**List[MdsQueryCriteria]**](MdsQueryCriteria.md) |  | 

## Example

```python
from edu_sharing_client.models.search_parameters_facets import SearchParametersFacets

# TODO update the JSON string below
json = "{}"
# create an instance of SearchParametersFacets from a JSON string
search_parameters_facets_instance = SearchParametersFacets.from_json(json)
# print the JSON string representation of the object
print(SearchParametersFacets.to_json())

# convert the object into a dict
search_parameters_facets_dict = search_parameters_facets_instance.to_dict()
# create an instance of SearchParametersFacets from a dict
search_parameters_facets_from_dict = SearchParametersFacets.from_dict(search_parameters_facets_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


