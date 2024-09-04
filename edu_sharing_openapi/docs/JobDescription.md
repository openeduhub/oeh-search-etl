# JobDescription


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**params** | [**List[JobFieldDescription]**](JobFieldDescription.md) |  | [optional] 
**tags** | **List[str]** |  | [optional] 

## Example

```python
from edu_sharing_client.models.job_description import JobDescription

# TODO update the JSON string below
json = "{}"
# create an instance of JobDescription from a JSON string
job_description_instance = JobDescription.from_json(json)
# print the JSON string representation of the object
print(JobDescription.to_json())

# convert the object into a dict
job_description_dict = job_description_instance.to_dict()
# create an instance of JobDescription from a dict
job_description_from_dict = JobDescription.from_dict(job_description_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


