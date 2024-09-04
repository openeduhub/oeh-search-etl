# WidgetDataDTO


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**caption** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.widget_data_dto import WidgetDataDTO

# TODO update the JSON string below
json = "{}"
# create an instance of WidgetDataDTO from a JSON string
widget_data_dto_instance = WidgetDataDTO.from_json(json)
# print the JSON string representation of the object
print(WidgetDataDTO.to_json())

# convert the object into a dict
widget_data_dto_dict = widget_data_dto_instance.to_dict()
# create an instance of WidgetDataDTO from a dict
widget_data_dto_from_dict = WidgetDataDTO.from_dict(widget_data_dto_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


