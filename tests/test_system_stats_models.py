from datetime import datetime, timezone

from geonode_scraper_sdk.models.health_response import HealthResponse
from geonode_scraper_sdk.models.health_status import HealthStatus
from geonode_scraper_sdk.models.request_count_response import RequestCountResponse
from geonode_scraper_sdk.models.statistics_response import StatisticsResponse
from geonode_scraper_sdk.models.tokens_usage_response import TokensUsageResponse

_NOW = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
_TODAY = datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc)


def test_health_status_all_values():
    expected = {"ok", "degraded", "unavailable"}
    assert {member.value for member in HealthStatus} == expected


def test_health_status_is_str_enum():
    assert HealthStatus.OK == "ok"
    assert isinstance(HealthStatus.DEGRADED, str)


def test_health_response_required_fields():
    resp = HealthResponse(
        version="0.1.0",
        service="scraper-api",
        timestamp=_NOW,
        status=HealthStatus.OK,
    )
    assert resp.version == "0.1.0"
    assert resp.service == "scraper-api"
    assert resp.status == HealthStatus.OK
    assert resp.timestamp == _NOW


def test_health_response_degraded():
    resp = HealthResponse(
        version="0.1.0",
        service="scraper-api",
        timestamp=_NOW,
        status=HealthStatus.DEGRADED,
    )
    assert resp.status == HealthStatus.DEGRADED


def test_health_response_serialization():
    resp = HealthResponse(
        version="0.1.0",
        service="scraper-api",
        timestamp=_NOW,
        status=HealthStatus.OK,
    )
    d = resp.to_dict()
    assert d["version"] == "0.1.0"
    assert d["status"] == "ok"


def test_request_count_response_fields():
    rc = RequestCountResponse(date=_TODAY, success_request_count=42, failed_request_count=3)
    assert rc.var_date == _TODAY
    assert rc.success_request_count == 42
    assert rc.failed_request_count == 3


def test_tokens_usage_response_fields():
    tu = TokensUsageResponse(date=_TODAY, tokens_used=1000)
    assert tu.var_date == _TODAY
    assert tu.tokens_used == 1000


def test_statistics_response_required_fields():
    resp = StatisticsResponse(
        extraction_count=100,
        previous_period_extraction_count=80,
        success_rate=0.95,
        average_extraction_duration=1500,
        period_tokens_used=5000,
    )
    assert resp.extraction_count == 100
    assert resp.success_rate == 0.95
    assert resp.requests is None
    assert resp.tokens_used is None


def test_statistics_response_with_daily_breakdown():
    rc = RequestCountResponse(date=_TODAY, success_request_count=10, failed_request_count=1)
    tu = TokensUsageResponse(date=_TODAY, tokens_used=250)
    resp = StatisticsResponse(
        extraction_count=11,
        previous_period_extraction_count=9,
        success_rate=0.909,
        average_extraction_duration=800,
        period_tokens_used=250,
        requests=[rc],
        tokens_used=[tu],
    )
    assert len(resp.requests) == 1
    assert resp.requests[0].success_request_count == 10
    assert len(resp.tokens_used) == 1
    assert resp.tokens_used[0].tokens_used == 250
