# Frontpage


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total_count** | **int** |  | [optional] 
**display_count** | **int** |  | [optional] 
**mode** | **str** |  | [optional] 
**timespan** | **int** |  | [optional] 
**timespan_all** | **bool** |  | [optional] 
**queries** | [**List[Query]**](Query.md) |  | [optional] 
**collection** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.frontpage import Frontpage

# TODO update the JSON string below
json = "{}"
# create an instance of Frontpage from a JSON string
frontpage_instance = Frontpage.from_json(json)
# print the JSON string representation of the object
print(Frontpage.to_json())

# convert the object into a dict
frontpage_dict = frontpage_instance.to_dict()
# create an instance of Frontpage from a dict
frontpage_from_dict = Frontpage.from_dict(frontpage_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


