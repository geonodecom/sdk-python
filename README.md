![Geonode Python SDK: Web Scraping & Data Extraction](assets/banner.svg)

# Geonode Python SDK: Web Scraping & Data Extraction

Build Python agents and data pipelines with Geonode’s typed clients. Extract pages, crawl sites, discover URLs, search the web and run batches. Use returned content in your own research and RAG workflows, with webhook subscriptions and usage statistics available from your code.

**[Try Geonode for free](https://app.geonode.com/sign-up)**

[Integrations page](https://geonode.com/integrations) · [Geonode API docs](https://docs.geonode.com/docs/scraper-api) · [Python SDK setup guide](https://docs.geonode.com/docs/scraper-api/guides/sdks/python) · [View package on PyPI](https://pypi.org/project/geonode-scraper-sdk/) · [View source on GitHub](https://github.com/geonodecom/sdk-python) · [Complete guide](docs/guide.md)

<!-- BEGIN README NAV -->
[Get started](#get-started) · [Example: prepare website content for retrieval](#example-prepare-website-content-for-retrieval) · [Setup questions](#setup-questions)
<!-- END README NAV -->

## Workflow ideas

- **Prepare documents for retrieval.** Extract Markdown from selected URLs, then pass it to your own chunking, embedding and storage pipeline.
- **Refresh a website dataset.** Crawl with depth and page limits, inspect results, and save content with its source URL.

## Get started

Requires Python 3.10 or newer and a [Geonode API key](https://app.geonode.com/). API requests use your Geonode account's plan and balance.

```sh
pip install geonode-scraper-sdk
```

Set `GEONODE_SCRAPER_API_KEY` in your server environment, then run:

```python
import os
from geonode_scraper_sdk import (
    ApiClient, Configuration, ExtractionApi, ExtractRequest, OutputFormat,
)

configuration = Configuration(
    api_key={"ApiKeyAuth": os.environ["GEONODE_SCRAPER_API_KEY"]}
)
with ApiClient(configuration) as client:
    result = ExtractionApi(client).extract_v1_extract_post(
        ExtractRequest(url="https://example.com", formats=[OutputFormat.MARKDOWN])
    )
    print(result.data.markdown)
```

The SDK sends your key in `X-Api-Key` to `https://scraper.geonode.io`. Keep the key out of source control and browser code.

## What you can build

| Task | Client |
| --- | --- |
| Extract a page as Markdown or HTML, with optional JavaScript rendering | `ExtractionApi` |
| Process many URLs and check or cancel jobs | `BatchApi` |
| Crawl linked pages with depth and page limits | `CrawlApi` |
| Discover a website's URLs | `MapApi` |
| Search the web | `SearchApi` |
| Configure notifications and manage delivery secrets | `WebhooksApi` |
| Inspect concurrency, usage and service health | `UsageApi`, `StatisticsApi`, `SystemApi` |

See the [complete guide](docs/guide.md) for background extraction, batch and crawl examples, proxy settings, webhooks, error handling and the method reference. Generated method names follow the API contract. The SDK is an API client; it does not bundle a local browser or MCP server.

<!-- BEGIN SHARED WORKFLOW GUIDE -->
## Understand the extraction result

The Python quick start requests Markdown and reads data.markdown from a completed extraction. Request HTML when you need data.html. Keep metadata.url alongside the content so later processing retains its source. tokens_charged reports the request's usage.

A background request returns a job ID and status instead of immediately returning finished content. Keep that ID, retrieve the job and inspect its terminal status before reading the result. A timeout after submission is not a reason to submit the same job again.

## Example: prepare website content for retrieval

1. Start with a small list of source URLs, or map a site and select the relevant pages.
2. Extract Markdown from one URL and inspect its content and source metadata before processing the list.
3. Use a batch for a known URL list, or a crawl with explicit depth and page limits when you need linked pages.
4. Pass completed content to your own chunking and embedding pipeline, then store the chunks with their source URLs and retrieval time.
5. Handle failed pages separately so partial results do not silently become a complete dataset.

**Expected result:** Page content and source metadata are ready for your application. Embeddings, vector storage, product-field parsing and change detection are separate steps you supply.

## Setup questions

Missing content? Confirm the requested format and whether the job has completed. Enable JavaScript rendering when the target depends on a browser, and inspect the returned status and error details.

Where does the API key belong? Keep it in your server environment and pass it through the SDK configuration. A browser application should call your own server instead of exposing the key.

Does installing the SDK run a scraper locally? It installs an API client. Extraction runs through the hosted Geonode service and uses your account's allowance.

Need MCP? Use the separate hosted MCP connection for a compatible assistant; this SDK does not start an MCP server.

These recipes describe source-supported workflows. They have not been run as authenticated end-to-end examples in this review.
<!-- END SHARED WORKFLOW GUIDE -->

## Development

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]' build twine
bash scripts/ruff.sh check
bash scripts/test.sh
python -m build
python -m twine check dist/*
```

Read [CONTRIBUTING.md](CONTRIBUTING.md) for the workflow, code generation and releases.

## Support and license

Use [GitHub issues](https://github.com/geonodecom/sdk-python/issues) for SDK bugs and [Geonode support](https://geonode.com/contact) for account or API questions. Report vulnerabilities privately using [SECURITY.md](SECURITY.md). Released changes are listed in [CHANGELOG.md](CHANGELOG.md).

[MIT license](LICENSE) · Copyright 2026 Geonode Team.

**[Try Geonode for free](https://app.geonode.com/sign-up)**
