# Changelog

All notable changes to the Python SDK will be documented in this file.

The format is inspired by Keep a Changelog.

## [Unreleased]

- Removed the internal repository preparation notes and links to the old monorepo.

- Docs links point to the package's page at https://docs.geonode.com/docs/scraper-api/guides/sdks/python.

- Prepare standalone source repository with documentation and self-contained maintainer tooling. Package name and version are unchanged.


- README rewritten so it can be published as the Python SDK page on docs.geonode.com: setup, common tasks including background jobs and webhooks, request options, errors and a method reference. The examples no longer set a placeholder `host`, so they call the production API as written.
- `Configuration` no longer lists an internal-only auth scheme. No SDK method used it.

## [0.6.1] - 2026-10-21

- The package page links to geonode.com, the Scraper API docs and sign-up.
- README: a sign-up link near the top.

## [0.6.0] - 2026-10-19

- Requests now send `User-Agent: geonode-python-sdk/<version>` instead of the generator default `OpenAPI-Generator/<version>/python`. Set `ApiClient.user_agent` to override it.
- `Configuration()` without a `host` now points at the production API, `https://scraper.geonode.io`, instead of `http://localhost`.

## [0.5.0] - 2026-09-16

- `ExtractRequest`: added `timeout`, the per-request budget in milliseconds counted from receipt and including queue wait. Sync requests only.
- `SearchRequest` and `SearchResponse`: added `engine`, so a caller can choose the search engine and see which one answered.
- `ErrorResponse`: added `details` for additional error context.
- `ExtractionError`: added `correlation_id` of the failed extraction.
- `JobCollectionResponse`: added `is_capped`.
- `ExtractionErrorCode`: added `CANCELLED`.
- Removed `SearchErrorResponse`, which the API no longer returns.

## [0.4.0] - 2026-07-15

- Added Search API: `SearchApi` with `search_v1_search_post`, `list_search_jobs_v1_search_jobs_get`, `get_search_job_v1_search_job_id_get`.
- Added response models `SearchRequest`, `SearchResponse`, `SearchHitModel`, `SearchErrorResponse`, `SearchJobDetailResponse`, `SearchJobsResponse`, `SearchListItemResponse`.
- Added Usage API: `UsageApi` with `get_concurrency_usage_v1_usage_concurrency_get`, and the `ConcurrencyUsageResponse` model.
- `MapRequest.include_subdomains` now defaults to `False` (previously `True`); discovery is scoped to the exact seed host by default.
- `MapResponse` gained an optional `metadata` field (`MapMetadata`) with discovery duration and link-count diagnostics.
- The API-key security scheme was renamed `APIKeyHeader` → `ApiKeyAuth`. Update any `Configuration(api_key={...})` dict to use the new key.
- One more internal-only endpoint is intentionally excluded from the SDK.

## [0.3.0] - 2026-06-11

- Added job-listing endpoints: `BatchApi.list_batch_jobs_v1_batch_jobs_get`, `CrawlApi.list_crawl_jobs_v1_crawl_jobs_get`, `MapApi.list_map_jobs_v1_map_jobs_get`, and `MapApi.get_map_job_v1_map_job_id_get`.
- Added response models `BatchJobsResponse`, `BatchListItemResponse`, `CrawlJobsResponse`, `CrawlListItemResponse`, `MapJobsResponse`, `MapListItemResponse`, `MapJobDetailResponse`.
- `CrawlRequest`/`CrawlConfig`: `proxy` now references `ProxySettings` (the `CrawlProxySettings` model was removed).
- `ExtractRequest`: removed `extract_links`. `ExtractionData`: removed `links`.
- Internal-only endpoints are intentionally excluded from the SDK.

## [0.2.0] - 2026-06-03

- Added Batch API: `BatchApi` with `create_batch`, `get_batch_status`, `cancel_batch`.
- Added Crawl API: `CrawlApi` with `create_crawl`, `get_crawl_status`, `cancel_crawl`.
- Added Map API: `MapApi` with `map_urls`.
- Added Webhooks API: `WebhooksApi` with `create_webhook`, `list_webhooks`, `get_webhook`, `update_webhook`, `delete_webhook`, `list_deliveries`, `rotate_secret`.
- Added `WaitConfig` and `WaitUntil` models for browser wait policy control.
- `ExtractRequest`: added `extract_links` and `wait_config` fields; `proxy` now optional with residential default.
- `ExtractionData`: added optional `links` field.
- `ExtractionMetadata`: removed `retry_count` and `engine_used`; added `wait_config`.
- `ExtractionErrorCode`: added `WORK_CONCURRENCY_LIMITED`, `WORK_CONCURRENCY_LEASE_EXPIRED`, `INVALID_WAIT_FOR_SELECTOR`, `WAIT_FOR_SELECTOR_TIMEOUT`.

## [0.1.0] - 2026-04-09

- Initial public packaging, licensing, and release automation for the Python SDK.
