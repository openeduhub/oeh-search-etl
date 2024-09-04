# SearchResultLrmi


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**suggests** | [**List[Suggest]**](Suggest.md) |  | [optional] 
**nodes** | **List[str]** |  | 
**pagination** | [**Pagination**](Pagination.md) |  | 
**facets** | [**List[Facet]**](Facet.md) |  | 
**ignored** | **List[str]** |  | [optional] 

## Example

```python
from edu_sharing_client.models.search_result_lrmi import SearchResultLrmi

# TODO update the JSON string below
json = "{}"
# create an instance of SearchResultLrmi from a JSON string
search_result_lrmi_instance = SearchResultLrmi.from_json(json)
# print the JSON string representation of the object
print(SearchResultLrmi.to_json())

# convert the object into a dict
search_result_lrmi_dict = search_result_lrmi_instance.to_dict()
# create an instance of SearchResultLrmi from a dict
search_result_lrmi_from_dict = SearchResultLrmi.from_dict(search_result_lrmi_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


