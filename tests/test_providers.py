from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from qgear_ingest.providers.base import DataMode, ProviderStatus
from qgear_ingest.providers.factory import ProviderConfig, build_provider_bundle
from qgear_ingest.providers.mock import MockProvider
from qgear_ingest.providers.sec_edgar import SecEdgarProvider


FIXTURES = Path(__file__).parent / "fixtures" / "sec"


class ProviderTests(unittest.TestCase):
    def test_mock_prices_and_benchmarks_include_metadata(self) -> None:
        provider = MockProvider()

        prices = provider.daily_prices(("NVDA", "MISSING"))
        benchmarks = provider.benchmark_snapshots(("SPY", "QQQ", "XLK", "SMH"))

        self.assertEqual(prices.status, ProviderStatus.OK)
        self.assertEqual(prices.metadata.mode, DataMode.DEMO)
        self.assertTrue(prices.cached)
        self.assertEqual(prices.payload["prices"][0]["ticker"], "NVDA")
        self.assertEqual(prices.payload["missing"], ["MISSING"])
        self.assertEqual(len(benchmarks.payload["benchmarks"]), 4)
        self.assertEqual(benchmarks.metadata.source_name, "Q-GEAR demo benchmark snapshots")

    def test_factory_routes_demo_mode_to_mock_providers(self) -> None:
        bundle = build_provider_bundle(ProviderConfig(mode=DataMode.DEMO))

        status = bundle.status_payload()
        response = bundle.company_facts_provider.company_facts("1045810")

        self.assertEqual(status["mode"], "demo")
        self.assertEqual(status["providers"]["company_facts"], "MockProvider")
        self.assertEqual(response.metadata.provider.value, "mock")

    def test_sec_requires_custom_user_agent_with_contact(self) -> None:
        with self.assertRaises(ValueError):
            SecEdgarProvider(user_agent="qgear", cache_dir=Path(tempfile.gettempdir()) / "qgear_bad_sec")

    def test_sec_submissions_cache_hit_and_filing_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cache_dir = Path(tmp)
            shutil.copyfile(
                FIXTURES / "sec_submissions_0001045810.json",
                cache_dir / "sec_submissions_0001045810.json",
            )
            provider = SecEdgarProvider(
                user_agent="qgear-ai-growth-os test contact@example.com",
                cache_dir=cache_dir,
                max_requests_per_second=50,
            )

            submissions = provider.submissions("1045810")
            filings = provider.filing_metadata("1045810", limit=1)

            self.assertEqual(submissions.status, ProviderStatus.OK)
            self.assertTrue(submissions.cached)
            self.assertEqual(submissions.metadata.source_date, "2026-05-22")
            self.assertEqual(filings.payload["filings"][0]["form"], "10-Q")
            self.assertIn("Archives/edgar/data/1045810", filings.payload["filings"][0]["source_url"])
            self.assertLessEqual(provider.max_requests_per_second, 10)

    def test_sec_malformed_cache_returns_error_response(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cache_dir = Path(tmp)
            (cache_dir / "sec_companyfacts_0001045810.json").write_text("{not json", encoding="utf-8")
            provider = SecEdgarProvider(
                user_agent="qgear-ai-growth-os test contact@example.com",
                cache_dir=cache_dir,
            )

            response = provider.company_facts("1045810")

            self.assertEqual(response.status, ProviderStatus.ERROR)
            self.assertIn("cache read failed", response.metadata.error or "")


if __name__ == "__main__":
    unittest.main()
