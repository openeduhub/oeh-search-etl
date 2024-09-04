# Pageable


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**page_number** | **int** |  | [optional] 
**unpaged** | **bool** |  | [optional] 
**offset** | **int** |  | [optional] 
**sort** | [**Sort**](Sort.md) |  | [optional] 
**paged** | **bool** |  | [optional] 
**page_size** | **int** |  | [optional] 

## Example

```python
from edu_sharing_client.models.pageable import Pageable

# TODO update the JSON string below
json = "{}"
# create an instance of Pageable from a JSON string
pageable_instance = Pageable.from_json(json)
# print the JSON string representation of the object
print(Pageable.to_json())

# convert the object into a dict
pageable_dict = pageable_instance.to_dict()
# create an instance of Pageable from a dict
pageable_from_dict = Pageable.from_dict(pageable_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


