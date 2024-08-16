# MdsList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**columns** | [**List[MdsColumn]**](MdsColumn.md) |  | [optional] 

## Example

```python
from edu_sharing_client.models.mds_list import MdsList

# TODO update the JSON string below
json = "{}"
# create an instance of MdsList from a JSON string
mds_list_instance = MdsList.from_json(json)
# print the JSON string representation of the object
print(MdsList.to_json())

# convert the object into a dict
mds_list_dict = mds_list_instance.to_dict()
# create an instance of MdsList from a dict
mds_list_from_dict = MdsList.from_dict(mds_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


