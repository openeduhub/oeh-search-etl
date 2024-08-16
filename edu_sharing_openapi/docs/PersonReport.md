# PersonReport


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**options** | [**PersonDeleteOptions**](PersonDeleteOptions.md) |  | [optional] 
**results** | [**List[PersonDeleteResult]**](PersonDeleteResult.md) |  | [optional] 

## Example

```python
from edu_sharing_client.models.person_report import PersonReport

# TODO update the JSON string below
json = "{}"
# create an instance of PersonReport from a JSON string
person_report_instance = PersonReport.from_json(json)
# print the JSON string representation of the object
print(PersonReport.to_json())

# convert the object into a dict
person_report_dict = person_report_instance.to_dict()
# create an instance of PersonReport from a dict
person_report_from_dict = PersonReport.from_dict(person_report_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


