# Geo


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**longitude** | **float** |  | [optional] 
**latitude** | **float** |  | [optional] 
**address_country** | **str** |  | [optional] 

## Example

```python
from edu_sharing_client.models.geo import Geo

# TODO update the JSON string below
json = "{}"
# create an instance of Geo from a JSON string
geo_instance = Geo.from_json(json)
# print the JSON string representation of the object
print(Geo.to_json())

# convert the object into a dict
geo_dict = geo_instance.to_dict()
# create an instance of Geo from a dict
geo_from_dict = Geo.from_dict(geo_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


