# Geonode Scraper SDK for Python

[Integrations page](https://geonode.com/integrations/sdk-python) · [Geonode API docs](https://docs.geonode.com/docs/scraper-api) · [GitHub source](https://github.com/geonodecom/sdk-python) · [Python SDK setup guide](https://docs.geonode.com/docs/scraper-api/guides/sdks/python) · [Published package](https://pypi.org/project/geonode-scraper-sdk/) · [Repository overview](../README.md)

**[Try Geonode for free](https://app.geonode.com/sign-up)**

The Python SDK for the [Geonode Scraper API](https://geonode.com/products/scraper-api). It turns any web page into clean Markdown or HTML, and also crawls sites, maps their URLs, runs web searches and reports your usage. Package: [`geonode-scraper-sdk` on PyPI](https://pypi.org/project/geonode-scraper-sdk/).

## Before you start

- Python 3.10 or newer.
- A Geonode API key. Sign in to the [Geonode dashboard](https://app.geonode.com/), open **API Keys**, and create a key or copy an existing one.

## Install

```sh
pip install geonode-scraper-sdk
```

## Authenticate

Every request sends your key in the `X-Api-Key` header. Pass it once in `Configuration`. Keep the key out of your code, for example in an environment variable:

```python
import os

from geonode_scraper_sdk import Configuration

configuration = Configuration(api_key={"ApiKeyAuth": os.environ["GEONODE_SCRAPER_API_KEY"]})
```

You don't need to set `host`: the client calls the production API, `https://scraper.geonode.io`. The examples below use this `configuration`.

## Your first request

Extract a page as Markdown. The call waits until the page is ready.

```python
from geonode_scraper_sdk import ApiClient, ExtractionApi, ExtractRequest, OutputFormat

with ApiClient(configuration) as api_client:
    api = ExtractionApi(api_client)
    response = api.extract_v1_extract_post(
        ExtractRequest(url="https://example.com", formats=[OutputFormat.MARKDOWN])
    )
    print(response.data.markdown)
    print(response.tokens_charged)  # what this request cost
```

## Common tasks

### Render JavaScript, pick a country, wait for an element

```python
from geonode_scraper_sdk import ExtractRequest, OutputFormat, ProxySettings, ProxyType, WaitConfig, WaitUntil

request = ExtractRequest(
    url="https://example.com/products",
    formats=[OutputFormat.MARKDOWN],
    render_js=True,                                   # use a headless browser
    proxy=ProxySettings(country="DE", type=ProxyType.RESIDENTIAL),
    wait_config=WaitConfig(wait_until=WaitUntil.NETWORKIDLE, wait_for="#content", wait_timeout=2000),
    timeout=60000,                                    # give up after 60 s
)
```

All options are in [Request options](#request-options).

### Run an extraction in the background

Send the request with `ProcessingMode.ASYNC` to get a job ID at once, then check the job until it finishes.

```python
import time

from geonode_scraper_sdk import ApiClient, ExtractionApi, ExtractRequest, JobStatus, ProcessingMode

DONE = {JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED}

with ApiClient(configuration) as api_client:
    api = ExtractionApi(api_client)
    accepted = api.extract_v1_extract_post(
        ExtractRequest(url="https://example.com", processing_mode=ProcessingMode.ASYNC)
    )
    job = api.get_job_result_v1_extract_job_id_get(accepted.job_id)
    while job.status not in DONE:
        time.sleep(2)
        job = api.get_job_result_v1_extract_job_id_get(accepted.job_id)

    if job.status == JobStatus.COMPLETED:
        print(job.data.html)
    else:
        print(job.status, job.error)
```

To be notified instead of checking, use [webhooks](#get-notified-with-webhooks).

### Extract many URLs at once (batch)

```python
from geonode_scraper_sdk import ApiClient, BatchApi, BatchRequest, OutputFormat

with ApiClient(configuration) as api_client:
    api = BatchApi(api_client)
    accepted = api.create_batch_v1_batch_post(
        BatchRequest(urls=["https://example.com", "https://example.org"], formats=[OutputFormat.MARKDOWN])
    )
    status = api.get_batch_status_v1_batch_job_id_get(job_id=accepted.job_id, page=1, page_size=50)
    print(status.status, f"{status.completed_urls}/{status.total_urls}")
    for item in status.results or []:
        print(item.url, item.status)
```

Check the status again until it is `COMPLETED`, as in the background example above. `results` comes in pages: use `page` and `page_size`.

### Crawl a site

Start from one URL and follow links up to a depth and a page limit.

```python
from geonode_scraper_sdk import ApiClient, CrawlApi, CrawlRequest, OutputFormat

with ApiClient(configuration) as api_client:
    api = CrawlApi(api_client)
    accepted = api.create_crawl_v1_crawl_post(
        CrawlRequest(url="https://example.com", depth=2, limit=50, formats=[OutputFormat.MARKDOWN])
    )
    print(accepted.job_id, accepted.estimated_pages)
    status = api.get_crawl_status_v1_crawl_job_id_get(job_id=accepted.job_id, page=1, page_size=50)
    print(status.status, f"{status.completed_pages}/{status.total_pages}")
```

### List a site's URLs (map)

Find the URLs under a site from its sitemap and links. Returns at once.

```python
from geonode_scraper_sdk import ApiClient, MapApi, MapRequest

with ApiClient(configuration) as api_client:
    result = MapApi(api_client).map_urls_v1_map_post(MapRequest(url="https://example.com"))
    for link in result.links or []:
        print(link.url, link.source)
```

Add `search="pricing"` to keep only matching URLs.

### Search the web

```python
from geonode_scraper_sdk import ApiClient, SearchApi, SearchRequest

with ApiClient(configuration) as api_client:
    result = SearchApi(api_client).search_v1_search_post(SearchRequest(query="geonode scraper api"))
    for hit in result.results:
        print(hit.position, hit.title, hit.url)
```

### Get notified with webhooks

Subscribe a URL to an event. Every finished extraction then sends a POST to that URL.

```python
from geonode_scraper_sdk import ApiClient, WebhookCreate, WebhookEventType, WebhooksApi

with ApiClient(configuration) as api_client:
    webhook = WebhooksApi(api_client).create_webhook_v1_webhooks_post(
        WebhookCreate(url="https://your-app.example/hooks/geonode", event_type=WebhookEventType.EXTRACT_COMPLETED)
    )
    print(webhook.id, webhook.secret)  # store the secret: it signs every delivery
```

Events: `EXTRACT_COMPLETED`, `BATCH_COMPLETED`, `CRAWL_COMPLETED`. Each delivery is JSON with `event`, `webhook_id`, `delivery_id`, `timestamp` and `data`. Check that a delivery comes from Geonode by comparing its `X-Webhook-Signature` header with an HMAC-SHA256 of the raw body:

```python
import hashlib
import hmac


def is_from_geonode(raw_body: bytes, signature_header: str, secret: str) -> bool:
    expected = "sha256=" + hmac.new(secret.encode(), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature_header)
```

Answer with any 2xx status. A 429 or 5xx answer makes Geonode retry the delivery. `rotate_secret_v1_webhooks_webhook_id_rotate_secret_post` issues a new secret and invalidates the old one.

### Check usage

```python
from datetime import datetime, timedelta, timezone

from geonode_scraper_sdk import ApiClient, StatisticsApi, UsageApi

with ApiClient(configuration) as api_client:
    usage = UsageApi(api_client).get_concurrency_usage_v1_usage_concurrency_get()
    print(f"{usage.work_concurrency_in_use} of {usage.work_concurrency_limit} concurrent requests in use")

    week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    stats = StatisticsApi(api_client).get_statistics_v1_statistics_get(start_date=week_ago)
    print(stats.extraction_count, stats.success_rate, stats.period_tokens_used)
```

## Request options

`ExtractRequest` fields. Batch and crawl take the same `formats`, `render_js`, `proxy` and `wait_config`.

| Field | Default | What it does |
|---|---|---|
| `url` | required | The page to extract. |
| `formats` | `[OutputFormat.HTML]` | `MARKDOWN`, `HTML` or both. |
| `render_js` | `False` | Load the page in a headless browser. Slower and costs more; use it when the content needs JavaScript. |
| `processing_mode` | `SYNC` | `SYNC` waits for the result; `ASYNC` returns a job ID at once. |
| `proxy` | residential, country from the URL | `type`: `RESIDENTIAL`, `DATACENTER` or `MIX`. `country`: a two-letter code such as `"US"`. Without a country, the API picks one from the URL. |
| `headers` | none | Extra HTTP headers for the target. `Host` is ignored. On browser requests `Accept-Language` sets the browser's language. |
| `timeout` | the API's ceiling | Milliseconds the request may take, including any wait in the queue. Sync requests only; at least 1000. |
| `wait_config` | adaptive | Browser waits, in this order: `wait_until` (`COMMIT`, `DOMCONTENTLOADED`, `LOAD`, `NETWORKIDLE`), `wait_for` (a CSS selector, or an XPath starting with `//` or `xpath=`), `wait_timeout` (0 to 30000 ms). Setting it turns on `render_js`. |

## Errors and limits

A failed request raises `ApiException` or one of its subclasses. `exc.status` is the HTTP status, `exc.body` the raw JSON, and `exc.headers` the response headers.

```python
from geonode_scraper_sdk import ApiClient, ApiException, ExtractionApi, ExtractRequest

with ApiClient(configuration) as api_client:
    try:
        ExtractionApi(api_client).extract_v1_extract_post(ExtractRequest(url="https://example.com"))
    except ApiException as exc:
        print(exc.status, exc.body)
        if exc.status == 429:
            print("retry after", exc.headers.get("Retry-After"), "seconds")
```

| Status | Meaning | Retry? |
|---|---|---|
| 401 | The API key is missing or wrong. | No |
| 402 | No active plan, or not enough balance. | After topping up |
| 403 | The target is blocked by Geonode's compliance list (`TARGET_BLOCKED`). Not charged. | No |
| 422 | Either the request is invalid (the body's `detail` names the bad fields), or the page could not be extracted. In the second case `error.code` says why, for example `PERMANENT_BLOCK` or `CAPTCHA_CHALLENGE`, and `error.retryable` says whether trying again can help. | Fix the request; retry only if `retryable` is true |
| 429 | Too many requests, or all your concurrent requests are in use. | Yes, after `Retry-After` |
| 503 | Temporarily unavailable. For browser pages, `ASYNC` mode may still work. | Yes, with a delay |
| 504 | The request did not finish within its `timeout`. | Yes, or raise `timeout` |
| 500 | An error on our side. | Yes, with a delay |

More in [error handling](https://docs.geonode.com/docs/scraper-api/troubleshooting/error-handling). Prices per request type are on the [pricing page](https://docs.geonode.com/docs/scraper-api/additional-resources/pricing).

## Reference

| Class | Method | Endpoint |
|---|---|---|
| `ExtractionApi` | `extract_v1_extract_post` | `POST /v1/extract` |
| | `get_job_result_v1_extract_job_id_get` | `GET /v1/extract/{job_id}` |
| | `list_jobs_v1_extract_jobs_get` | `GET /v1/extract/jobs` |
| `BatchApi` | `create_batch_v1_batch_post` | `POST /v1/batch` |
| | `get_batch_status_v1_batch_job_id_get` | `GET /v1/batch/{job_id}` |
| | `cancel_batch_v1_batch_job_id_delete` | `DELETE /v1/batch/{job_id}` |
| | `list_batch_jobs_v1_batch_jobs_get` | `GET /v1/batch/jobs` |
| `CrawlApi` | `create_crawl_v1_crawl_post` | `POST /v1/crawl` |
| | `get_crawl_status_v1_crawl_job_id_get` | `GET /v1/crawl/{job_id}` |
| | `cancel_crawl_v1_crawl_job_id_delete` | `DELETE /v1/crawl/{job_id}` |
| | `list_crawl_jobs_v1_crawl_jobs_get` | `GET /v1/crawl/jobs` |
| `MapApi` | `map_urls_v1_map_post` | `POST /v1/map` |
| | `list_map_jobs_v1_map_jobs_get`, `get_map_job_v1_map_job_id_get` | `GET /v1/map/jobs`, `GET /v1/map/{job_id}` |
| `SearchApi` | `search_v1_search_post` | `POST /v1/search` |
| | `list_search_jobs_v1_search_jobs_get`, `get_search_job_v1_search_job_id_get` | `GET /v1/search/jobs`, `GET /v1/search/{job_id}` |
| `WebhooksApi` | `create_webhook_v1_webhooks_post`, `list_webhooks_v1_webhooks_get`, `get_webhook_v1_webhooks_webhook_id_get`, `update_webhook_v1_webhooks_webhook_id_patch`, `delete_webhook_v1_webhooks_webhook_id_delete` | `/v1/webhooks` |
| | `list_deliveries_v1_webhooks_webhook_id_deliveries_get`, `rotate_secret_v1_webhooks_webhook_id_rotate_secret_post` | `/v1/webhooks/{webhook_id}/…` |
| `UsageApi` | `get_concurrency_usage_v1_usage_concurrency_get` | `GET /v1/usage/concurrency` |
| `StatisticsApi` | `get_statistics_v1_statistics_get` | `GET /v1/statistics` |
| `SystemApi` | `health_check_health_get` | `GET /health` |

Every method also has a `*_with_http_info` variant that returns the status code and headers with the result, and a `*_without_preload_content` variant that returns the raw HTTP response. Full request and response schemas are in the [API reference](https://docs.geonode.com/docs/scraper-api/v1/reference).

## Versions and support

- The latest version is on [PyPI](https://pypi.org/project/geonode-scraper-sdk/). The API stays backward compatible, so code written for an older version keeps working; new API features arrive in a new SDK release.
- Requests send `User-Agent: geonode-python-sdk/<version>`, which helps support see which version you use. Set `api_client.user_agent` to change it.
- Questions or problems: [contact Geonode](https://geonode.com/contact).
