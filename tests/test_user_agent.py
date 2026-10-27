from unittest.mock import patch

import geonode_scraper_sdk
from geonode_scraper_sdk.api.system_api import SystemApi

# The API reads `geonode-<client>/<version>` from the User-Agent and keeps only allowlisted
# clients (scraper-api#674); this SDK's name there is `python-sdk`.
EXPECTED_USER_AGENT = f"geonode-python-sdk/{geonode_scraper_sdk.__version__}"

_HEALTH_PAYLOAD = {
    "version": "0.1.0",
    "service": "scraper-api",
    "timestamp": "2026-01-01T00:00:00Z",
    "status": "ok",
}


def test_default_user_agent_names_the_sdk_and_its_version():
    # Fails when the version is bumped without regenerating, which leaves the old version here.
    assert geonode_scraper_sdk.ApiClient().user_agent == EXPECTED_USER_AGENT


def test_request_sends_the_sdk_user_agent(mock_api_client, make_mock_http_response):
    mock_resp = make_mock_http_response(200, _HEALTH_PAYLOAD)
    with patch.object(mock_api_client.rest_client.pool_manager, "request", return_value=mock_resp) as request:
        SystemApi(mock_api_client).health_check_health_get()

    assert request.call_args.kwargs["headers"]["User-Agent"] == EXPECTED_USER_AGENT


def test_caller_can_still_override_the_user_agent(mock_api_client, make_mock_http_response):
    mock_api_client.user_agent = "my-app/1.0"
    mock_resp = make_mock_http_response(200, _HEALTH_PAYLOAD)
    with patch.object(mock_api_client.rest_client.pool_manager, "request", return_value=mock_resp) as request:
        SystemApi(mock_api_client).health_check_health_get()

    assert request.call_args.kwargs["headers"]["User-Agent"] == "my-app/1.0"
