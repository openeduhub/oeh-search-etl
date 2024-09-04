# RatingHistory


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**overall** | [**RatingData**](RatingData.md) |  | [optional] 
**affiliation** | [**Dict[str, RatingData]**](RatingData.md) |  | [optional] 
**timestamp** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.rating_history import RatingHistory

# TODO update the JSON string below
json = "{}"
# create an instance of RatingHistory from a JSON string
rating_history_instance = RatingHistory.from_json(json)
# print the JSON string representation of the object
print(RatingHistory.to_json())

# convert the object into a dict
rating_history_dict = rating_history_instance.to_dict()
# create an instance of RatingHistory from a dict
rating_history_from_dict = RatingHistory.from_dict(rating_history_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


