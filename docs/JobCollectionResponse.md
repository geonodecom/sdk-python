# JobCollectionResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**jobs** | [**List[JobListItemResponse]**](JobListItemResponse.md) | List of jobs |
**page** | **int** | Current page number |
**page_size** | **int** | Number of items per page |
**page_count** | **int** | Total number of pages |

## Example

```python
from geonode_scraper_sdk.models.job_collection_response import JobCollectionResponse

# TODO update the JSON string below
json = "{}"
# create an instance of JobCollectionResponse from a JSON string
job_collection_response_instance = JobCollectionResponse.from_json(json)
# print the JSON string representation of the object
print(JobCollectionResponse.to_json())

# convert the object into a dict
job_collection_response_dict = job_collection_response_instance.to_dict()
# create an instance of JobCollectionResponse from a dict
job_collection_response_from_dict = JobCollectionResponse.from_dict(job_collection_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
