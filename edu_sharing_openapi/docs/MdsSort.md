# MdsSort


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**columns** | [**List[MdsSortColumn]**](MdsSortColumn.md) |  | [optional] 
**default** | [**MdsSortDefault**](MdsSortDefault.md) |  | [optional] 

## Example

```python
from edu_sharing_client.models.mds_sort import MdsSort

# TODO update the JSON string below
json = "{}"
# create an instance of MdsSort from a JSON string
mds_sort_instance = MdsSort.from_json(json)
# print the JSON string representation of the object
print(MdsSort.to_json())

# convert the object into a dict
mds_sort_dict = mds_sort_instance.to_dict()
# create an instance of MdsSort from a dict
mds_sort_from_dict = MdsSort.from_dict(mds_sort_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


