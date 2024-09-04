# Banner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | **str** |  | [optional] 
**href** | **str** |  | [optional] 
**components** | **List[str]** |  | [optional] 

## Example

```python
from edu_sharing_client.models.banner import Banner

# TODO update the JSON string below
json = "{}"
# create an instance of Banner from a JSON string
banner_instance = Banner.from_json(json)
# print the JSON string representation of the object
print(Banner.to_json())

# convert the object into a dict
banner_dict = banner_instance.to_dict()
# create an instance of Banner from a dict
banner_from_dict = Banner.from_dict(banner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


