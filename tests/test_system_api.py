from unittest.mock import patch

import pytest

from geonode_scraper_sdk.api.system_api import SystemApi
from geonode_scraper_sdk.models.health_status import HealthStatus
from geonode_scraper_sdk.rest import ApiException


@pytest.fixture
def system_api(mock_api_client):
    return SystemApi(mock_api_client)


_HEALTH_PAYLOAD = {
    "version": "0.1.0",
    "service": "scraper-api",
    "timestamp": "2026-01-01T00:00:00Z",
    "status": "ok",
}


def test_health_check_ok(system_api, mock_api_client, make_mock_http_response):
    mock_resp = make_mock_http_response(200, _HEALTH_PAYLOAD)
    with patch.object(mock_api_client.rest_client.pool_manager, "request", return_value=mock_resp):
        response = system_api.health_check_health_get()
    assert response is not None
    assert response.status == HealthStatus.OK
    assert response.version == "0.1.0"
    assert response.service == "scraper-api"


def test_health_check_degraded(system_api, mock_api_client, make_mock_http_response):
    """A 503 with a HealthResponse body raises ApiException (SDK behaviour for non-2xx)."""
    mock_resp = make_mock_http_response(503, {**_HEALTH_PAYLOAD, "status": "degraded"})
    with patch.object(mock_api_client.rest_client.pool_manager, "request", return_value=mock_resp):
        with pytest.raises(ApiException) as exc_info:
            system_api.health_check_health_get()
    assert exc_info.value.status == 503
