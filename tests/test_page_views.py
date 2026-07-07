import unittest
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.page_views import aggregate_page_views, iter_report_rows, write_snapshot


class AggregatePageViewsTests(unittest.TestCase):
    def test_combines_canonical_variants_for_the_same_page(self):
        rows = [
            ("jxnl.co", "/writing/2026/06/28/example/", 10),
            ("www.jxnl.co", "/writing/2026/06/28/example/index.html", 4),
            ("jxnl.co", "/writing/2026/06/28/example?ref=twitter", 2),
            ("jxnl.github.io", "/blog/writing/2026/06/28/example/", 8),
        ]

        self.assertEqual(
            aggregate_page_views(rows),
            {"/writing/2026/06/28/example/": 24},
        )

    def test_excludes_other_hosts_and_non_post_paths(self):
        rows = [
            ("example.com", "/writing/2026/06/28/example/", 100),
            ("jxnl.co", "/services/", 20),
            ("jxnl.co", "/writing/", 10),
            ("jxnl.co", "/writing/2026/06/28/example/", 5),
        ]

        self.assertEqual(
            aggregate_page_views(rows),
            {"/writing/2026/06/28/example/": 5},
        )


class IterReportRowsTests(unittest.TestCase):
    def test_reads_all_pages_until_report_row_count_is_reached(self):
        class Response:
            def __init__(self, rows, row_count):
                self.rows = rows
                self.row_count = row_count

        class Client:
            def __init__(self):
                self.requests = []
                self.responses = [
                    Response(["first", "second"], 4),
                    Response(["third", "fourth"], 4),
                ]

            def run_report(self, request):
                self.requests.append(request)
                return self.responses.pop(0)

        client = Client()

        rows = list(
            iter_report_rows(
                client,
                lambda offset, limit: {"offset": offset, "limit": limit},
                limit=2,
            )
        )

        self.assertEqual(rows, ["first", "second", "third", "fourth"])
        self.assertEqual(
            client.requests,
            [{"offset": 0, "limit": 2}, {"offset": 2, "limit": 2}],
        )


class WriteSnapshotTests(unittest.TestCase):
    def test_writes_a_sorted_static_asset(self):
        with TemporaryDirectory() as directory:
            output = Path(directory) / "assets" / "page-views.json"

            write_snapshot(
                output,
                {
                    "/writing/2026/06/29/later/": 3,
                    "/writing/2026/06/28/earlier/": 12,
                },
                generated_at="2026-07-01T08:00:00Z",
            )

            self.assertEqual(
                json.loads(output.read_text()),
                {
                    "generated_at": "2026-07-01T08:00:00Z",
                    "views": {
                        "/writing/2026/06/28/earlier/": 12,
                        "/writing/2026/06/29/later/": 3,
                    },
                },
            )


if __name__ == "__main__":
    unittest.main()
