# JobEntry


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**Job**](Job.md) |  | 

## Example

```python
from edu_sharing_client.models.job_entry import JobEntry

# TODO update the JSON string below
json = "{}"
# create an instance of JobEntry from a JSON string
job_entry_instance = JobEntry.from_json(json)
# print the JSON string representation of the object
print(JobEntry.to_json())

# convert the object into a dict
job_entry_dict = job_entry_instance.to_dict()
# create an instance of JobEntry from a dict
job_entry_from_dict = JobEntry.from_dict(job_entry_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


