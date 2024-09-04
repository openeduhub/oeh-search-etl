# SearchResultNode


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**suggests** | [**List[Suggest]**](Suggest.md) |  | [optional] 
**nodes** | [**List[Node]**](Node.md) |  | 
**pagination** | [**Pagination**](Pagination.md) |  | 
**facets** | [**List[Facet]**](Facet.md) |  | 
**ignored** | **List[str]** |  | [optional] 

## Example

```python
from edu_sharing_client.models.search_result_node import SearchResultNode

# TODO update the JSON string below
json = "{}"
# create an instance of SearchResultNode from a JSON string
search_result_node_instance = SearchResultNode.from_json(json)
# print the JSON string representation of the object
print(SearchResultNode.to_json())

# convert the object into a dict
search_result_node_dict = search_result_node_instance.to_dict()
# create an instance of SearchResultNode from a dict
search_result_node_from_dict = SearchResultNode.from_dict(search_result_node_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


