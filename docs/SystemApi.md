# geonode_scraper_sdk.SystemApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**health_check_health_get**](SystemApi.md#health_check_health_get) | **GET** /health | Health check


# **health_check_health_get**
> HealthResponse health_check_health_get()

Health check

### Example


```python
import geonode_scraper_sdk
from geonode_scraper_sdk.models.health_response import HealthResponse
from geonode_scraper_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = geonode_scraper_sdk.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with geonode_scraper_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = geonode_scraper_sdk.SystemApi(api_client)

    try:
        # Health check
        api_response = api_instance.health_check_health_get()
        print("The response of SystemApi->health_check_health_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SystemApi->health_check_health_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**HealthResponse**](HealthResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Service is healthy |  -  |
**503** | Service unavailable |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
