# JobKey


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**group** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.job_key import JobKey

# TODO update the JSON string below
json = "{}"
# create an instance of JobKey from a JSON string
job_key_instance = JobKey.from_json(json)
# print the JSON string representation of the object
print(JobKey.to_json())

# convert the object into a dict
job_key_dict = job_key_instance.to_dict()
# create an instance of JobKey from a dict
job_key_from_dict = JobKey.from_dict(job_key_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


