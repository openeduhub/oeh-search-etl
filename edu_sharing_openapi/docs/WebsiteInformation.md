# WebsiteInformation


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**duplicate_nodes** | [**List[Node]**](Node.md) |  | [optional] 
**title** | **str** |  | [optional] 
**page** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**license** | **str** |  | [optional] 
**keywords** | **List[str]** |  | [optional] 

## Example

```python
from edu_sharing_client.models.website_information import WebsiteInformation

# TODO update the JSON string below
json = "{}"
# create an instance of WebsiteInformation from a JSON string
website_information_instance = WebsiteInformation.from_json(json)
# print the JSON string representation of the object
print(WebsiteInformation.to_json())

# convert the object into a dict
website_information_dict = website_information_instance.to_dict()
# create an instance of WebsiteInformation from a dict
website_information_from_dict = WebsiteInformation.from_dict(website_information_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


