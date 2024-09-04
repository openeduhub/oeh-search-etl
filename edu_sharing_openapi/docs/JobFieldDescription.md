# JobFieldDescription


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**file** | **bool** |  | [optional] 
**sample_value** | **str** |  | [optional] 
**is_array** | **bool** |  | [optional] 
**array** | **bool** |  | [optional] 

## Example

```python
from edu_sharing_client.models.job_field_description import JobFieldDescription

# TODO update the JSON string below
json = "{}"
# create an instance of JobFieldDescription from a JSON string
job_field_description_instance = JobFieldDescription.from_json(json)
# print the JSON string representation of the object
print(JobFieldDescription.to_json())

# convert the object into a dict
job_field_description_dict = job_field_description_instance.to_dict()
# create an instance of JobFieldDescription from a dict
job_field_description_from_dict = JobFieldDescription.from_dict(job_field_description_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


