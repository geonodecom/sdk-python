from geonode_scraper_sdk.models.error_response import ErrorResponse
from geonode_scraper_sdk.models.extraction_error import ExtractionError
from geonode_scraper_sdk.models.extraction_error_code import ExtractionErrorCode
from geonode_scraper_sdk.models.extraction_error_response import ExtractionErrorResponse
from geonode_scraper_sdk.models.http_validation_error import HTTPValidationError
from geonode_scraper_sdk.models.location_inner import LocationInner
from geonode_scraper_sdk.models.validation_error import ValidationError


def test_error_response_required_fields():
    err = ErrorResponse(code="UNAUTHORIZED", message="Invalid API key", retryable=False)
    assert err.code == "UNAUTHORIZED"
    assert err.message == "Invalid API key"
    assert err.retryable is False
    assert err.correlation_id is None


def test_error_response_with_correlation_id():
    err = ErrorResponse(
        code="INTERNAL_ERROR",
        message="Something went wrong",
        retryable=True,
        correlation_id="abc-123",
    )
    assert err.correlation_id == "abc-123"
    assert err.retryable is True


def test_extraction_error_code_all_values():
    expected = {
        "RATE_LIMITED",
        "WORK_CONCURRENCY_LIMITED",
        "WORK_CONCURRENCY_LEASE_EXPIRED",
        "TEMPORARY_BLOCK",
        "NETWORK_ERROR",
        "CAPTCHA_CHALLENGE",
        "PERMANENT_BLOCK",
        "INVALID_URL",
        "INVALID_WAIT_FOR_SELECTOR",
        "WAIT_FOR_SELECTOR_TIMEOUT",
        "UNPROCESSABLE_CONTENT",
        "AUTH_REQUIRED",
        "TIMEOUT",
        "PAYMENT_REQUIRED",
        "INTERNAL_ERROR",
        "PROXY_ERROR",
        "CANCELLED",
    }
    actual = {member.value for member in ExtractionErrorCode}
    assert actual == expected


def test_extraction_error_code_is_str_enum():
    assert ExtractionErrorCode.RATE_LIMITED == "RATE_LIMITED"
    assert isinstance(ExtractionErrorCode.TIMEOUT, str)


def test_extraction_error_required_fields():
    err = ExtractionError(
        code=ExtractionErrorCode.TIMEOUT,
        message="Request timed out",
        retryable=True,
    )
    assert err.code == ExtractionErrorCode.TIMEOUT
    assert err.message == "Request timed out"
    assert err.retryable is True
    assert err.details is None


def test_extraction_error_with_details():
    err = ExtractionError(
        code=ExtractionErrorCode.CAPTCHA_CHALLENGE,
        message="CAPTCHA detected",
        retryable=True,
        details={"challenge_type": "recaptcha"},
    )
    assert err.details == {"challenge_type": "recaptcha"}


def test_extraction_error_response_structure():
    inner = ExtractionError(
        code=ExtractionErrorCode.NETWORK_ERROR,
        message="Connection refused",
        retryable=True,
    )
    resp = ExtractionErrorResponse(error=inner, tokens_charged=0)
    assert resp.tokens_charged == 0
    assert resp.error.code == ExtractionErrorCode.NETWORK_ERROR


def test_extraction_error_response_round_trip():
    resp = ExtractionErrorResponse(
        error=ExtractionError(
            code=ExtractionErrorCode.TIMEOUT,
            message="Request timed out",
            retryable=True,
            details={"attempt": "2"},
        ),
        tokens_charged=4,
    )
    restored = ExtractionErrorResponse.from_json(resp.to_json())
    assert restored == resp


def test_location_inner_accepts_string():
    loc = LocationInner("body")
    assert loc.actual_instance == "body"


def test_location_inner_accepts_int():
    loc = LocationInner(0)
    assert loc.actual_instance == 0


def test_validation_error_structure():
    ve = ValidationError(
        loc=[LocationInner("body"), LocationInner("url")],
        msg="field required",
        type="missing",
    )
    assert ve.msg == "field required"
    assert ve.type == "missing"
    assert len(ve.loc) == 2


def test_http_validation_error_structure():
    ve = ValidationError(
        loc=[LocationInner("body")],
        msg="value is not a valid URL",
        type="url",
    )
    http_err = HTTPValidationError(detail=[ve])
    assert len(http_err.detail) == 1
    assert http_err.detail[0].msg == "value is not a valid URL"


def test_http_validation_error_empty_detail():
    http_err = HTTPValidationError(detail=[])
    assert http_err.detail == []


def test_http_validation_error_round_trip():
    http_err = HTTPValidationError(
        detail=[
            ValidationError(
                loc=[LocationInner("query"), LocationInner("page")],
                msg="Input should be greater than or equal to 1",
                type="greater_than_equal",
            )
        ]
    )
    restored = HTTPValidationError.from_dict(http_err.to_dict())
    assert restored.to_dict() == http_err.to_dict()
