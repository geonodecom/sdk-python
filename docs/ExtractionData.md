# ExtractionData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**html** | **str** |  | [optional]
**markdown** | **str** |  | [optional]

## Example

```python
from geonode_scraper_sdk.models.extraction_data import ExtractionData

# TODO update the JSON string below
json = "{}"
# create an instance of ExtractionData from a JSON string
extraction_data_instance = ExtractionData.from_json(json)
# print the JSON string representation of the object
print(ExtractionData.to_json())

# convert the object into a dict
extraction_data_dict = extraction_data_instance.to_dict()
# create an instance of ExtractionData from a dict
extraction_data_from_dict = ExtractionData.from_dict(extraction_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
