# StreamList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**stream** | [**List[StreamEntry]**](StreamEntry.md) |  | [optional] 
**pagination** | [**Pagination**](Pagination.md) |  | [optional] 

## Example

```python
from edu_sharing_client.models.stream_list import StreamList

# TODO update the JSON string below
json = "{}"
# create an instance of StreamList from a JSON string
stream_list_instance = StreamList.from_json(json)
# print the JSON string representation of the object
print(StreamList.to_json())

# convert the object into a dict
stream_list_dict = stream_list_instance.to_dict()
# create an instance of StreamList from a dict
stream_list_from_dict = StreamList.from_dict(stream_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


