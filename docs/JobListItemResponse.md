# JobListItemResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**job_id** | **UUID** | Job ID |
**status** | [**JobStatus**](JobStatus.md) | Current job status |
**url** | **str** | URL to extract content from |
**created_at** | **datetime** | Date when job was created |
**execution_time** | **int** |  | [optional]
**output** | [**List[OutputFormat]**](OutputFormat.md) | Output formats requested | [optional]

## Example

```python
from geonode_scraper_sdk.models.job_list_item_response import JobListItemResponse

# TODO update the JSON string below
json = "{}"
# create an instance of JobListItemResponse from a JSON string
job_list_item_response_instance = JobListItemResponse.from_json(json)
# print the JSON string representation of the object
print(JobListItemResponse.to_json())

# convert the object into a dict
job_list_item_response_dict = job_list_item_response_instance.to_dict()
# create an instance of JobListItemResponse from a dict
job_list_item_response_from_dict = JobListItemResponse.from_dict(job_list_item_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
