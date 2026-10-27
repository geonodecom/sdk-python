# ExtractionErrorResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**error** | [**ExtractionError**](ExtractionError.md) | Execution metadata |
**tokens_charged** | **int** | Number of tokens charged for this extraction |

## Example

```python
from geonode_scraper_sdk.models.extraction_error_response import ExtractionErrorResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ExtractionErrorResponse from a JSON string
extraction_error_response_instance = ExtractionErrorResponse.from_json(json)
# print the JSON string representation of the object
print(ExtractionErrorResponse.to_json())

# convert the object into a dict
extraction_error_response_dict = extraction_error_response_instance.to_dict()
# create an instance of ExtractionErrorResponse from a dict
extraction_error_response_from_dict = ExtractionErrorResponse.from_dict(extraction_error_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
