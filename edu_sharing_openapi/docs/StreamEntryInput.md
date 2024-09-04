# StreamEntryInput


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**title** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**nodes** | **List[str]** |  | [optional] 
**properties** | **Dict[str, object]** |  | [optional] 
**priority** | **int** |  | [optional] 

## Example

```python
from edu_sharing_client.models.stream_entry_input import StreamEntryInput

# TODO update the JSON string below
json = "{}"
# create an instance of StreamEntryInput from a JSON string
stream_entry_input_instance = StreamEntryInput.from_json(json)
# print the JSON string representation of the object
print(StreamEntryInput.to_json())

# convert the object into a dict
stream_entry_input_dict = stream_entry_input_instance.to_dict()
# create an instance of StreamEntryInput from a dict
stream_entry_input_from_dict = StreamEntryInput.from_dict(stream_entry_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


