# SearchResultElastic


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**suggests** | [**List[Suggest]**](Suggest.md) |  | [optional] 
**elastic_response** | **str** |  | [optional] 
**nodes** | **List[object]** |  | 
**pagination** | [**Pagination**](Pagination.md) |  | 
**facets** | [**List[Facet]**](Facet.md) |  | 
**ignored** | **List[str]** |  | [optional] 

## Example

```python
from edu_sharing_client.models.search_result_elastic import SearchResultElastic

# TODO update the JSON string below
json = "{}"
# create an instance of SearchResultElastic from a JSON string
search_result_elastic_instance = SearchResultElastic.from_json(json)
# print the JSON string representation of the object
print(SearchResultElastic.to_json())

# convert the object into a dict
search_result_elastic_dict = search_result_elastic_instance.to_dict()
# create an instance of SearchResultElastic from a dict
search_result_elastic_from_dict = SearchResultElastic.from_dict(search_result_elastic_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


