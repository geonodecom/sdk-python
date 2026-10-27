# ExtractSyncResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**ExtractionData**](ExtractionData.md) | Extracted content in requested formats |
**metadata** | [**ExtractionMetadata**](ExtractionMetadata.md) | Execution metadata |
**tokens_charged** | **int** | Number of tokens charged for this extraction |

## Example

```python
from geonode_scraper_sdk.models.extract_sync_response import ExtractSyncResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ExtractSyncResponse from a JSON string
extract_sync_response_instance = ExtractSyncResponse.from_json(json)
# print the JSON string representation of the object
print(ExtractSyncResponse.to_json())

# convert the object into a dict
extract_sync_response_dict = extract_sync_response_instance.to_dict()
# create an instance of ExtractSyncResponse from a dict
extract_sync_response_from_dict = ExtractSyncResponse.from_dict(extract_sync_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
