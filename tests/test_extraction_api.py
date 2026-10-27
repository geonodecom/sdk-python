from datetime import datetime, timezone
from unittest.mock import patch

import pytest

from geonode_scraper_sdk.api.extraction_api import ExtractionApi
from geonode_scraper_sdk.models.error_response import ErrorResponse
from geonode_scraper_sdk.models.extract_request import ExtractRequest
from geonode_scraper_sdk.models.extraction_error_code import ExtractionErrorCode
from geonode_scraper_sdk.models.extraction_error_response import ExtractionErrorResponse
from geonode_scraper_sdk.models.http_validation_error import HTTPValidationError
from geonode_scraper_sdk.models.job_status import JobStatus
from geonode_scraper_sdk.models.output_format import OutputFormat
from geonode_scraper_sdk.models.processing_mode import ProcessingMode
from geonode_scraper_sdk.rest import ApiException


@pytest.fixture
def extraction_api(mock_api_client):
    return ExtractionApi(mock_api_client)


_SYNC_RESPONSE = {
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

_ASYNC_RESPONSE = {
    "job_id": "test-job-uuid",
    "status": "queued",
    "status_url": "http://api.mock.local/v1/extract/test-job-uuid",
    "estimated_tokens": 50,
}

_JOB_STATUS_RESPONSE = {
    "job_id": "test-job-uuid",
    "status": "completed",
    "created_at": "2026-01-01T00:00:00Z",
    "completed_at": "2026-01-01T00:00:05Z",
    "data": {"html": "<html/>"},
    "metadata": {
        "url": "https://example.com",
        "render_js": False,
        "formats": ["html"],
        "processing_mode": "sync",
    },
    "tokens_charged": 10,
}

_JOB_LIST_RESPONSE = {
    "jobs": [
        {
            "job_id": "00000000-0000-0000-0000-000000000001",
            "status": "completed",
            "url": "https://example.com",
            "created_at": "2026-01-01T00:00:00Z",
        }
    ],
    "page": 1,
    "page_size": 100,
    "page_count": 1,
}


def test_extract_sync(extraction_api, mock_api_client, make_mock_http_response):
    mock_resp = make_mock_http_response(200, _SYNC_RESPONSE)
    with patch.object(mock_api_client.rest_client.pool_manager, "request", return_value=mock_resp):
        response = extraction_api.extract_v1_extract_post(extract_request=ExtractRequest(url="https://example.com"))
    assert response is not None
    assert response.tokens_charged == 10
    assert response.data.html == "<html><body>Example</body></html>"
    assert response.metadata.url == "https://example.com"


def test_extract_async(extraction_api, mock_api_client, make_mock_http_response):
    mock_resp = make_mock_http_response(202, _ASYNC_RESPONSE)
    with patch.object(mock_api_client.rest_client.pool_manager, "request", return_value=mock_resp):
        response = extraction_api.extract_v1_extract_post(
            extract_request=ExtractRequest(
                url="https://example.com",
                processing_mode=ProcessingMode.ASYNC,
            )
        )
    assert response is not None
    assert response.job_id == "test-job-uuid"
    assert response.estimated_tokens == 50


def test_extract_sync_serializes_defaults_and_auth_header(
    extraction_api,
    mock_api_client,
    make_mock_http_response,
    get_request_details,
):
    mock_resp = make_mock_http_response(200, _SYNC_RESPONSE)
    with patch.object(mock_api_client.rest_client.pool_manager, "request", return_value=mock_resp) as mock_req:
        extraction_api.extract_v1_extract_post(extract_request=ExtractRequest(url="https://example.com"))

    request_details = get_request_details(mock_req)

    assert request_details["method"] == "POST"
    assert request_details["headers"]["X-Api-Key"] == "test-mock-api-key"
    assert request_details["headers"]["Content-Type"] == "application/json"
    assert request_details["headers"]["Accept"] == "application/json"
    assert request_details["body"] == {
        "url": "https://example.com",
        "formats": ["html"],
        "render_js": False,
        "processing_mode": "sync",
    }


@pytest.mark.parametrize(
    ("status", "fixture_name", "code", "retryable"),
    [
        (400, "error_400_json", "BAD_REQUEST", False),
        (401, "error_401_json", "UNAUTHORIZED", False),
        (402, "error_402_json", "PAYMENT_REQUIRED", False),
        (429, "error_429_json", "RATE_LIMITED", True),
        (500, "error_500_json", "INTERNAL_ERROR", True),
        (503, "error_503_json", "SERVICE_UNAVAILABLE", True),
    ],
)
def test_extract_error_responses(
    extraction_api,
    mock_api_client,
    make_mock_http_response,
    request,
    assert_api_exception_payload,
    status,
    fixture_name,
    code,
    retryable,
):
    mock_resp = make_mock_http_response(status, request.getfixturevalue(fixture_name))
    with patch.object(mock_api_client.rest_client.pool_manager, "request", return_value=mock_resp):
        with pytest.raises(ApiException) as exc_info:
            extraction_api.extract_v1_extract_post(extract_request=ExtractRequest(url="https://example.com"))

    assert_api_exception_payload(
        exc_info,
        status=status,
        data_type=ErrorResponse,
        code=code,
        retryable=retryable,
    )


def test_extract_unprocessable_entity(
    extraction_api,
    mock_api_client,
    make_mock_http_response,
    extraction_error_422_json,
    assert_api_exception_payload,
):
    mock_resp = make_mock_http_response(422, extraction_error_422_json)
    with patch.object(mock_api_client.rest_client.pool_manager, "request", return_value=mock_resp):
        with pytest.raises(ApiException) as exc_info:
            extraction_api.extract_v1_extract_post(extract_request=ExtractRequest(url="https://example.com"))

    assert_api_exception_payload(
        exc_info,
        status=422,
        data_type=ExtractionErrorResponse,
        code=ExtractionErrorCode.TIMEOUT,
        retryable=True,
    )
    assert exc_info.value.data.tokens_charged == 7


def test_get_job_result(extraction_api, mock_api_client, make_mock_http_response):
    mock_resp = make_mock_http_response(200, _JOB_STATUS_RESPONSE)
    with patch.object(mock_api_client.rest_client.pool_manager, "request", return_value=mock_resp):
        response = extraction_api.get_job_result_v1_extract_job_id_get(job_id="test-job-uuid")
    assert response is not None
    assert response.job_id == "test-job-uuid"
    assert response.tokens_charged == 10


def test_get_job_result_not_found(
    extraction_api,
    mock_api_client,
    make_mock_http_response,
    error_404_json,
    assert_api_exception_payload,
):
    mock_resp = make_mock_http_response(404, error_404_json)
    with patch.object(mock_api_client.rest_client.pool_manager, "request", return_value=mock_resp):
        with pytest.raises(ApiException) as exc_info:
            extraction_api.get_job_result_v1_extract_job_id_get(job_id="nonexistent")
    assert_api_exception_payload(
        exc_info,
        status=404,
        data_type=ErrorResponse,
        code="NOT_FOUND",
        retryable=False,
    )


def test_get_job_result_unauthorized(
    extraction_api,
    mock_api_client,
    make_mock_http_response,
    error_401_json,
    assert_api_exception_payload,
):
    mock_resp = make_mock_http_response(401, error_401_json)
    with patch.object(mock_api_client.rest_client.pool_manager, "request", return_value=mock_resp):
        with pytest.raises(ApiException) as exc_info:
            extraction_api.get_job_result_v1_extract_job_id_get(job_id="test-job-uuid")

    assert_api_exception_payload(
        exc_info,
        status=401,
        data_type=ErrorResponse,
        code="UNAUTHORIZED",
        retryable=False,
    )


def test_get_job_result_validation_error(
    extraction_api,
    mock_api_client,
    make_mock_http_response,
    path_validation_error_json,
    assert_api_exception_payload,
):
    mock_resp = make_mock_http_response(422, path_validation_error_json)
    with patch.object(mock_api_client.rest_client.pool_manager, "request", return_value=mock_resp):
        with pytest.raises(ApiException) as exc_info:
            extraction_api.get_job_result_v1_extract_job_id_get(job_id="bad-job-id")

    assert_api_exception_payload(
        exc_info,
        status=422,
        data_type=HTTPValidationError,
    )
    assert exc_info.value.data.detail[0].loc[0].actual_instance == "path"
    assert exc_info.value.data.detail[0].loc[1].actual_instance == "job_id"


def test_list_jobs(extraction_api, mock_api_client, make_mock_http_response):
    mock_resp = make_mock_http_response(200, _JOB_LIST_RESPONSE)
    with patch.object(mock_api_client.rest_client.pool_manager, "request", return_value=mock_resp):
        response = extraction_api.list_jobs_v1_extract_jobs_get()
    assert response is not None
    assert len(response.jobs) == 1
    assert response.page == 1
    assert response.page_count == 1


@pytest.mark.parametrize(
    ("kwargs", "expected_query"),
    [
        ({"job_id": "test-job-uuid"}, {"job_id": "test-job-uuid"}),
        ({"url": "https://example.com/path?q=1"}, {"url": "https://example.com/path?q=1"}),
        ({"status": JobStatus.COMPLETED}, {"status": "completed"}),
        ({"output": OutputFormat.HTML}, {"output": "html"}),
        (
            {"start_date": datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc)},
            {"start_date": datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc)},
        ),
        (
            {"end_date": datetime(2026, 1, 7, 23, 59, 59, tzinfo=timezone.utc)},
            {"end_date": datetime(2026, 1, 7, 23, 59, 59, tzinfo=timezone.utc)},
        ),
        ({"page": 2, "page_size": 10}, {"page": "2", "page_size": "10"}),
    ],
)
def test_list_jobs_serializes_each_filter(
    extraction_api,
    mock_api_client,
    make_mock_http_response,
    get_request_details,
    kwargs,
    expected_query,
):
    mock_resp = make_mock_http_response(200, _JOB_LIST_RESPONSE)
    with patch.object(mock_api_client.rest_client.pool_manager, "request", return_value=mock_resp) as mock_req:
        extraction_api.list_jobs_v1_extract_jobs_get(**kwargs)

    request_details = get_request_details(mock_req)
    query = request_details["query"]
    for key, expected in expected_query.items():
        if isinstance(expected, datetime):
            expected = expected.strftime(mock_api_client.configuration.datetime_format)
        assert query[key] == expected
    assert request_details["headers"]["X-Api-Key"] == "test-mock-api-key"


