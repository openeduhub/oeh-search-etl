# Node


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**node_lti_deep_link** | [**NodeLTIDeepLink**](NodeLTIDeepLink.md) |  | [optional] 
**remote** | [**Remote**](Remote.md) |  | [optional] 
**content** | [**Content**](Content.md) |  | [optional] 
**license** | [**License**](License.md) |  | [optional] 
**is_directory** | **bool** |  | [optional] 
**comment_count** | **int** |  | [optional] 
**rating** | [**RatingDetails**](RatingDetails.md) |  | [optional] 
**used_in_collections** | [**List[Node]**](Node.md) |  | [optional] 
**relations** | [**Dict[str, Node]**](Node.md) |  | [optional] 
**contributors** | [**List[Contributor]**](Contributor.md) |  | [optional] 
**ref** | [**NodeRef**](NodeRef.md) |  | 
**parent** | [**NodeRef**](NodeRef.md) |  | [optional] 
**type** | **str** |  | [optional] 
**aspects** | **List[str]** |  | [optional] 
**name** | **str** |  | 
**title** | **str** |  | [optional] 
**metadataset** | **str** |  | [optional] 
**repository_type** | **str** |  | [optional] 
**created_at** | **datetime** |  | 
**created_by** | [**Person**](Person.md) |  | 
**modified_at** | **datetime** |  | [optional] 
**modified_by** | [**Person**](Person.md) |  | [optional] 
**access** | **List[str]** |  | 
**download_url** | **str** |  | 
**properties** | **Dict[str, List[str]]** |  | [optional] 
**mimetype** | **str** |  | [optional] 
**mediatype** | **str** |  | [optional] 
**size** | **str** |  | [optional] 
**preview** | [**Preview**](Preview.md) |  | [optional] 
**icon_url** | **str** |  | [optional] 
**collection** | [**Collection**](Collection.md) |  | 
**owner** | [**Person**](Person.md) |  | 
**is_public** | **bool** |  | [optional] 

## Example

```python
from edu_sharing_client.models.node import Node

# TODO update the JSON string below
json = "{}"
# create an instance of Node from a JSON string
node_instance = Node.from_json(json)
# print the JSON string representation of the object
print(Node.to_json())

# convert the object into a dict
node_dict = node_instance.to_dict()
# create an instance of Node from a dict
node_from_dict = Node.from_dict(node_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


