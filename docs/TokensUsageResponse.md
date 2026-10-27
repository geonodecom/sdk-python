# TokensUsageResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_date** | **datetime** | Date of the tokens usage |
**tokens_used** | **int** | Number of tokens used on this date |

## Example

```python
from geonode_scraper_sdk.models.tokens_usage_response import TokensUsageResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TokensUsageResponse from a JSON string
tokens_usage_response_instance = TokensUsageResponse.from_json(json)
# print the JSON string representation of the object
print(TokensUsageResponse.to_json())

# convert the object into a dict
tokens_usage_response_dict = tokens_usage_response_instance.to_dict()
# create an instance of TokensUsageResponse from a dict
tokens_usage_response_from_dict = TokensUsageResponse.from_dict(tokens_usage_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
