from datetime import datetime, timezone
from unittest.mock import patch

import pytest

from geonode_scraper_sdk.api.statistics_api import StatisticsApi
from geonode_scraper_sdk.models.error_response import ErrorResponse
from geonode_scraper_sdk.models.http_validation_error import HTTPValidationError
from geonode_scraper_sdk.rest import ApiException


@pytest.fixture
def statistics_api(mock_api_client):
    return StatisticsApi(mock_api_client)


_STATS_RESPONSE = {
    "extraction_count": 100,
    "previous_period_extraction_count": 80,
    "success_rate": 0.95,
    "average_extraction_duration": 1500,
    "period_tokens_used": 5000,
}


def test_get_statistics_success(statistics_api, mock_api_client, make_mock_http_response):
    mock_resp = make_mock_http_response(200, _STATS_RESPONSE)
    with patch.object(mock_api_client.rest_client.pool_manager, "request", return_value=mock_resp):
        response = statistics_api.get_statistics_v1_statistics_get()
    assert response is not None
    assert response.extraction_count == 100
    assert response.success_rate == 0.95
    assert response.period_tokens_used == 5000


def test_get_statistics_with_date_range(
    statistics_api,
    mock_api_client,
    make_mock_http_response,
    get_request_details,
):
    mock_resp = make_mock_http_response(200, {**_STATS_RESPONSE, "extraction_count": 10})
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    end = datetime(2026, 1, 7, tzinfo=timezone.utc)
    with patch.object(mock_api_client.rest_client.pool_manager, "request", return_value=mock_resp) as mock_req:
        response = statistics_api.get_statistics_v1_statistics_get(start_date=start, end_date=end)

    assert response.extraction_count == 10
    request_details = get_request_details(mock_req)
    assert request_details["query"] == {
        "start_date": start.strftime(mock_api_client.configuration.datetime_format),
        "end_date": end.strftime(mock_api_client.configuration.datetime_format),
    }
    assert request_details["headers"]["X-Api-Key"] == "test-mock-api-key"


def test_get_statistics_unauthorized(
    statistics_api,
    mock_api_client,
    make_mock_http_response,
    error_401_json,
    assert_api_exception_payload,
):
    mock_resp = make_mock_http_response(401, error_401_json)
    with patch.object(mock_api_client.rest_client.pool_manager, "request", return_value=mock_resp):
        with pytest.raises(ApiException) as exc_info:
            statistics_api.get_statistics_v1_statistics_get()

    assert_api_exception_payload(
        exc_info,
        status=401,
        data_type=ErrorResponse,
        code="UNAUTHORIZED",
        retryable=False,
    )


def test_get_statistics_validation_error(
    statistics_api,
    mock_api_client,
    make_mock_http_response,
    statistics_validation_error_json,
    assert_api_exception_payload,
):
    mock_resp = make_mock_http_response(422, statistics_validation_error_json)
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    end = datetime(2026, 1, 7, tzinfo=timezone.utc)
    with patch.object(mock_api_client.rest_client.pool_manager, "request", return_value=mock_resp):
        with pytest.raises(ApiException) as exc_info:
            statistics_api.get_statistics_v1_statistics_get(start_date=start, end_date=end)

    assert_api_exception_payload(
        exc_info,
        status=422,
        data_type=HTTPValidationError,
    )
    assert exc_info.value.data.detail[0].loc[0].actual_instance == "query"
    assert exc_info.value.data.detail[0].loc[1].actual_instance == "start_date"
