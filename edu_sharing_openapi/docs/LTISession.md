# LTISession


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**accept_multiple** | **bool** |  | [optional] 
**deeplink_return_url** | **str** |  | [optional] 
**accept_types** | **List[str]** |  | [optional] 
**accept_presentation_document_targets** | **List[str]** |  | [optional] 
**can_confirm** | **bool** |  | [optional] 
**title** | **str** |  | [optional] 
**text** | **str** |  | [optional] 
**custom_content_node** | [**Node**](Node.md) |  | [optional] 

## Example

```python
from edu_sharing_client.models.lti_session import LTISession

# TODO update the JSON string below
json = "{}"
# create an instance of LTISession from a JSON string
lti_session_instance = LTISession.from_json(json)
# print the JSON string representation of the object
print(LTISession.to_json())

# convert the object into a dict
lti_session_dict = lti_session_instance.to_dict()
# create an instance of LTISession from a dict
lti_session_from_dict = LTISession.from_dict(lti_session_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


