# JobDetail


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**key** | [**JobKey**](JobKey.md) |  | [optional] 
**job_data_map** | [**JobDetailJobDataMap**](JobDetailJobDataMap.md) |  | [optional] 
**durable** | **bool** |  | [optional] 
**persist_job_data_after_execution** | **bool** |  | [optional] 
**concurrent_exection_disallowed** | **bool** |  | [optional] 
**job_builder** | [**JobBuilder**](JobBuilder.md) |  | [optional] 
**description** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.job_detail import JobDetail

# TODO update the JSON string below
json = "{}"
# create an instance of JobDetail from a JSON string
job_detail_instance = JobDetail.from_json(json)
# print the JSON string representation of the object
print(JobDetail.to_json())

# convert the object into a dict
job_detail_dict = job_detail_instance.to_dict()
# create an instance of JobDetail from a dict
job_detail_from_dict = JobDetail.from_dict(job_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


