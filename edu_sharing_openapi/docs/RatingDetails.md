# RatingDetails


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**overall** | [**RatingData**](RatingData.md) |  | [optional] 
**affiliation** | [**Dict[str, RatingData]**](RatingData.md) |  | [optional] 
**user** | **float** |  | [optional] 

## Example

```python
from edu_sharing_client.models.rating_details import RatingDetails

# TODO update the JSON string below
json = "{}"
# create an instance of RatingDetails from a JSON string
rating_details_instance = RatingDetails.from_json(json)
# print the JSON string representation of the object
print(RatingDetails.to_json())

# convert the object into a dict
rating_details_dict = rating_details_instance.to_dict()
# create an instance of RatingDetails from a dict
rating_details_from_dict = RatingDetails.from_dict(rating_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


