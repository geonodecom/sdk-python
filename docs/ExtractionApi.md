# geonode_scraper_sdk.ExtractionApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**extract_v1_extract_post**](ExtractionApi.md#extract_v1_extract_post) | **POST** /v1/extract | Extract content from a URL
[**get_job_result_v1_extract_job_id_get**](ExtractionApi.md#get_job_result_v1_extract_job_id_get) | **GET** /v1/extract/{job_id} | Get extraction job result
[**list_jobs_v1_extract_jobs_get**](ExtractionApi.md#list_jobs_v1_extract_jobs_get) | **GET** /v1/extract/jobs | List extraction jobs


# **extract_v1_extract_post**
> ExtractSyncResponse extract_v1_extract_post(extract_request)

Extract content from a URL

Extract clean markdown or HTML from any URL with sync or async mode support

### Example

* Api Key Authentication (APIKeyHeader):

```python
import geonode_scraper_sdk
from geonode_scraper_sdk.models.extract_request import ExtractRequest
from geonode_scraper_sdk.models.extract_sync_response import ExtractSyncResponse
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
    api_instance = geonode_scraper_sdk.ExtractionApi(api_client)
    extract_request = geonode_scraper_sdk.ExtractRequest() # ExtractRequest |

    try:
        # Extract content from a URL
        api_response = api_instance.extract_v1_extract_post(extract_request)
        print("The response of ExtractionApi->extract_v1_extract_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExtractionApi->extract_v1_extract_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **extract_request** | [**ExtractRequest**](ExtractRequest.md)|  |

### Return type

[**ExtractSyncResponse**](ExtractSyncResponse.md)

### Authorization

[APIKeyHeader](../README.md#APIKeyHeader)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Extraction succeeded (sync mode) |  -  |
**202** | Job accepted (async mode) |  -  |
**400** | Invalid request |  -  |
**401** | Unauthorized |  -  |
**402** | Payment required |  -  |
**429** | Request throttled |  -  |
**422** | Extraction failed |  -  |
**500** | Internal server error |  -  |
**503** | Service temporarily unavailable |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_job_result_v1_extract_job_id_get**
> JobStatusResponse get_job_result_v1_extract_job_id_get(job_id)

Get extraction job result

Poll for job progress and retrieve extraction results (async mode only)

### Example

* Api Key Authentication (APIKeyHeader):

```python
import geonode_scraper_sdk
from geonode_scraper_sdk.models.job_status_response import JobStatusResponse
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
    api_instance = geonode_scraper_sdk.ExtractionApi(api_client)
    job_id = 'job_id_example' # str |

    try:
        # Get extraction job result
        api_response = api_instance.get_job_result_v1_extract_job_id_get(job_id)
        print("The response of ExtractionApi->get_job_result_v1_extract_job_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExtractionApi->get_job_result_v1_extract_job_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **job_id** | **str**|  |

### Return type

[**JobStatusResponse**](JobStatusResponse.md)

### Authorization

[APIKeyHeader](../README.md#APIKeyHeader)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Job result details |  -  |
**401** | Unauthorized |  -  |
**404** | Job not found |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_jobs_v1_extract_jobs_get**
> JobCollectionResponse list_jobs_v1_extract_jobs_get(job_id=job_id, url=url, status=status, output=output, start_date=start_date, end_date=end_date, page=page, page_size=page_size)

List extraction jobs

List and filter extraction jobs by job ID, URL, status, output format, and date range

### Example

* Api Key Authentication (APIKeyHeader):

```python
import geonode_scraper_sdk
from geonode_scraper_sdk.models.job_collection_response import JobCollectionResponse
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
    api_instance = geonode_scraper_sdk.ExtractionApi(api_client)
    job_id = 'job_id_example' # str | Filter by job ID (optional)
    url = 'url_example' # str | Filter by target URL (optional)
    status = geonode_scraper_sdk.JobStatus() # JobStatus | Filter by job status (optional)
    output = geonode_scraper_sdk.OutputFormat() # OutputFormat | Filter by output format (optional)
    start_date = '2013-10-20T19:20:30+01:00' # datetime | Filter jobs created on or after this date (optional)
    end_date = '2013-10-20T19:20:30+01:00' # datetime | Filter jobs created on or before this date (optional)
    page = 1 # int | Page number (must be greater than 0) (optional) (default to 1)
    page_size = 100 # int | Number of results per page (max 100) (optional) (default to 100)

    try:
        # List extraction jobs
        api_response = api_instance.list_jobs_v1_extract_jobs_get(job_id=job_id, url=url, status=status, output=output, start_date=start_date, end_date=end_date, page=page, page_size=page_size)
        print("The response of ExtractionApi->list_jobs_v1_extract_jobs_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExtractionApi->list_jobs_v1_extract_jobs_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **job_id** | **str**| Filter by job ID | [optional]
 **url** | **str**| Filter by target URL | [optional]
 **status** | [**JobStatus**](.md)| Filter by job status | [optional]
 **output** | [**OutputFormat**](.md)| Filter by output format | [optional]
 **start_date** | **datetime**| Filter jobs created on or after this date | [optional]
 **end_date** | **datetime**| Filter jobs created on or before this date | [optional]
 **page** | **int**| Page number (must be greater than 0) | [optional] [default to 1]
 **page_size** | **int**| Number of results per page (max 100) | [optional] [default to 100]

### Return type

[**JobCollectionResponse**](JobCollectionResponse.md)

### Authorization

[APIKeyHeader](../README.md#APIKeyHeader)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Job list retrieved |  -  |
**401** | Unauthorized |  -  |
**404** | Job not found |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
