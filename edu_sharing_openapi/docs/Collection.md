# Collection


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**scope** | **str** |  | [optional] 
**author_freetext** | **str** |  | [optional] 
**order_ascending** | **bool** |  | [optional] 
**level0** | **bool** | false | 
**title** | **str** |  | 
**description** | **str** |  | [optional] 
**type** | **str** |  | 
**viewtype** | **str** |  | 
**order_mode** | **str** |  | [optional] 
**x** | **int** |  | [optional] 
**y** | **int** |  | [optional] 
**z** | **int** |  | [optional] 
**color** | **str** |  | [optional] 
**from_user** | **bool** | false | 
**pinned** | **bool** |  | [optional] 
**child_collections_count** | **int** |  | [optional] 
**child_references_count** | **int** |  | [optional] 

## Example

```python
from edu_sharing_client.models.collection import Collection

# TODO update the JSON string below
json = "{}"
# create an instance of Collection from a JSON string
collection_instance = Collection.from_json(json)
# print the JSON string representation of the object
print(Collection.to_json())

# convert the object into a dict
collection_dict = collection_instance.to_dict()
# create an instance of Collection from a dict
collection_from_dict = Collection.from_dict(collection_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


