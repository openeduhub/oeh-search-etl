# TrackingAuthority


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**hash** | **str** |  | [optional] 
**organization** | [**List[Organization]**](Organization.md) |  | [optional] 
**mediacenter** | [**List[Group]**](Group.md) |  | [optional] 

## Example

```python
from edu_sharing_client.models.tracking_authority import TrackingAuthority

# TODO update the JSON string below
json = "{}"
# create an instance of TrackingAuthority from a JSON string
tracking_authority_instance = TrackingAuthority.from_json(json)
# print the JSON string representation of the object
print(TrackingAuthority.to_json())

# convert the object into a dict
tracking_authority_dict = tracking_authority_instance.to_dict()
# create an instance of TrackingAuthority from a dict
tracking_authority_from_dict = TrackingAuthority.from_dict(tracking_authority_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


