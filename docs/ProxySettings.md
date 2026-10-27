# ProxySettings


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**country** | **str** |  | [optional]
**type** | [**ProxyType**](ProxyType.md) | Type of proxy to use (datacenter or residential) | [optional]

## Example

```python
from geonode_scraper_sdk.models.proxy_settings import ProxySettings

# TODO update the JSON string below
json = "{}"
# create an instance of ProxySettings from a JSON string
proxy_settings_instance = ProxySettings.from_json(json)
# print the JSON string representation of the object
print(ProxySettings.to_json())

# convert the object into a dict
proxy_settings_dict = proxy_settings_instance.to_dict()
# create an instance of ProxySettings from a dict
proxy_settings_from_dict = ProxySettings.from_dict(proxy_settings_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
