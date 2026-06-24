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
            "/today",
            "/pipeline",
            "/ai/status",
            "/portfolio",
            "/earnings",
            "/alerts",
            "/reports/weekly",
            "/reports/monthly",
            "/reports/quarterly",
            "/reports/annual",
            "/providers/status",
            "/financials/NVDA",
            "/financials/NVDA/metrics",
            "/prices/NVDA",
            "/technical/NVDA",
            "/data/quality/NVDA",
            "/data/health",
            "/macro/status",
            "/macro/fred/FEDFUNDS",
            "/energy/status",
            "/energy/eia/context",
            "/valuation/backtest/demo",
        ):
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)

    def test_universe_has_seed_count(self) -> None:
        payload = self.client.get("/universe").json()

        self.assertEqual(payload["count"], 34)
        self.assertIn("total", payload["companies"][0]["score"])

    def test_today_is_review_only_with_pipeline_context(self) -> None:
        payload = self.client.get("/today").json()

        self.assertEqual(payload["mode"], "demo")
        self.assertTrue(payload["not_trade_instructions"])
        self.assertIn("No action justified today", payload["default_stance"])
        self.assertGreater(payload["metrics"]["review_queue_count"], 0)
        self.assertGreater(payload["metrics"]["blocked_count"], 0)
        self.assertTrue(all(item["trade_instruction"] is False for item in payload["review_queue"]))
        self.assertTrue(all(alert["trade_instruction"] is False for alert in payload["alerts"]))

    def test_pipeline_exposes_state_reasons_and_source_metadata(self) -> None:
        payload = self.client.get("/pipeline").json()
        states = {state["state"]: state for state in payload["states"]}
        queue_item = payload["review_queue"][0]

        self.assertTrue(payload["not_trade_instructions"])
        self.assertEqual(payload["summary"]["total"], 34)
        self.assertIn("WATCHLIST", states)
        self.assertIn("STARTER_ALLOWED", states)
        self.assertIn("ADD_ALLOWED", states)
        self.assertEqual(queue_item["trade_instruction"], False)
        self.assertIn("primary_reason", queue_item)
        self.assertIn("next_task", queue_item)
        self.assertIn("source", queue_item["source_metadata"])
        self.assertIn("source_date", queue_item["source_metadata"])
        self.assertIn("confidence", queue_item["source_metadata"])
        self.assertIn("disproves_if", queue_item["source_metadata"])

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

    def test_portfolio_intelligence_fields_are_review_only(self) -> None:
        self.client.post(
            "/portfolio/positions",
            json={
                "ticker": "ANET",
                "shares": 10,
                "average_cost": 90,
                "current_price": 100,
                "status": "HOLD",
                "thesis_status": "APPROVED",
                "next_review_date": "2026-09-30",
            },
        )
        payload = self.client.get("/portfolio").json()

        self.assertTrue(payload["manual_only"])
        self.assertIn("cash_pct", payload)
        self.assertIn("expected_irr_distribution", payload)
        self.assertIn("benchmark_comparison", payload)
        self.assertIn("concentration_risks", payload)
        self.assertIn("blocked_adds", payload)
        self.assertIn("review_calendar", payload)
        self.assertTrue(all(item["trade_instruction"] is False for item in payload["concentration_risks"]))
        self.assertTrue(all(item["trade_instruction"] is False for item in payload["review_calendar"]))
        self.assertEqual(len(payload["benchmark_comparison"]), 4)

    def test_provider_metadata_routes_are_demo_safe(self) -> None:
        status = self.client.get("/providers/status").json()
        prices = self.client.get("/providers/prices?tickers=NVDA,NOPE").json()
        benchmarks = self.client.get("/providers/benchmarks").json()
        filings = self.client.get("/providers/filings/1045810?limit=1").json()

        self.assertEqual(status["mode"], "demo")
        self.assertFalse(status["live_network_required_for_tests"])
        self.assertEqual(status["ai"]["provider_metadata"]["mode"], "none")
        self.assertFalse(status["ai"]["ai_enabled"])
        self.assertEqual(prices["metadata"]["status"], "ok")
        self.assertEqual(prices["metadata"]["mode"], "demo")
        self.assertEqual(prices["payload"]["missing"], ["NOPE"])
        self.assertEqual(len(benchmarks["payload"]["benchmarks"]), 4)
        self.assertEqual(filings["payload"]["filings"][0]["form"], "10-Q")

    def test_provider_cik_validation(self) -> None:
        response = self.client.get("/providers/company-facts/not-a-cik")

        self.assertEqual(response.status_code, 422)

    def test_financials_and_data_quality_routes_are_review_only(self) -> None:
        financials = self.client.get("/financials/NVDA").json()
        metrics = self.client.get("/financials/NVDA/metrics").json()
        prices = self.client.get("/prices/NVDA").json()
        technical = self.client.get("/technical/NVDA").json()
        quality = self.client.get("/data/quality/NVDA").json()
        missing = self.client.get("/data/quality/NOPE").json()
        health = self.client.get("/data/health").json()
        sec_refresh = self.client.post("/providers/sec/refresh/NVDA").json()
        price_refresh = self.client.post("/providers/prices/refresh/NVDA").json()
        benchmark_refresh = self.client.post("/providers/benchmarks/refresh").json()
        macro = self.client.get("/macro/fred/FEDFUNDS").json()
        energy = self.client.get("/energy/eia/context").json()

        self.assertEqual(financials["status"], "ok")
        self.assertEqual(financials["snapshot"]["ticker"], "NVDA")
        self.assertEqual(financials["snapshot"]["source_metadata"]["mode"], "demo")
        self.assertEqual(metrics["metrics"]["revenue"], 44_062_000_000)
        self.assertEqual(metrics["metrics"]["free_cash_flow"], 25_900_000_000)
        self.assertTrue(metrics["not_trade_instruction"])
        self.assertEqual(prices["status"], "ok")
        self.assertEqual(len(prices["prices"]), 260)
        self.assertTrue(prices["not_trade_instruction"])
        self.assertEqual(technical["status"], "ok")
        self.assertEqual(technical["technical"]["technical_regime"], "SUPPORTIVE")
        self.assertTrue(technical["not_trade_instruction"])
        self.assertEqual(quality["status"], "ok")
        self.assertFalse(quality["can_support_action_in_live_mode"])
        self.assertTrue(quality["not_trade_instruction"])
        self.assertEqual(missing["status"], "missing_mapping")
        self.assertEqual(health["status"], "review_only")
        self.assertTrue(health["not_trade_instruction"])
        self.assertEqual(sec_refresh["status"], "ok")
        self.assertTrue(sec_refresh["explicit_refresh"])
        self.assertTrue(sec_refresh["not_trade_instruction"])
        self.assertEqual(price_refresh["status"], "ok")
        self.assertTrue(price_refresh["explicit_refresh"])
        self.assertTrue(price_refresh["not_trade_instruction"])
        self.assertEqual(benchmark_refresh["status"], "ok")
        self.assertTrue(benchmark_refresh["explicit_refresh"])
        self.assertTrue(benchmark_refresh["not_trade_instruction"])
        self.assertEqual(macro["status"], "missing_api_key")
        self.assertTrue(macro["review_only"])
        self.assertEqual(energy["status"], "missing_api_key")
        self.assertTrue(energy["review_only"])

    def test_ai_status_and_disabled_routes_are_draft_only(self) -> None:
        status = self.client.get("/ai/status").json()
        response = self.client.post(
            "/ai/evidence/extract",
            json={
                "ticker": "NVDA",
                "source_title": "Manual excerpt",
                "source_type": "earnings release",
                "source_date": "2026-06-22",
                "source_url_or_description": "User-pasted local excerpt",
                "pasted_text": "Revenue growth accelerated and guidance was raised in the supplied excerpt.",
                "external_ai_acknowledged": False,
            },
        ).json()
        earnings_response = self.client.post(
            "/ai/earnings/summarize",
            json={
                "ticker": "NVDA",
                "fiscal_period": "2026Q1",
                "report_date": "2026-06-22",
                "earnings_text": "Revenue growth accelerated, guidance was raised, and margins expanded in the supplied excerpt.",
                "existing_thesis": "AI demand remains measurable.",
                "external_ai_acknowledged": False,
            },
        ).json()

        self.assertFalse(status["ai_enabled"])
        self.assertTrue(status["draft_only"])
        self.assertFalse(status["mutates_decision_state"])
        self.assertEqual(response["draft_status"], "disabled")
        self.assertTrue(response["requires_user_verification"])
        self.assertFalse(response["mutates_decision_state"])
        self.assertFalse(response["provider_metadata"]["external_call_performed"])
        self.assertEqual(earnings_response["draft_status"], "disabled")
        self.assertFalse(earnings_response["mutates_decision_state"])

    def test_earnings_evidence_and_review_round_trip(self) -> None:
        evidence_payload = {
            "claim": "AI demand became more measurable after earnings.",
            "evidence": "Revenue growth accelerated, guidance was raised, and margins expanded.",
            "source": "Q-GEAR API smoke fixture",
            "source_date": "2026-06-22",
            "confidence": "HIGH",
            "disproves_if": "Guidance is cut, AI demand slows, or margins deteriorate.",
            "source_type": "EARNINGS_RELEASE",
            "verification_status": "USER_VERIFIED",
            "source_url": "local://tests/earnings/nvda",
            "retrieved_at": "2026-06-22T00:00:00+00:00",
            "provider": "manual",
            "accession_number": "manual-earnings-smoke",
            "filing_date": "2026-06-22",
            "period_end_date": "2026-04-30",
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
        detail = self.client.get("/universe/NVDA").json()

        self.assertEqual(evidence_response.status_code, 200)
        self.assertEqual(review_response.status_code, 200)
        self.assertEqual(evidence_response.json()["evidence"]["source_type"], "EARNINGS_RELEASE")
        self.assertEqual(evidence_response.json()["evidence"]["verification_status"], "USER_VERIFIED")
        self.assertEqual(evidence_response.json()["evidence"]["source_url"], "local://tests/earnings/nvda")
        self.assertEqual(review_response.json()["thesis_status_change"], "STRENGTHENED")
        self.assertGreaterEqual(len(stored["stored_evidence"]), 2)
        self.assertGreaterEqual(len(stored["stored_reviews"]), 1)
        self.assertTrue(
            any(item["claim"] == evidence_payload["claim"] for item in detail["evidence_table"])
        )
        self.assertTrue(
            any(
                item["claim"] == evidence_payload["claim"]
                and item["source_type"] == "EARNINGS_RELEASE"
                and item["verification_status"] == "USER_VERIFIED"
                for item in detail["evidence_table"]
            )
        )

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
        self.assertIn("sensitivity_table", response.json())
        self.assertIn("assumptions", response.json()["summary"]["cases"][0])
        self.assertFalse(response.json()["trade_instruction"])

    def test_valuation_calculate_validates_probabilities(self) -> None:
        cases = [
            {
                "name": "bear",
                "probability": 0.25,
                "current_price": 100,
                "target_price_3y": 120,
                "target_price_5y": 140,
                "notes": "Bear case with slower growth.",
                "assumptions": {
                    "revenue_cagr_pct": 10,
                    "gross_margin_pct": 55,
                    "operating_margin_pct": 25,
                    "fcf_margin_pct": 20,
                    "terminal_multiple": 18,
                    "dilution_buyback_pct": -1,
                    "net_cash_debt_per_share": 0,
                },
                "evidence_refs": ["Q-GEAR API smoke valuation fixture"],
            },
            {
                "name": "base",
                "probability": 0.50,
                "current_price": 100,
                "target_price_3y": 150,
                "target_price_5y": 210,
                "notes": "Base case with evidence-backed growth.",
                "assumptions": {
                    "revenue_cagr_pct": 18,
                    "gross_margin_pct": 60,
                    "operating_margin_pct": 32,
                    "fcf_margin_pct": 28,
                    "terminal_multiple": 25,
                    "dilution_buyback_pct": 0,
                    "net_cash_debt_per_share": 0,
                },
                "evidence_refs": ["Q-GEAR API smoke valuation fixture"],
            },
            {
                "name": "bull",
                "probability": 0.25,
                "current_price": 100,
                "target_price_3y": 190,
                "target_price_5y": 300,
                "notes": "Bull case with stronger margins.",
                "assumptions": {
                    "revenue_cagr_pct": 25,
                    "gross_margin_pct": 63,
                    "operating_margin_pct": 36,
                    "fcf_margin_pct": 32,
                    "terminal_multiple": 32,
                    "dilution_buyback_pct": 1,
                    "net_cash_debt_per_share": 0,
                },
                "evidence_refs": ["Q-GEAR API smoke valuation fixture"],
            },
        ]
        valid = self.client.post(
            "/valuation/NVDA/calculate",
            json={"ticker": "NVDA", "hurdle_irr_pct": 15, "cases": cases},
        )
        invalid_cases = [dict(item) for item in cases]
        invalid_cases[0] = {**invalid_cases[0], "probability": 0.30}
        invalid = self.client.post(
            "/valuation/NVDA/calculate",
            json={"ticker": "NVDA", "hurdle_irr_pct": 15, "cases": invalid_cases},
        )

        self.assertEqual(valid.status_code, 200)
        self.assertEqual(valid.json()["mode"], "user_draft")
        self.assertIn("probability_weighted_irr_5y_pct", valid.json()["summary"])
        self.assertEqual(invalid.status_code, 422)

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
                "decision_outcome": "PENDING",
                "mistake_category": "NONE",
                "evidence_quality": "HIGH",
                "followed_system": True,
                "later_review": "",
                "process_score": 92,
            },
        )
        analytics = self.client.get("/journal/analytics").json()
        monthly = self.client.get("/reports/monthly").json()
        annual = self.client.get("/reports/annual").json()

        self.assertEqual(journal_response.status_code, 200)
        self.assertGreaterEqual(analytics["entry_count"], 1)
        self.assertGreaterEqual(analytics["action_counts"]["NO_ACTION"], 1)
        self.assertIn("followed_system_rate_pct", analytics)
        self.assertIn("average_process_score", analytics)
        self.assertGreaterEqual(analytics["evidence_quality_counts"]["HIGH"], 1)
        self.assertGreaterEqual(analytics["mistake_counts"]["NONE"], 1)
        self.assertGreaterEqual(monthly["journal_analytics"]["evidence_backed_count"], 1)
        self.assertIn("blocked_adds", monthly)
        self.assertIn("review_calendar", monthly)
        self.assertIn("benchmark_policy", annual)
        self.assertIn("THESIS_REVIEW_DUE", annual["alert_rules"])


if __name__ == "__main__":
    unittest.main()
