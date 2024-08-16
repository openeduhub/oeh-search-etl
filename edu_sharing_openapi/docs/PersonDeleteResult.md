# PersonDeleteResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**authority_name** | **str** |  | [optional] 
**deleted_name** | **str** |  | [optional] 
**home_folder** | [**Dict[str, Counts]**](Counts.md) |  | [optional] 
**shared_folders** | [**Dict[str, Counts]**](Counts.md) |  | [optional] 
**collections** | [**CollectionCounts**](CollectionCounts.md) |  | [optional] 
**comments** | **int** |  | [optional] 
**ratings** | **int** |  | [optional] 
**collection_feedback** | **int** |  | [optional] 
**stream** | **int** |  | [optional] 

## Example

```python
from edu_sharing_client.models.person_delete_result import PersonDeleteResult

# TODO update the JSON string below
json = "{}"
# create an instance of PersonDeleteResult from a JSON string
person_delete_result_instance = PersonDeleteResult.from_json(json)
# print the JSON string representation of the object
print(PersonDeleteResult.to_json())

# convert the object into a dict
person_delete_result_dict = person_delete_result_instance.to_dict()
# create an instance of PersonDeleteResult from a dict
person_delete_result_from_dict = PersonDeleteResult.from_dict(person_delete_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


