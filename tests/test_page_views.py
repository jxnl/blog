import unittest
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.page_views import aggregate_page_views, write_snapshot


class AggregatePageViewsTests(unittest.TestCase):
    def test_combines_canonical_variants_for_the_same_page(self):
        rows = [
            ("jxnl.co", "/writing/2026/06/28/example/", 10),
            ("www.jxnl.co", "/writing/2026/06/28/example/index.html", 4),
            ("jxnl.co", "/writing/2026/06/28/example?ref=twitter", 2),
        ]

        self.assertEqual(
            aggregate_page_views(rows),
            {"/writing/2026/06/28/example/": 16},
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
