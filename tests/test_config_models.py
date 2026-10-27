import pytest
from pydantic import ValidationError

from geonode_scraper_sdk.models.output_format import OutputFormat
from geonode_scraper_sdk.models.processing_mode import ProcessingMode
from geonode_scraper_sdk.models.proxy_settings import ProxySettings
from geonode_scraper_sdk.models.proxy_type import ProxyType


def test_proxy_type_all_values():
    expected = {"datacenter", "residential", "mix"}
    assert {member.value for member in ProxyType} == expected


def test_proxy_type_is_str_enum():
    assert ProxyType.RESIDENTIAL == "residential"
    assert isinstance(ProxyType.DATACENTER, str)


def test_processing_mode_all_values():
    expected = {"sync", "async"}
    assert {member.value for member in ProcessingMode} == expected


def test_processing_mode_is_str_enum():
    assert ProcessingMode.SYNC == "sync"
    assert ProcessingMode.ASYNC == "async"


def test_output_format_all_values():
    expected = {"markdown", "html"}
    assert {member.value for member in OutputFormat} == expected


def test_output_format_is_str_enum():
    assert OutputFormat.HTML == "html"
    assert OutputFormat.MARKDOWN == "markdown"


def test_proxy_settings_empty():
    proxy = ProxySettings()
    assert proxy.country is None
    assert proxy.type == ProxyType.RESIDENTIAL


def test_proxy_settings_valid_country():
    proxy = ProxySettings(country="US")
    assert proxy.country == "US"


def test_proxy_settings_valid_country_gb():
    proxy = ProxySettings(country="GB")
    assert proxy.country == "GB"


def test_proxy_settings_invalid_country_lowercase():
    with pytest.raises(ValidationError):
        ProxySettings(country="us")


def test_proxy_settings_invalid_country_too_long():
    with pytest.raises(ValidationError):
        ProxySettings(country="USA")


def test_proxy_settings_with_type():
    proxy = ProxySettings(type=ProxyType.DATACENTER)
    assert proxy.type == ProxyType.DATACENTER
    assert proxy.country is None


def test_proxy_settings_full():
    proxy = ProxySettings(country="DE", type=ProxyType.RESIDENTIAL)
    assert proxy.country == "DE"
    assert proxy.type == ProxyType.RESIDENTIAL


def test_proxy_settings_from_dict_applies_default_type():
    proxy = ProxySettings.from_dict({"country": "US"})
    assert proxy.country == "US"
    assert proxy.type == ProxyType.RESIDENTIAL


def test_proxy_settings_round_trip():
    proxy = ProxySettings(country="DE", type=ProxyType.DATACENTER)
    restored = ProxySettings.from_json(proxy.to_json())
    assert restored == proxy
