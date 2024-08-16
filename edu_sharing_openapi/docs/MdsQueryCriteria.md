# MdsQueryCriteria


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_property** | **str** |  | 
**values** | **List[str]** |  | 

## Example

```python
from edu_sharing_client.models.mds_query_criteria import MdsQueryCriteria

# TODO update the JSON string below
json = "{}"
# create an instance of MdsQueryCriteria from a JSON string
mds_query_criteria_instance = MdsQueryCriteria.from_json(json)
# print the JSON string representation of the object
print(MdsQueryCriteria.to_json())

# convert the object into a dict
mds_query_criteria_dict = mds_query_criteria_instance.to_dict()
# create an instance of MdsQueryCriteria from a dict
mds_query_criteria_from_dict = MdsQueryCriteria.from_dict(mds_query_criteria_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


