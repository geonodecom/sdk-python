# ExtractAsyncResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**job_id** | **str** | Job ID for polling status |
**status** | [**JobStatus**](JobStatus.md) | Initial job status |
**status_url** | **str** | URL to poll for job status |
**estimated_tokens** | **int** | Estimated tokens reserved for this job |

## Example

```python
from geonode_scraper_sdk.models.extract_async_response import ExtractAsyncResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ExtractAsyncResponse from a JSON string
extract_async_response_instance = ExtractAsyncResponse.from_json(json)
# print the JSON string representation of the object
print(ExtractAsyncResponse.to_json())

# convert the object into a dict
extract_async_response_dict = extract_async_response_instance.to_dict()
# create an instance of ExtractAsyncResponse from a dict
extract_async_response_from_dict = ExtractAsyncResponse.from_dict(extract_async_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
