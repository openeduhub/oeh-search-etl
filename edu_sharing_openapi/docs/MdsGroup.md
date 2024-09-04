# MdsGroup


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**rendering** | **str** |  | [optional] 
**id** | **str** |  | [optional] 
**views** | **List[str]** |  | [optional] 

## Example

```python
from edu_sharing_client.models.mds_group import MdsGroup

# TODO update the JSON string below
json = "{}"
# create an instance of MdsGroup from a JSON string
mds_group_instance = MdsGroup.from_json(json)
# print the JSON string representation of the object
print(MdsGroup.to_json())

# convert the object into a dict
mds_group_dict = mds_group_instance.to_dict()
# create an instance of MdsGroup from a dict
mds_group_from_dict = MdsGroup.from_dict(mds_group_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


