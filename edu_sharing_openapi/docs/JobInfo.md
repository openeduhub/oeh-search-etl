# JobInfo


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**job_data_map** | [**JobDetailJobDataMap**](JobDetailJobDataMap.md) |  | [optional] 
**job_name** | **str** |  | [optional] 
**job_group** | **str** |  | [optional] 
**start_time** | **int** |  | [optional] 
**finish_time** | **int** |  | [optional] 
**status** | **str** |  | [optional] 
**worst_level** | [**Level**](Level.md) |  | [optional] 
**log** | [**List[LogEntry]**](LogEntry.md) |  | [optional] 
**job_detail** | [**JobDetail**](JobDetail.md) |  | [optional] 

## Example

```python
from edu_sharing_client.models.job_info import JobInfo

# TODO update the JSON string below
json = "{}"
# create an instance of JobInfo from a JSON string
job_info_instance = JobInfo.from_json(json)
# print the JSON string representation of the object
print(JobInfo.to_json())

# convert the object into a dict
job_info_dict = job_info_instance.to_dict()
# create an instance of JobInfo from a dict
job_info_from_dict = JobInfo.from_dict(job_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


