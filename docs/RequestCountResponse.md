# RequestCountResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_date** | **datetime** | Date of the request count |
**success_request_count** | **int** | Number of successful requests on this date |
**failed_request_count** | **int** | Number of failed requests on this date |

## Example

```python
from geonode_scraper_sdk.models.request_count_response import RequestCountResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RequestCountResponse from a JSON string
request_count_response_instance = RequestCountResponse.from_json(json)
# print the JSON string representation of the object
print(RequestCountResponse.to_json())

# convert the object into a dict
request_count_response_dict = request_count_response_instance.to_dict()
# create an instance of RequestCountResponse from a dict
request_count_response_from_dict = RequestCountResponse.from_dict(request_count_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
