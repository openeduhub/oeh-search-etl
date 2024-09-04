# MdsEntries


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadatasets** | [**List[MetadataSetInfo]**](MetadataSetInfo.md) |  | 

## Example

```python
from edu_sharing_client.models.mds_entries import MdsEntries

# TODO update the JSON string below
json = "{}"
# create an instance of MdsEntries from a JSON string
mds_entries_instance = MdsEntries.from_json(json)
# print the JSON string representation of the object
print(MdsEntries.to_json())

# convert the object into a dict
mds_entries_dict = mds_entries_instance.to_dict()
# create an instance of MdsEntries from a dict
mds_entries_from_dict = MdsEntries.from_dict(mds_entries_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


