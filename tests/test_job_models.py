import uuid
from datetime import datetime, timezone

from geonode_scraper_sdk.models.extraction_error import ExtractionError
from geonode_scraper_sdk.models.extraction_error_code import ExtractionErrorCode
from geonode_scraper_sdk.models.job_collection_response import JobCollectionResponse
from geonode_scraper_sdk.models.job_list_item_response import JobListItemResponse
from geonode_scraper_sdk.models.job_status import JobStatus
from geonode_scraper_sdk.models.job_status_response import JobStatusResponse
from geonode_scraper_sdk.models.output_format import OutputFormat

_NOW = datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
_JOB_UUID = uuid.UUID("00000000-0000-0000-0000-000000000001")


def test_job_status_all_values():
    expected = {"queued", "processing", "completed", "failed", "cancelled"}
    assert {member.value for member in JobStatus} == expected


def test_job_status_is_str_enum():
    assert JobStatus.COMPLETED == "completed"
    assert isinstance(JobStatus.FAILED, str)


def test_job_status_response_minimal():
    resp = JobStatusResponse(
        job_id="abc-123",
        status=JobStatus.QUEUED,
        created_at=_NOW,
    )
    assert resp.job_id == "abc-123"
    assert resp.status == JobStatus.QUEUED
    assert resp.completed_at is None
    assert resp.data is None
    assert resp.error is None
    assert resp.tokens_charged is None


def test_job_status_response_completed(valid_extraction_data, valid_extraction_metadata):
    resp = JobStatusResponse(
        job_id="abc-123",
        status=JobStatus.COMPLETED,
        created_at=_NOW,
        completed_at=datetime(2026, 1, 1, 0, 0, 5, tzinfo=timezone.utc),
        data=valid_extraction_data,
        metadata=valid_extraction_metadata,
        tokens_charged=10,
    )
    assert resp.status == JobStatus.COMPLETED
    assert resp.tokens_charged == 10
    assert resp.data.html == "<html><body>Example</body></html>"


def test_job_status_response_failed():
    error = ExtractionError(
        code=ExtractionErrorCode.TIMEOUT,
        message="Request timed out",
        retryable=True,
    )
    resp = JobStatusResponse(
        job_id="abc-123",
        status=JobStatus.FAILED,
        created_at=_NOW,
        error=error,
    )
    assert resp.status == JobStatus.FAILED
    assert resp.error.code == ExtractionErrorCode.TIMEOUT
    assert resp.data is None


def test_job_list_item_response_required():
    item = JobListItemResponse(
        job_id=_JOB_UUID,
        status=JobStatus.COMPLETED,
        url="https://example.com",
        created_at=_NOW,
    )
    assert item.job_id == _JOB_UUID
    assert item.status == JobStatus.COMPLETED
    assert item.execution_time is None
    assert item.output is None


def test_job_list_item_response_with_optional():
    item = JobListItemResponse(
        job_id=_JOB_UUID,
        status=JobStatus.COMPLETED,
        url="https://example.com",
        created_at=_NOW,
        execution_time=1200,
        output=[OutputFormat.HTML, OutputFormat.MARKDOWN],
    )
    assert item.execution_time == 1200
    assert item.output == [OutputFormat.HTML, OutputFormat.MARKDOWN]


def test_job_collection_response_structure(valid_job_collection_response):
    resp = valid_job_collection_response
    assert len(resp.jobs) == 1
    assert resp.page == 1
    assert resp.page_size == 100
    assert resp.page_count == 1


def test_job_collection_response_empty():
    resp = JobCollectionResponse(jobs=[], page=1, page_size=100, page_count=0)
    assert resp.jobs == []
    assert resp.page_count == 0


def test_job_status_response_round_trip(valid_job_status_response):
    restored = JobStatusResponse.from_json(valid_job_status_response.to_json())
    assert restored == valid_job_status_response


def test_job_collection_response_round_trip(valid_job_collection_response):
    restored = JobCollectionResponse.from_dict(valid_job_collection_response.to_dict())
    assert restored == valid_job_collection_response
