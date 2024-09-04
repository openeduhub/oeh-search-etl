# Mds


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**create** | [**Create**](Create.md) |  | [optional] 
**widgets** | [**List[MdsWidget]**](MdsWidget.md) |  | 
**views** | [**List[MdsView]**](MdsView.md) |  | 
**groups** | [**List[MdsGroup]**](MdsGroup.md) |  | 
**lists** | [**List[MdsList]**](MdsList.md) |  | 
**sorts** | [**List[MdsSort]**](MdsSort.md) |  | 

## Example

```python
from edu_sharing_client.models.mds import Mds

# TODO update the JSON string below
json = "{}"
# create an instance of Mds from a JSON string
mds_instance = Mds.from_json(json)
# print the JSON string representation of the object
print(Mds.to_json())

# convert the object into a dict
mds_dict = mds_instance.to_dict()
# create an instance of Mds from a dict
mds_from_dict = Mds.from_dict(mds_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


