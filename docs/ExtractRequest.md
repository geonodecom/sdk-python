# ExtractRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | **str** | URL to extract content from |
**formats** | [**List[OutputFormat]**](OutputFormat.md) | Output formats to return | [optional] [default to [html]]
**render_js** | **bool** | If true, uses a headless browser to render the page (slower, more expensive). | [optional] [default to False]
**processing_mode** | [**ProcessingMode**](ProcessingMode.md) | Processing mode: sync (block until done) or async (starts job and return job ID) | [optional]
**proxy** | [**ProxySettings**](ProxySettings.md) | Proxy configuration | [optional]
**headers** | **Dict[str, str]** |  | [optional]

## Example

```python
from geonode_scraper_sdk.models.extract_request import ExtractRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ExtractRequest from a JSON string
extract_request_instance = ExtractRequest.from_json(json)
# print the JSON string representation of the object
print(ExtractRequest.to_json())

# convert the object into a dict
extract_request_dict = extract_request_instance.to_dict()
# create an instance of ExtractRequest from a dict
extract_request_from_dict = ExtractRequest.from_dict(extract_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
