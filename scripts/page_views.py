"""Build-time Google Analytics page-view snapshot support."""

from collections import defaultdict
from datetime import datetime, timezone
import json
import logging
import os
from pathlib import Path
import re
from typing import Callable, Iterable, Iterator, Mapping, Optional, Tuple
from urllib.parse import urlsplit


PageViewRow = Tuple[str, str, int]
POST_PATH = re.compile(r"^/writing/\d{4}/\d{2}/\d{2}/[^/]+/$")
ANALYTICS_READ_SCOPE = "https://www.googleapis.com/auth/analytics.readonly"
REPORT_ROW_LIMIT = 250_000
LOGGER = logging.getLogger("mkdocs.hooks.page_views")


def normalize_path(path: str) -> str:
    """Return the canonical public path used by the MkDocs site."""
    normalized = urlsplit(path).path or "/"
    if normalized.endswith("/index.html"):
        normalized = normalized[: -len("index.html")]
    if not normalized.startswith("/"):
        normalized = f"/{normalized}"
    if normalized != "/" and not normalized.endswith("/"):
        normalized = f"{normalized}/"
    return normalized


def aggregate_page_views(
    rows: Iterable[PageViewRow],
    allowed_hosts: Iterable[str] = (
        "jxnl.co",
        "www.jxnl.co",
        "jxnl.github.io",
    ),
) -> Mapping[str, int]:
    """Combine current and historical GA page-view rows into canonical totals."""
    hosts = set(allowed_hosts)
    totals: defaultdict[str, int] = defaultdict(int)
    for host, path, views in rows:
        normalized = normalize_path(path)
        if host == "jxnl.github.io" and normalized.startswith("/blog/"):
            normalized = normalized[len("/blog") :]
        if host in hosts and POST_PATH.fullmatch(normalized):
            totals[normalized] += int(views)
    return dict(sorted(totals.items()))


def write_snapshot(
    destination: Path,
    views: Mapping[str, int],
    generated_at: Optional[str],
) -> None:
    """Write the public, static page-view asset consumed by the browser."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at": generated_at,
        "views": dict(sorted(views.items())),
    }
    destination.write_text(f"{json.dumps(payload, indent=2)}\n")


def iter_report_rows(
    client,
    make_request: Callable[[int, int], object],
    limit: int = REPORT_ROW_LIMIT,
) -> Iterator[object]:
    """Yield every row from a potentially paginated GA Data API report."""
    offset = 0
    while True:
        response = client.run_report(make_request(offset, limit))
        rows = tuple(response.rows)
        yield from rows

        offset += len(rows)
        row_count = getattr(response, "row_count", 0)
        if not rows or len(rows) < limit or (row_count and offset >= row_count):
            break


def fetch_page_views(
    property_id: str,
    service_account_json: str,
) -> Mapping[str, int]:
    """Fetch and aggregate all-time blog-post views from the GA4 Data API."""
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import (
        DateRange,
        Dimension,
        Metric,
        RunReportRequest,
    )
    from google.oauth2 import service_account

    credentials = service_account.Credentials.from_service_account_info(
        json.loads(service_account_json),
        scopes=[ANALYTICS_READ_SCOPE],
    )
    client = BetaAnalyticsDataClient(credentials=credentials)

    def make_request(offset: int, limit: int) -> RunReportRequest:
        return RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name="hostName"), Dimension(name="pagePath")],
            metrics=[Metric(name="screenPageViews")],
            date_ranges=[DateRange(start_date="2015-08-14", end_date="yesterday")],
            limit=limit,
            offset=offset,
        )

    rows = (
        (
            row.dimension_values[0].value,
            row.dimension_values[1].value,
            int(row.metric_values[0].value),
        )
        for row in iter_report_rows(client, make_request)
    )
    return aggregate_page_views(rows)


def on_post_build(config, **_kwargs) -> None:
    """MkDocs hook: add the analytics snapshot to the finished static site."""
    destination = Path(config.site_dir) / "assets" / "page-views.json"
    property_id = os.getenv("GA_PROPERTY_ID")
    service_account_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")

    if not property_id and not service_account_json:
        LOGGER.info("GA credentials are not configured; writing an empty view snapshot")
        write_snapshot(destination, {}, generated_at=None)
        return

    if not property_id or not service_account_json:
        raise RuntimeError(
            "GA_PROPERTY_ID and GOOGLE_SERVICE_ACCOUNT_JSON must be configured together"
        )

    views = fetch_page_views(property_id, service_account_json)
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    write_snapshot(destination, views, generated_at=generated_at.replace("+00:00", "Z"))
    LOGGER.info("Wrote page-view counts for %s blog posts", len(views))
