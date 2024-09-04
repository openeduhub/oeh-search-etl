# RatingEventDTO


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**node** | [**NodeDataDTO**](NodeDataDTO.md) |  | [optional] 
**new_rating** | **float** |  | [optional] 
**rating_sum** | **float** |  | [optional] 
**rating_count** | **int** |  | [optional] 

## Example

```python
from edu_sharing_client.models.rating_event_dto import RatingEventDTO

# TODO update the JSON string below
json = "{}"
# create an instance of RatingEventDTO from a JSON string
rating_event_dto_instance = RatingEventDTO.from_json(json)
# print the JSON string representation of the object
print(RatingEventDTO.to_json())

# convert the object into a dict
rating_event_dto_dict = rating_event_dto_instance.to_dict()
# create an instance of RatingEventDTO from a dict
rating_event_dto_from_dict = RatingEventDTO.from_dict(rating_event_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


