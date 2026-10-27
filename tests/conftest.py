import json
from datetime import datetime, timezone
from unittest.mock import MagicMock
from urllib.parse import parse_qs, urlsplit

import pytest

import geonode_scraper_sdk
from geonode_scraper_sdk.rest import ApiException  # noqa: F401


@pytest.fixture
def mock_configuration():
    """Fixture providing a basic valid runtime configuration for the client."""
    config = geonode_scraper_sdk.Configuration(host="http://api.mock.local")
    config.api_key["ApiKeyAuth"] = "test-mock-api-key"
    return config


@pytest.fixture
def mock_api_client(mock_configuration):
    """Fixture providing a configured ApiClient instance."""
    with geonode_scraper_sdk.ApiClient(mock_configuration) as api_client:
        yield api_client


@pytest.fixture
def valid_extraction_data():
    from geonode_scraper_sdk.models.extraction_data import ExtractionData

    return ExtractionData(
        html="<html><body>Example</body></html>",
        markdown="# Example",
    )


@pytest.fixture
def valid_extraction_metadata():
    from geonode_scraper_sdk.models.extraction_metadata import ExtractionMetadata
    from geonode_scraper_sdk.models.output_format import OutputFormat
    from geonode_scraper_sdk.models.processing_mode import ProcessingMode

    return ExtractionMetadata(
        url="https://example.com",
        render_js=False,
        formats=[OutputFormat.HTML],
        processing_mode=ProcessingMode.SYNC,
    )


@pytest.fixture
def valid_sync_response(valid_extraction_data, valid_extraction_metadata):
    from geonode_scraper_sdk.models.extract_sync_response import ExtractSyncResponse

    return ExtractSyncResponse(
        data=valid_extraction_data,
        metadata=valid_extraction_metadata,
        tokens_charged=10,
    )


@pytest.fixture
def valid_async_response():
    from geonode_scraper_sdk.models.extract_async_response import ExtractAsyncResponse
    from geonode_scraper_sdk.models.job_status import JobStatus

    return ExtractAsyncResponse(
        job_id="test-job-uuid",
        status=JobStatus.QUEUED,
        status_url="http://api.mock.local/v1/extract/test-job-uuid",
        estimated_tokens=50,
    )


@pytest.fixture
def valid_job_status_response(valid_extraction_data, valid_extraction_metadata):
    from geonode_scraper_sdk.models.job_status import JobStatus
    from geonode_scraper_sdk.models.job_status_response import JobStatusResponse

    return JobStatusResponse(
        job_id="test-job-uuid",
        status=JobStatus.COMPLETED,
        created_at=datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        completed_at=datetime(2026, 1, 1, 0, 0, 5, tzinfo=timezone.utc),
        data=valid_extraction_data,
        metadata=valid_extraction_metadata,
        tokens_charged=10,
    )


@pytest.fixture
def valid_job_collection_response():
    import uuid

    from geonode_scraper_sdk.models.job_collection_response import JobCollectionResponse
    from geonode_scraper_sdk.models.job_list_item_response import JobListItemResponse
    from geonode_scraper_sdk.models.job_status import JobStatus

    return JobCollectionResponse(
        jobs=[
            JobListItemResponse(
                job_id=uuid.UUID("00000000-0000-0000-0000-000000000001"),
                status=JobStatus.COMPLETED,
                url="https://example.com",
                created_at=datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
            )
        ],
        page=1,
        page_size=100,
        page_count=1,
    )


@pytest.fixture
def error_401_json():
    return {"code": "UNAUTHORIZED", "message": "Invalid API key", "retryable": False}


@pytest.fixture
def error_400_json():
    return {
        "code": "BAD_REQUEST",
        "message": "Invalid extraction request",
        "correlation_id": "req-400",
        "retryable": False,
    }


@pytest.fixture
def error_402_json():
    return {
        "code": "PAYMENT_REQUIRED",
        "message": "Insufficient credits",
        "correlation_id": "req-402",
        "retryable": False,
    }


@pytest.fixture
def error_429_json():
    return {
        "code": "RATE_LIMITED",
        "message": "Too many requests",
        "correlation_id": "req-429",
        "retryable": True,
    }


@pytest.fixture
def error_404_json():
    return {"code": "NOT_FOUND", "message": "Job not found", "retryable": False}


@pytest.fixture
def error_500_json():
    return {
        "code": "INTERNAL_ERROR",
        "message": "Unexpected server failure",
        "correlation_id": "req-500",
        "retryable": True,
    }


@pytest.fixture
def error_503_json():
    return {
        "code": "SERVICE_UNAVAILABLE",
        "message": "Service temporarily unavailable",
        "correlation_id": "req-503",
        "retryable": True,
    }


@pytest.fixture
def extraction_error_422_json():
    return {
        "error": {
            "code": "TIMEOUT",
            "message": "Target site timed out",
            "retryable": True,
            "details": {"attempt": "3"},
        },
        "tokens_charged": 7,
    }


@pytest.fixture
def query_validation_error_json():
    return {
        "detail": [
            {
                "loc": ["query", "page"],
                "msg": "Input should be greater than or equal to 1",
                "type": "greater_than_equal",
            }
        ]
    }


@pytest.fixture
def path_validation_error_json():
    return {
        "detail": [
            {
                "loc": ["path", "job_id"],
                "msg": "Input should be a valid UUID",
                "type": "uuid_parsing",
            }
        ]
    }


@pytest.fixture
def statistics_validation_error_json():
    return {
        "detail": [
            {
                "loc": ["query", "start_date"],
                "msg": "Input should be a valid datetime",
                "type": "datetime_parsing",
            }
        ]
    }


@pytest.fixture
def valid_extraction_request_payload():
    return {"url": "https://example.com"}


@pytest.fixture
def valid_extraction_success_response():
    return {
        "data": {
            "html": "<html><body>Example</body></html>",
            "markdown": "# Example",
        },
        "metadata": {
            "url": "https://example.com",
            "render_js": False,
            "formats": ["html"],
            "processing_mode": "sync",
        },
        "tokens_charged": 10,
    }


@pytest.fixture
def make_mock_http_response():
    """Factory that creates mock urllib3 responses for use with patch.object."""

    def _factory(status: int, json_body: dict, headers: dict | None = None):
        mock_resp = MagicMock()
        mock_resp.status = status
        mock_resp.reason = "OK"
        mock_resp.data = json.dumps(json_body).encode()
        h = {"content-type": "application/json"}
        if headers:
            h.update(headers)
        mock_resp.headers = h
        return mock_resp

    return _factory


@pytest.fixture
def get_request_details():
    def _get(mock_request):
        args, kwargs = mock_request.call_args
        body = kwargs.get("body")
        if isinstance(body, bytes):
            body = body.decode()
        if isinstance(body, str):
            body = json.loads(body)
        query = parse_qs(urlsplit(args[1]).query, keep_blank_values=True)
        normalized_query = {key: values[0] if len(values) == 1 else values for key, values in query.items()}
        return {
            "method": args[0],
            "url": args[1],
            "query": normalized_query,
            "body": body,
            "headers": kwargs.get("headers", {}),
        }

    return _get


@pytest.fixture
def assert_api_exception_payload():
    def _assert(exc_info, *, status, data_type, code=None, retryable=None):
        exc = exc_info.value
        assert exc.status == status
        assert exc.body is not None
        assert isinstance(exc.data, data_type)
        payload = exc.data.error if hasattr(exc.data, "error") else exc.data
        if code is not None:
            assert payload.code == code
        if retryable is not None:
            assert payload.retryable is retryable

    return _assert
