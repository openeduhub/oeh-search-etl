# JobDataMap


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dirty** | **bool** |  | [optional] 
**allows_transient_data** | **bool** |  | [optional] 
**keys** | **List[str]** |  | [optional] 
**wrapped_map** | **Dict[str, object]** |  | [optional] 
**empty** | **bool** |  | [optional] 

## Example

```python
from edu_sharing_client.models.job_data_map import JobDataMap

# TODO update the JSON string below
json = "{}"
# create an instance of JobDataMap from a JSON string
job_data_map_instance = JobDataMap.from_json(json)
# print the JSON string representation of the object
print(JobDataMap.to_json())

# convert the object into a dict
job_data_map_dict = job_data_map_instance.to_dict()
# create an instance of JobDataMap from a dict
job_data_map_from_dict = JobDataMap.from_dict(job_data_map_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


