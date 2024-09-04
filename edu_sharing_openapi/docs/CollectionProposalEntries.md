# CollectionProposalEntries


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**Pagination**](Pagination.md) |  | [optional] 
**collections** | [**List[NodeCollectionProposalCount]**](NodeCollectionProposalCount.md) |  | 

## Example

```python
from edu_sharing_client.models.collection_proposal_entries import CollectionProposalEntries

# TODO update the JSON string below
json = "{}"
# create an instance of CollectionProposalEntries from a JSON string
collection_proposal_entries_instance = CollectionProposalEntries.from_json(json)
# print the JSON string representation of the object
print(CollectionProposalEntries.to_json())

# convert the object into a dict
collection_proposal_entries_dict = collection_proposal_entries_instance.to_dict()
# create an instance of CollectionProposalEntries from a dict
collection_proposal_entries_from_dict = CollectionProposalEntries.from_dict(collection_proposal_entries_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


