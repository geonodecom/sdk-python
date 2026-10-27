# geonode_scraper_sdk.StatisticsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_statistics_v1_statistics_get**](StatisticsApi.md#get_statistics_v1_statistics_get) | **GET** /v1/statistics | Get extraction statistics


# **get_statistics_v1_statistics_get**
> StatisticsResponse get_statistics_v1_statistics_get(start_date=start_date, end_date=end_date)

Get extraction statistics

Retrieve aggregated extraction statistics for a given date range

### Example

* Api Key Authentication (APIKeyHeader):

```python
import geonode_scraper_sdk
from geonode_scraper_sdk.models.statistics_response import StatisticsResponse
from geonode_scraper_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = geonode_scraper_sdk.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: APIKeyHeader
configuration.api_key['APIKeyHeader'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['APIKeyHeader'] = 'Bearer'

# Enter a context with an instance of the API client
with geonode_scraper_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = geonode_scraper_sdk.StatisticsApi(api_client)
    start_date = '2013-10-20T19:20:30+01:00' # datetime | Filter by start date (defaults to 30 days ago) (optional)
    end_date = '2013-10-20T19:20:30+01:00' # datetime | Filter by end date (defaults to now) (optional)

    try:
        # Get extraction statistics
        api_response = api_instance.get_statistics_v1_statistics_get(start_date=start_date, end_date=end_date)
        print("The response of StatisticsApi->get_statistics_v1_statistics_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StatisticsApi->get_statistics_v1_statistics_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **start_date** | **datetime**| Filter by start date (defaults to 30 days ago) | [optional]
 **end_date** | **datetime**| Filter by end date (defaults to now) | [optional]

### Return type

[**StatisticsResponse**](StatisticsResponse.md)

### Authorization

[APIKeyHeader](../README.md#APIKeyHeader)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Statistics retrieved successfully |  -  |
**401** | Unauthorized |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
