# RestoreResults


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**results** | [**List[RestoreResult]**](RestoreResult.md) |  | 

## Example

```python
from edu_sharing_client.models.restore_results import RestoreResults

# TODO update the JSON string below
json = "{}"
# create an instance of RestoreResults from a JSON string
restore_results_instance = RestoreResults.from_json(json)
# print the JSON string representation of the object
print(RestoreResults.to_json())

# convert the object into a dict
restore_results_dict = restore_results_instance.to_dict()
# create an instance of RestoreResults from a dict
restore_results_from_dict = RestoreResults.from_dict(restore_results_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


