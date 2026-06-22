from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

TMP = Path(tempfile.gettempdir()) / f"qgear_api_test_{os.getpid()}"
TMP.mkdir(parents=True, exist_ok=True)
os.environ["QGEAR_SQLITE_PATH"] = str(TMP / "qgear_test.db")
os.environ["QGEAR_DUCKDB_PATH"] = str(TMP / "qgear_test.duckdb")

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402


class ApiSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    def test_health_has_no_local_paths(self) -> None:
        payload = self.client.get("/health").json()

        self.assertEqual(payload["status"], "ok")
        self.assertNotIn("sqlite_path", payload)
        self.assertNotIn("path", str(payload.get("duckdb", "")))

    def test_core_routes_return_success(self) -> None:
        for path in (
            "/universe",
            "/portfolio",
            "/earnings",
            "/alerts",
            "/reports/weekly",
            "/reports/monthly",
            "/reports/quarterly",
            "/reports/annual",
            "/providers/status",
            "/valuation/backtest/demo",
        ):
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)

    def test_universe_has_seed_count(self) -> None:
        payload = self.client.get("/universe").json()

        self.assertEqual(payload["count"], 34)
        self.assertIn("total", payload["companies"][0]["score"])

    def test_unknown_portfolio_ticker_rejected(self) -> None:
        response = self.client.post(
            "/portfolio/positions",
            json={
                "ticker": "NOPE",
                "shares": 1,
                "average_cost": 10,
                "current_price": 10,
                "status": "HOLD",
                "thesis_status": "DRAFT",
                "next_review_date": "2026-09-30",
            },
        )

        self.assertEqual(response.status_code, 404)

    def test_negative_position_rejected_by_schema(self) -> None:
        response = self.client.post(
            "/portfolio/positions",
            json={
                "ticker": "NVDA",
                "shares": -1,
                "average_cost": 10,
                "current_price": 10,
                "status": "HOLD",
                "thesis_status": "DRAFT",
                "next_review_date": "2026-09-30",
            },
        )

        self.assertEqual(response.status_code, 422)

    def test_provider_metadata_routes_are_demo_safe(self) -> None:
        status = self.client.get("/providers/status").json()
        prices = self.client.get("/providers/prices?tickers=NVDA,NOPE").json()
        benchmarks = self.client.get("/providers/benchmarks").json()
        filings = self.client.get("/providers/filings/1045810?limit=1").json()

        self.assertEqual(status["mode"], "demo")
        self.assertFalse(status["live_network_required_for_tests"])
        self.assertEqual(prices["metadata"]["status"], "ok")
        self.assertEqual(prices["metadata"]["mode"], "demo")
        self.assertEqual(prices["payload"]["missing"], ["NOPE"])
        self.assertEqual(len(benchmarks["payload"]["benchmarks"]), 4)
        self.assertEqual(filings["payload"]["filings"][0]["form"], "10-Q")

    def test_provider_cik_validation(self) -> None:
        response = self.client.get("/providers/company-facts/not-a-cik")

        self.assertEqual(response.status_code, 422)

    def test_earnings_evidence_and_review_round_trip(self) -> None:
        evidence_payload = {
            "claim": "AI demand became more measurable after earnings.",
            "evidence": "Revenue growth accelerated, guidance was raised, and margins expanded.",
            "source": "Q-GEAR API smoke fixture",
            "source_date": "2026-06-22",
            "confidence": "HIGH",
            "disproves_if": "Guidance is cut, AI demand slows, or margins deteriorate.",
        }
        evidence_response = self.client.post("/earnings/NVDA/evidence", json=evidence_payload)
        review_response = self.client.post(
            "/earnings/NVDA/reviews",
            json={
                "fiscal_period": "2026Q1",
                "report_date": "2026-06-22",
                "revenue_surprise_pct": 8,
                "eps_surprise_pct": 6,
                "guidance_raised": True,
                "revenue_growth_accelerated": True,
                "ai_evidence_improved": True,
                "margin_expanded": True,
                "fcf_improved": True,
                "management_tone": "constructive but evidence-gated",
                "score_change": 4,
                "action_change": "NO_ACTION",
                "evidence": [evidence_payload],
            },
        )
        stored = self.client.get("/earnings/NVDA").json()

        self.assertEqual(evidence_response.status_code, 200)
        self.assertEqual(review_response.status_code, 200)
        self.assertEqual(review_response.json()["thesis_status_change"], "STRENGTHENED")
        self.assertGreaterEqual(len(stored["stored_evidence"]), 2)
        self.assertGreaterEqual(len(stored["stored_reviews"]), 1)

    def test_earnings_evidence_requires_iso_source_date(self) -> None:
        response = self.client.post(
            "/earnings/NVDA/evidence",
            json={
                "claim": "AI demand became more measurable after earnings.",
                "evidence": "Revenue growth accelerated, guidance was raised, and margins expanded.",
                "source": "Q-GEAR API smoke fixture",
                "source_date": "June 22, 2026",
                "confidence": "HIGH",
                "disproves_if": "Guidance is cut, AI demand slows, or margins deteriorate.",
            },
        )

        self.assertEqual(response.status_code, 422)

    def test_valuation_hurdle_blocks_expensive_demo_company(self) -> None:
        response = self.client.get("/valuation/PLTR")

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["decision_gate"]["valuation_clears_hurdle"])

    def test_alerts_are_review_prompts_not_trade_instructions(self) -> None:
        payload = self.client.get("/alerts").json()

        self.assertIn("STALE_EVIDENCE", payload["rules"])
        self.assertGreater(len(payload["alerts"]), 0)
        self.assertTrue(all(alert["trade_instruction"] is False for alert in payload["alerts"]))
        self.assertTrue(any(alert["type"] == "TECHNICAL_BREAK" for alert in payload["alerts"]))

    def test_journal_analytics_and_review_reports(self) -> None:
        journal_response = self.client.post(
            "/journal",
            json={
                "entry_date": "2026-06-22",
                "ticker": "NVDA",
                "action": "NO_ACTION",
                "price": 110,
                "position_size_pct": 0,
                "score": 90,
                "evidence": "No fresh positive action-changing evidence today.",
                "thesis": "Approved thesis remains under review.",
                "invalidation_rule": "Guidance cut or margin deterioration would weaken thesis.",
                "expected_irr_pct": 16,
                "future_review_date": "2026-09-30",
                "later_outcome": "",
            },
        )
        analytics = self.client.get("/journal/analytics").json()
        monthly = self.client.get("/reports/monthly").json()
        annual = self.client.get("/reports/annual").json()

        self.assertEqual(journal_response.status_code, 200)
        self.assertGreaterEqual(analytics["entry_count"], 1)
        self.assertGreaterEqual(analytics["action_counts"]["NO_ACTION"], 1)
        self.assertGreaterEqual(monthly["journal_analytics"]["evidence_backed_count"], 1)
        self.assertIn("benchmark_policy", annual)
        self.assertIn("THESIS_REVIEW_DUE", annual["alert_rules"])


if __name__ == "__main__":
    unittest.main()
