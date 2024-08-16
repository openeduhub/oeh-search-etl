# MdsWidget


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ids** | **Dict[str, str]** |  | [optional] 
**link** | **str** |  | [optional] 
**configuration** | **str** |  | [optional] 
**format** | **str** |  | [optional] 
**allow_valuespace_suggestions** | **bool** |  | [optional] 
**count_defaultvalue_as_filter** | **bool** | When true, a set defaultvalue will still trigger the search to show an active filter. When false (default), the defaultvalue will be shown as if no filter is active | [optional] 
**condition** | [**MdsWidgetCondition**](MdsWidgetCondition.md) |  | [optional] 
**maxlength** | **int** |  | [optional] 
**interaction_type** | **str** |  | [optional] 
**filter_mode** | **str** |  | [optional] 
**expandable** | **str** |  | [optional] 
**subwidgets** | [**List[MdsSubwidget]**](MdsSubwidget.md) |  | [optional] 
**required** | **str** |  | [optional] 
**id** | **str** |  | [optional] 
**caption** | **str** |  | [optional] 
**bottom_caption** | **str** |  | [optional] 
**icon** | **str** |  | [optional] 
**type** | **str** |  | [optional] 
**template** | **str** |  | [optional] 
**has_values** | **bool** |  | [optional] 
**values** | [**List[MdsValue]**](MdsValue.md) |  | [optional] 
**placeholder** | **str** |  | [optional] 
**unit** | **str** |  | [optional] 
**min** | **int** |  | [optional] 
**max** | **int** |  | [optional] 
**default_min** | **int** |  | [optional] 
**default_max** | **int** |  | [optional] 
**step** | **int** |  | [optional] 
**is_required** | **str** |  | [optional] 
**allowempty** | **bool** |  | [optional] 
**defaultvalue** | **str** |  | [optional] 
**is_extended** | **bool** |  | [optional] 
**is_searchable** | **bool** |  | [optional] 
**hide_if_empty** | **bool** |  | [optional] 

## Example

```python
from edu_sharing_client.models.mds_widget import MdsWidget

# TODO update the JSON string below
json = "{}"
# create an instance of MdsWidget from a JSON string
mds_widget_instance = MdsWidget.from_json(json)
# print the JSON string representation of the object
print(MdsWidget.to_json())

# convert the object into a dict
mds_widget_dict = mds_widget_instance.to_dict()
# create an instance of MdsWidget from a dict
mds_widget_from_dict = MdsWidget.from_dict(mds_widget_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


