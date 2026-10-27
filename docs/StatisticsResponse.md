# StatisticsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**extraction_count** | **int** | Total number of extractions in the period |
**previous_period_extraction_count** | **int** | Total extractions in the previous period |
**success_rate** | **float** | Extraction success rate (0.0 to 1.0) |
**average_extraction_duration** | **int** | Average extraction duration in milliseconds |
**period_tokens_used** | **int** | Total tokens used in the period |
**requests** | [**List[RequestCountResponse]**](RequestCountResponse.md) | Daily request counts | [optional]
**tokens_used** | [**List[TokensUsageResponse]**](TokensUsageResponse.md) | Daily tokens usage | [optional]

## Example

```python
from geonode_scraper_sdk.models.statistics_response import StatisticsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of StatisticsResponse from a JSON string
statistics_response_instance = StatisticsResponse.from_json(json)
# print the JSON string representation of the object
print(StatisticsResponse.to_json())

# convert the object into a dict
statistics_response_dict = statistics_response_instance.to_dict()
# create an instance of StatisticsResponse from a dict
statistics_response_from_dict = StatisticsResponse.from_dict(statistics_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
