# Tracking


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**counts** | **Dict[str, int]** |  | [optional] 
**var_date** | **str** |  | [optional] 
**fields** | **Dict[str, object]** |  | [optional] 
**groups** | **Dict[str, Dict[str, Dict[str, int]]]** |  | [optional] 
**authority** | [**TrackingAuthority**](TrackingAuthority.md) |  | [optional] 

## Example

```python
from edu_sharing_client.models.tracking import Tracking

# TODO update the JSON string below
json = "{}"
# create an instance of Tracking from a JSON string
tracking_instance = Tracking.from_json(json)
# print the JSON string representation of the object
print(Tracking.to_json())

# convert the object into a dict
tracking_dict = tracking_instance.to_dict()
# create an instance of Tracking from a dict
tracking_from_dict = Tracking.from_dict(tracking_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


