# MdsView


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**caption** | **str** |  | [optional] 
**icon** | **str** |  | [optional] 
**html** | **str** |  | [optional] 
**rel** | **str** |  | [optional] 
**hide_if_empty** | **bool** |  | [optional] 
**is_extended** | **bool** |  | [optional] 

## Example

```python
from edu_sharing_client.models.mds_view import MdsView

# TODO update the JSON string below
json = "{}"
# create an instance of MdsView from a JSON string
mds_view_instance = MdsView.from_json(json)
# print the JSON string representation of the object
print(MdsView.to_json())

# convert the object into a dict
mds_view_dict = mds_view_instance.to_dict()
# create an instance of MdsView from a dict
mds_view_from_dict = MdsView.from_dict(mds_view_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


