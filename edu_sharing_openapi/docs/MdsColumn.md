# MdsColumn


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**format** | **str** |  | [optional] 
**show_default** | **bool** |  | [optional] 

## Example

```python
from edu_sharing_client.models.mds_column import MdsColumn

# TODO update the JSON string below
json = "{}"
# create an instance of MdsColumn from a JSON string
mds_column_instance = MdsColumn.from_json(json)
# print the JSON string representation of the object
print(MdsColumn.to_json())

# convert the object into a dict
mds_column_dict = mds_column_instance.to_dict()
# create an instance of MdsColumn from a dict
mds_column_from_dict = MdsColumn.from_dict(mds_column_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


