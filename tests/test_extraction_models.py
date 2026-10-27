import pytest
from pydantic import ValidationError

from geonode_scraper_sdk.models.extract_request import ExtractRequest
from geonode_scraper_sdk.models.extraction_data import ExtractionData
from geonode_scraper_sdk.models.extraction_metadata import ExtractionMetadata
from geonode_scraper_sdk.models.job_status import JobStatus
from geonode_scraper_sdk.models.output_format import OutputFormat
from geonode_scraper_sdk.models.processing_mode import ProcessingMode
from geonode_scraper_sdk.models.proxy_settings import ProxySettings


def test_extract_request_minimal():
    req = ExtractRequest(url="https://example.com")
    assert req.url == "https://example.com"
    assert req.render_js is False
    assert req.formats == [OutputFormat.HTML]
    assert req.processing_mode == ProcessingMode.SYNC
    assert req.proxy is None
    assert req.headers is None


def test_extract_request_full():
    req = ExtractRequest(
        url="https://example.com",
        formats=[OutputFormat.HTML, OutputFormat.MARKDOWN],
        render_js=True,
        processing_mode=ProcessingMode.ASYNC,
        proxy=ProxySettings(country="US"),
        headers={"X-Custom": "value"},
    )
    assert req.formats == [OutputFormat.HTML, OutputFormat.MARKDOWN]
    assert req.render_js is True
    assert req.processing_mode == ProcessingMode.ASYNC
    assert req.proxy.country == "US"
    assert req.headers == {"X-Custom": "value"}


def test_extract_request_url_empty():
    with pytest.raises(ValidationError):
        ExtractRequest(url="")


def test_extraction_data_all_none():
    data = ExtractionData()
    assert data.html is None
    assert data.markdown is None


def test_extraction_data_with_content():
    data = ExtractionData(
        html="<html><body>Hello</body></html>",
        markdown="# Hello",
    )
    assert data.html == "<html><body>Hello</body></html>"
    assert data.markdown == "# Hello"


def test_extraction_metadata_minimal():
    meta = ExtractionMetadata(
        url="https://example.com",
        render_js=False,
        formats=[OutputFormat.HTML],
        processing_mode=ProcessingMode.SYNC,
    )
    assert meta.url == "https://example.com"
    assert meta.render_js is False
    assert meta.http_status is None
    assert meta.duration_ms is None


def test_extraction_metadata_full():
    meta = ExtractionMetadata(
        url="https://example.com",
        render_js=True,
        formats=[OutputFormat.HTML, OutputFormat.MARKDOWN],
        processing_mode=ProcessingMode.SYNC,
        http_status=200,
        duration_ms=1500,
        proxy=ProxySettings(country="GB"),
        headers={"Accept": "text/html"},
    )
    assert meta.http_status == 200
    assert meta.duration_ms == 1500
    assert meta.proxy.country == "GB"
    assert meta.headers == {"Accept": "text/html"}


def test_extract_sync_response_fields(valid_sync_response):
    assert valid_sync_response.tokens_charged == 10
    assert valid_sync_response.data.html == "<html><body>Example</body></html>"
    assert valid_sync_response.metadata.url == "https://example.com"


def test_extract_sync_response_serialization(valid_sync_response):
    d = valid_sync_response.to_dict()
    assert "data" in d
    assert "metadata" in d
    assert d["tokens_charged"] == 10
    assert d["data"]["html"] == "<html><body>Example</body></html>"


def test_extract_async_response_fields(valid_async_response):
    assert valid_async_response.job_id == "test-job-uuid"
    assert valid_async_response.status == JobStatus.QUEUED
    assert "test-job-uuid" in valid_async_response.status_url
    assert valid_async_response.estimated_tokens == 50


def test_extract_request_from_dict_applies_contract_defaults():
    req = ExtractRequest.from_dict({"url": "https://example.com"})
    assert req.formats == [OutputFormat.HTML]
    assert req.render_js is False
    assert req.processing_mode == ProcessingMode.SYNC


def test_extract_request_json_round_trip():
    req = ExtractRequest(
        url="https://example.com",
        formats=[OutputFormat.HTML, OutputFormat.MARKDOWN],
        render_js=True,
        processing_mode=ProcessingMode.ASYNC,
        proxy=ProxySettings(country="US"),
        headers={"X-Custom": "value"},
    )
    restored = ExtractRequest.from_json(req.to_json())
    assert restored == req


def test_extract_sync_response_round_trip(valid_sync_response):
    restored = valid_sync_response.from_dict(valid_sync_response.to_dict())
    assert restored == valid_sync_response


def test_extract_async_response_round_trip(valid_async_response):
    restored = valid_async_response.from_json(valid_async_response.to_json())
    assert restored == valid_async_response
