# ExtractionMetadata


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | **str** | URL that was extracted |
**render_js** | **bool** | Whether a headless browser was used |
**http_status** | **int** |  | [optional]
**duration_ms** | **int** |  | [optional]
**formats** | [**List[OutputFormat]**](OutputFormat.md) | Output formats to return |
**proxy** | [**ProxySettings**](ProxySettings.md) |  | [optional]
**processing_mode** | [**ProcessingMode**](ProcessingMode.md) | Processing mode: sync (block until done) or async (starts job and return job ID) |
**headers** | **Dict[str, str]** |  | [optional]
**wait_config** | [**WaitConfig**](WaitConfig.md) |  | [optional]

## Example

```python
from geonode_scraper_sdk.models.extraction_metadata import ExtractionMetadata

# TODO update the JSON string below
json = "{}"
# create an instance of ExtractionMetadata from a JSON string
extraction_metadata_instance = ExtractionMetadata.from_json(json)
# print the JSON string representation of the object
print(ExtractionMetadata.to_json())

# convert the object into a dict
extraction_metadata_dict = extraction_metadata_instance.to_dict()
# create an instance of ExtractionMetadata from a dict
extraction_metadata_from_dict = ExtractionMetadata.from_dict(extraction_metadata_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
