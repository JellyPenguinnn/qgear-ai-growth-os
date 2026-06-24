from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from qgear_ingest.providers.base import DataMode, ProviderName, ProviderResponse, ProviderStatus
from qgear_ingest.providers.macro import EiaProvider, EiaProviderConfig, FredProvider, FredProviderConfig
from qgear_ingest.providers.mock import MockProvider
from qgear_ingest.providers.prices import AlphaVantagePriceProvider, AlphaVantagePriceProviderConfig
from qgear_ingest.providers.sec_edgar import SecEdgarProvider


@dataclass(frozen=True)
class ProviderConfig:
    mode: DataMode = DataMode.DEMO
    cache_dir: Path = Path("data/cache")
    sec_user_agent: str = "qgear-ai-growth-os personal research app contact@example.com"
    sec_max_requests_per_second: int = 10
    price_provider: str = "mock"
    alpha_vantage_api_key: str | None = None
    fred_api_key: str | None = None
    eia_api_key: str | None = None


class UnavailableSecProvider:
    def __init__(self, error: str) -> None:
        self.error = error

    def company_facts(self, cik: str) -> ProviderResponse:
        return self._response("company facts", f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik.zfill(10)}.json")

    def submissions(self, cik: str) -> ProviderResponse:
        return self._response("submissions", f"https://data.sec.gov/submissions/CIK{cik.zfill(10)}.json")

    def filing_metadata(self, cik: str, *, limit: int = 20) -> ProviderResponse:
        return self._response("filing metadata", f"https://data.sec.gov/submissions/CIK{cik.zfill(10)}.json")

    def _response(self, source_name: str, source_url: str) -> ProviderResponse:
        return ProviderResponse.unavailable(
            provider=ProviderName.SEC_EDGAR,
            source_url=source_url,
            source_name=f"SEC EDGAR {source_name}",
            error=self.error,
            status=ProviderStatus.NOT_CONFIGURED,
            mode=DataMode.LIVE,
        )


@dataclass(frozen=True)
class ProviderBundle:
    mode: DataMode
    company_facts_provider: object
    filings_provider: object
    price_provider: object
    price_history_provider: object
    benchmark_provider: object
    fred_provider: object
    eia_provider: object

    def status_payload(self) -> dict:
        return {
            "mode": self.mode.value,
            "live_network_required_for_tests": False,
            "providers": {
                "company_facts": type(self.company_facts_provider).__name__,
                "filings": type(self.filings_provider).__name__,
                "prices": type(self.price_provider).__name__,
                "price_history": type(self.price_history_provider).__name__,
                "benchmarks": type(self.benchmark_provider).__name__,
                "fred": type(self.fred_provider).__name__,
                "eia": type(self.eia_provider).__name__,
            },
            "safety": {
                "auto_trading": "disabled",
                "margin": "disabled",
                "options": "disabled_in_mvp",
                "live_data_is_optional": True,
            },
        }


def build_provider_bundle(config: ProviderConfig) -> ProviderBundle:
    mock = MockProvider()
    if config.mode == DataMode.DEMO:
        sec_provider: object = mock
    else:
        try:
            sec_provider = SecEdgarProvider(
                user_agent=config.sec_user_agent,
                cache_dir=config.cache_dir / "sec",
                max_requests_per_second=config.sec_max_requests_per_second,
            )
        except ValueError as exc:
            sec_provider = UnavailableSecProvider(str(exc))
    price_provider: object
    if config.mode == DataMode.LIVE and config.price_provider == "alpha_vantage":
        price_provider = AlphaVantagePriceProvider(AlphaVantagePriceProviderConfig(api_key=config.alpha_vantage_api_key))
    else:
        price_provider = mock

    return ProviderBundle(
        mode=config.mode,
        company_facts_provider=sec_provider,
        filings_provider=sec_provider,
        price_provider=price_provider,
        price_history_provider=price_provider,
        benchmark_provider=mock,
        fred_provider=FredProvider(FredProviderConfig(api_key=config.fred_api_key)),
        eia_provider=EiaProvider(EiaProviderConfig(api_key=config.eia_api_key)),
    )
