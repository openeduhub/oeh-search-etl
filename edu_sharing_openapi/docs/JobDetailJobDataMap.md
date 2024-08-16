# JobDetailJobDataMap


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
from edu_sharing_client.models.job_detail_job_data_map import JobDetailJobDataMap

# TODO update the JSON string below
json = "{}"
# create an instance of JobDetailJobDataMap from a JSON string
job_detail_job_data_map_instance = JobDetailJobDataMap.from_json(json)
# print the JSON string representation of the object
print(JobDetailJobDataMap.to_json())

# convert the object into a dict
job_detail_job_data_map_dict = job_detail_job_data_map_instance.to_dict()
# create an instance of JobDetailJobDataMap from a dict
job_detail_job_data_map_from_dict = JobDetailJobDataMap.from_dict(job_detail_job_data_map_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


