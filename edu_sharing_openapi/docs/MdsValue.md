# MdsValue


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**caption** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**parent** | **str** |  | [optional] 
**url** | **str** |  | [optional] 
**alternative_ids** | **List[str]** |  | [optional] 

## Example

```python
from edu_sharing_client.models.mds_value import MdsValue

# TODO update the JSON string below
json = "{}"
# create an instance of MdsValue from a JSON string
mds_value_instance = MdsValue.from_json(json)
# print the JSON string representation of the object
print(MdsValue.to_json())

# convert the object into a dict
mds_value_dict = mds_value_instance.to_dict()
# create an instance of MdsValue from a dict
mds_value_from_dict = MdsValue.from_dict(mds_value_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


