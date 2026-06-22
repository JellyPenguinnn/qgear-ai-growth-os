from __future__ import annotations

from dataclasses import asdict

from qgear_ingest.providers.base import (
    BenchmarkSnapshot,
    DataMode,
    FilingMetadata,
    PriceSnapshot,
    ProviderName,
    ProviderResponse,
)


DEMO_SOURCE_DATE = "2026-06-22"


DEMO_FILING_ROWS: tuple[FilingMetadata, ...] = (
    FilingMetadata(
        accession_number="0001045810-26-000001",
        form="10-Q",
        filing_date="2026-05-22",
        report_date="2026-04-30",
        primary_document="nvda-20260430.htm",
        source_url="local://demo/sec/submissions/0001045810",
    ),
    FilingMetadata(
        accession_number="0001045810-26-000002",
        form="8-K",
        filing_date="2026-05-22",
        report_date="2026-05-21",
        primary_document="nvda-20260522x8k.htm",
        source_url="local://demo/sec/submissions/0001045810",
    ),
)


DEMO_PRICES: dict[str, PriceSnapshot] = {
    "NVDA": PriceSnapshot("NVDA", DEMO_SOURCE_DATE, 142.1, 145.3, 140.8, 144.5, 144.5, 182_000_000),
    "AMD": PriceSnapshot("AMD", DEMO_SOURCE_DATE, 163.2, 166.4, 160.1, 164.8, 164.8, 55_000_000),
    "MU": PriceSnapshot("MU", DEMO_SOURCE_DATE, 129.4, 133.2, 128.9, 132.6, 132.6, 31_000_000),
    "SPY": PriceSnapshot("SPY", DEMO_SOURCE_DATE, 640.0, 644.2, 638.4, 642.1, 642.1, 72_000_000),
    "QQQ": PriceSnapshot("QQQ", DEMO_SOURCE_DATE, 565.2, 570.7, 562.8, 568.9, 568.9, 49_000_000),
    "XLK": PriceSnapshot("XLK", DEMO_SOURCE_DATE, 250.4, 253.1, 249.8, 252.4, 252.4, 8_000_000),
    "SMH": PriceSnapshot("SMH", DEMO_SOURCE_DATE, 290.0, 296.2, 288.7, 294.9, 294.9, 12_000_000),
}


DEMO_BENCHMARKS: dict[str, BenchmarkSnapshot] = {
    "SPY": BenchmarkSnapshot("SPY", DEMO_SOURCE_DATE, 642.1, 642.1),
    "QQQ": BenchmarkSnapshot("QQQ", DEMO_SOURCE_DATE, 568.9, 568.9),
    "XLK": BenchmarkSnapshot("XLK", DEMO_SOURCE_DATE, 252.4, 252.4),
    "SMH": BenchmarkSnapshot("SMH", DEMO_SOURCE_DATE, 294.9, 294.9),
}


class MockProvider:
    def company_facts(self, cik: str) -> ProviderResponse:
        return ProviderResponse.ok(
            provider=ProviderName.MOCK,
            payload={"cik": cik, "mode": "demo", "message": "Mock company facts are used until live providers are configured."},
            source_url="local://demo/company-facts",
            source_name="Q-GEAR demo company facts",
            cached=True,
            source_date=DEMO_SOURCE_DATE,
            as_of_date=DEMO_SOURCE_DATE,
            cache_key=f"mock_company_facts_{cik}",
            mode=DataMode.DEMO,
        )

    def submissions(self, cik: str) -> ProviderResponse:
        return ProviderResponse.ok(
            provider=ProviderName.MOCK,
            payload={
                "cik": cik,
                "mode": "demo",
                "filings": {"recent": [asdict(row) for row in DEMO_FILING_ROWS]},
            },
            source_url="local://demo/sec/submissions",
            source_name="Q-GEAR demo SEC submissions",
            cached=True,
            source_date=DEMO_SOURCE_DATE,
            as_of_date=DEMO_SOURCE_DATE,
            cache_key=f"mock_submissions_{cik}",
            mode=DataMode.DEMO,
        )

    def filing_metadata(self, cik: str, *, limit: int = 20) -> ProviderResponse:
        rows = DEMO_FILING_ROWS[:limit]
        return ProviderResponse.ok(
            provider=ProviderName.MOCK,
            payload={"cik": cik, "filings": [asdict(row) for row in rows]},
            source_url="local://demo/sec/filings",
            source_name="Q-GEAR demo filing metadata",
            cached=True,
            source_date=DEMO_SOURCE_DATE,
            as_of_date=DEMO_SOURCE_DATE,
            cache_key=f"mock_filing_metadata_{cik}_{limit}",
            mode=DataMode.DEMO,
        )

    def daily_prices(self, tickers: tuple[str, ...]) -> ProviderResponse:
        normalized = tuple(ticker.upper() for ticker in tickers)
        snapshots = []
        missing = []
        for ticker in normalized:
            snapshot = DEMO_PRICES.get(ticker)
            if snapshot:
                snapshots.append(asdict(snapshot))
            else:
                missing.append(ticker)
        return ProviderResponse.ok(
            provider=ProviderName.MOCK,
            payload={"prices": snapshots, "missing": missing},
            source_url="local://demo/prices",
            source_name="Q-GEAR demo price snapshots",
            cached=True,
            source_date=DEMO_SOURCE_DATE,
            as_of_date=DEMO_SOURCE_DATE,
            cache_key="mock_daily_prices_" + "_".join(normalized),
            mode=DataMode.DEMO,
        )

    def benchmark_snapshots(self, benchmarks: tuple[str, ...]) -> ProviderResponse:
        normalized = tuple(benchmark.upper() for benchmark in benchmarks)
        snapshots = []
        missing = []
        for benchmark in normalized:
            snapshot = DEMO_BENCHMARKS.get(benchmark)
            if snapshot:
                snapshots.append(asdict(snapshot))
            else:
                missing.append(benchmark)
        return ProviderResponse.ok(
            provider=ProviderName.MOCK,
            payload={"benchmarks": snapshots, "missing": missing},
            source_url="local://demo/benchmarks",
            source_name="Q-GEAR demo benchmark snapshots",
            cached=True,
            source_date=DEMO_SOURCE_DATE,
            as_of_date=DEMO_SOURCE_DATE,
            cache_key="mock_benchmarks_" + "_".join(normalized),
            mode=DataMode.DEMO,
        )

    def series(self, series_id: str) -> ProviderResponse:
        return ProviderResponse.ok(
            provider=ProviderName.MOCK,
            payload={"series_id": series_id, "mode": "demo", "observations": []},
            source_url="local://demo/macro-series",
            source_name="Q-GEAR demo macro series",
            cached=True,
            source_date=DEMO_SOURCE_DATE,
            as_of_date=DEMO_SOURCE_DATE,
            cache_key=f"mock_macro_{series_id}",
            mode=DataMode.DEMO,
        )
