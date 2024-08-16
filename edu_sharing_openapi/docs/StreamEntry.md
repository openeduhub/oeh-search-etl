# StreamEntry


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**nodes** | [**List[Node]**](Node.md) |  | [optional] 
**properties** | **Dict[str, object]** |  | [optional] 
**priority** | **int** |  | [optional] 
**author** | [**UserSimple**](UserSimple.md) |  | [optional] 
**created** | **int** |  | [optional] 
**modified** | **int** |  | [optional] 

## Example

```python
from edu_sharing_client.models.stream_entry import StreamEntry

# TODO update the JSON string below
json = "{}"
# create an instance of StreamEntry from a JSON string
stream_entry_instance = StreamEntry.from_json(json)
# print the JSON string representation of the object
print(StreamEntry.to_json())

# convert the object into a dict
stream_entry_dict = stream_entry_instance.to_dict()
# create an instance of StreamEntry from a dict
stream_entry_from_dict = StreamEntry.from_dict(stream_entry_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


