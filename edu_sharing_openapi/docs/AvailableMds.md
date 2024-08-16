# AvailableMds


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**repository** | **str** |  | [optional] 
**mds** | **List[str]** |  | [optional] 

## Example

```python
from edu_sharing_client.models.available_mds import AvailableMds

# TODO update the JSON string below
json = "{}"
# create an instance of AvailableMds from a JSON string
available_mds_instance = AvailableMds.from_json(json)
# print the JSON string representation of the object
print(AvailableMds.to_json())

# convert the object into a dict
available_mds_dict = available_mds_instance.to_dict()
# create an instance of AvailableMds from a dict
available_mds_from_dict = AvailableMds.from_dict(available_mds_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


