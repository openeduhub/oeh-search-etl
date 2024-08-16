# MdsWidgetCondition


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | 
**value** | **str** |  | 
**negate** | **bool** |  | 
**dynamic** | **bool** |  | 
**pattern** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.mds_widget_condition import MdsWidgetCondition

# TODO update the JSON string below
json = "{}"
# create an instance of MdsWidgetCondition from a JSON string
mds_widget_condition_instance = MdsWidgetCondition.from_json(json)
# print the JSON string representation of the object
print(MdsWidgetCondition.to_json())

# convert the object into a dict
mds_widget_condition_dict = mds_widget_condition_instance.to_dict()
# create an instance of MdsWidgetCondition from a dict
mds_widget_condition_from_dict = MdsWidgetCondition.from_dict(mds_widget_condition_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


