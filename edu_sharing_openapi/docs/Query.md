# Query


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**condition** | [**Condition**](Condition.md) |  | [optional] 
**query** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.query import Query

# TODO update the JSON string below
json = "{}"
# create an instance of Query from a JSON string
query_instance = Query.from_json(json)
# print the JSON string representation of the object
print(Query.to_json())

# convert the object into a dict
query_dict = query_instance.to_dict()
# create an instance of Query from a dict
query_from_dict = Query.from_dict(query_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


