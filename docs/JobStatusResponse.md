# JobStatusResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**job_id** | **str** | Job ID |
**status** | [**JobStatus**](JobStatus.md) | Current job status |
**created_at** | **datetime** | When job was created |
**completed_at** | **datetime** |  | [optional]
**data** | [**ExtractionData**](ExtractionData.md) |  | [optional]
**metadata** | [**ExtractionMetadata**](ExtractionMetadata.md) |  | [optional]
**error** | [**ExtractionError**](ExtractionError.md) |  | [optional]
**tokens_charged** | **int** |  | [optional]

## Example

```python
from geonode_scraper_sdk.models.job_status_response import JobStatusResponse

# TODO update the JSON string below
json = "{}"
# create an instance of JobStatusResponse from a JSON string
job_status_response_instance = JobStatusResponse.from_json(json)
# print the JSON string representation of the object
print(JobStatusResponse.to_json())

# convert the object into a dict
job_status_response_dict = job_status_response_instance.to_dict()
# create an instance of JobStatusResponse from a dict
job_status_response_from_dict = JobStatusResponse.from_dict(job_status_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