def test_list_jobs_serializes_all_filters_together(
    extraction_api,
    mock_api_client,
    make_mock_http_response,
    get_request_details,
):
    start = datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    end = datetime(2026, 1, 7, 23, 59, 59, tzinfo=timezone.utc)
    mock_resp = make_mock_http_response(200, _JOB_LIST_RESPONSE)
    with patch.object(mock_api_client.rest_client.pool_manager, "request", return_value=mock_resp) as mock_req:
        extraction_api.list_jobs_v1_extract_jobs_get(
            job_id="test-job-uuid",
            url="https://example.com/path?q=1",
            status=JobStatus.COMPLETED,
            output=OutputFormat.MARKDOWN,
            start_date=start,
            end_date=end,
            page=2,
            page_size=10,
        )

    query = get_request_details(mock_req)["query"]
    assert query == {
        "job_id": "test-job-uuid",
        "url": "https://example.com/path?q=1",
        "status": "completed",
        "output": "markdown",
        "start_date": start.strftime(mock_api_client.configuration.datetime_format),
        "end_date": end.strftime(mock_api_client.configuration.datetime_format),
        "page": "2",
        "page_size": "10",
    }


@pytest.mark.parametrize(
    ("status", "fixture_name", "code", "retryable"),
    [
        (401, "error_401_json", "UNAUTHORIZED", False),
        (404, "error_404_json", "NOT_FOUND", False),
    ],
)
def test_list_jobs_error_responses(
    extraction_api,
    mock_api_client,
    make_mock_http_response,
    request,
    assert_api_exception_payload,
    status,
    fixture_name,
    code,
    retryable,
):
    mock_resp = make_mock_http_response(status, request.getfixturevalue(fixture_name))
    with patch.object(mock_api_client.rest_client.pool_manager, "request", return_value=mock_resp):
        with pytest.raises(ApiException) as exc_info:
            extraction_api.list_jobs_v1_extract_jobs_get(job_id="test-job-uuid")

    assert_api_exception_payload(
        exc_info,
        status=status,
        data_type=ErrorResponse,
        code=code,
        retryable=retryable,
    )


def test_list_jobs_validation_error(
    extraction_api,
    mock_api_client,
    make_mock_http_response,
    query_validation_error_json,
    assert_api_exception_payload,
):
    mock_resp = make_mock_http_response(422, query_validation_error_json)
    with patch.object(mock_api_client.rest_client.pool_manager, "request", return_value=mock_resp):
        with pytest.raises(ApiException) as exc_info:
            extraction_api.list_jobs_v1_extract_jobs_get(page=1)

    assert_api_exception_payload(
        exc_info,
        status=422,
        data_type=HTTPValidationError,
    )
    assert exc_info.value.data.detail[0].loc[0].actual_instance == "query"
    assert exc_info.value.data.detail[0].msg == "Input should be greater than or equal to 1"
