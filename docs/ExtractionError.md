# ExtractionError


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | [**ExtractionErrorCode**](ExtractionErrorCode.md) | Error classification code |
**message** | **str** | Human-readable error description |
**retryable** | **bool** | Whether the error is transient and may succeed on retry |
**details** | **Dict[str, str]** |  | [optional]

## Example

```python
from geonode_scraper_sdk.models.extraction_error import ExtractionError

# TODO update the JSON string below
json = "{}"
# create an instance of ExtractionError from a JSON string
extraction_error_instance = ExtractionError.from_json(json)
# print the JSON string representation of the object
print(ExtractionError.to_json())

# convert the object into a dict
extraction_error_dict = extraction_error_instance.to_dict()
# create an instance of ExtractionError from a dict
extraction_error_from_dict = ExtractionError.from_dict(extraction_error_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
