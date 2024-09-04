# SubGroupItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**key** | **str** |  | [optional] 
**display_name** | **str** |  | [optional] 
**count** | **int** |  | [optional] 

## Example

```python
from edu_sharing_client.models.sub_group_item import SubGroupItem

# TODO update the JSON string below
json = "{}"
# create an instance of SubGroupItem from a JSON string
sub_group_item_instance = SubGroupItem.from_json(json)
# print the JSON string representation of the object
print(SubGroupItem.to_json())

# convert the object into a dict
sub_group_item_dict = sub_group_item_instance.to_dict()
# create an instance of SubGroupItem from a dict
sub_group_item_from_dict = SubGroupItem.from_dict(sub_group_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


