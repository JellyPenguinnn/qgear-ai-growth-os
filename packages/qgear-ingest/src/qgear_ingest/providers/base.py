from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from enum import Enum
from typing import Any, Protocol


class ProviderName(str, Enum):
    MOCK = "mock"
    SEC_EDGAR = "sec_edgar"
    FRED = "fred"
    EIA = "eia"
    ALPHA_VANTAGE = "alpha_vantage"
    FINANCIAL_MODELING_PREP = "financial_modeling_prep"
    FINNHUB = "finnhub"
    NASDAQ_DATA_LINK = "nasdaq_data_link"
    YFINANCE_EXPERIMENTAL = "yfinance_experimental"


class ProviderStatus(str, Enum):
    OK = "ok"
    NOT_CONFIGURED = "not_configured"
    MISSING_API_KEY = "missing_api_key"
    UNAVAILABLE = "unavailable"
    NOT_IMPLEMENTED = "not_implemented"
    ERROR = "error"


class DataMode(str, Enum):
    DEMO = "demo"
    LIVE = "live"


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


@dataclass(frozen=True)
class ProviderMetadata:
    provider: ProviderName
    status: ProviderStatus
    source_url: str
    source_name: str
    retrieved_at: str
    cached: bool = False
    source_date: str | None = None
    as_of_date: str | None = None
    cache_written_at: str | None = None
    cache_key: str | None = None
    error: str | None = None
    mode: DataMode | None = None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ProviderResponse:
    payload: dict
    metadata: ProviderMetadata

    @property
    def provider(self) -> ProviderName:
        return self.metadata.provider

    @property
    def source_url(self) -> str:
        return self.metadata.source_url

    @property
    def cached(self) -> bool:
        return self.metadata.cached

    @property
    def status(self) -> ProviderStatus:
        return self.metadata.status

    @classmethod
    def ok(
        cls,
        *,
        provider: ProviderName,
        payload: dict,
        source_url: str,
        source_name: str,
        cached: bool = False,
        source_date: str | None = None,
        as_of_date: str | None = None,
        cache_written_at: str | None = None,
        cache_key: str | None = None,
        mode: DataMode | None = None,
        retrieved_at: str | None = None,
    ) -> "ProviderResponse":
        return cls(
            payload=payload,
            metadata=ProviderMetadata(
                provider=provider,
                status=ProviderStatus.OK,
                source_url=source_url,
                source_name=source_name,
                retrieved_at=retrieved_at or utc_now_iso(),
                cached=cached,
                source_date=source_date,
                as_of_date=as_of_date,
                cache_written_at=cache_written_at,
                cache_key=cache_key,
                mode=mode,
            ),
        )

    @classmethod
    def unavailable(
        cls,
        *,
        provider: ProviderName,
        source_url: str,
        source_name: str,
        error: str,
        status: ProviderStatus = ProviderStatus.ERROR,
        payload: dict | None = None,
        mode: DataMode | None = None,
        retrieved_at: str | None = None,
    ) -> "ProviderResponse":
        return cls(
            payload=payload or {},
            metadata=ProviderMetadata(
                provider=provider,
                status=status,
                source_url=source_url,
                source_name=source_name,
                retrieved_at=retrieved_at or utc_now_iso(),
                cached=False,
                error=error,
                mode=mode,
            ),
        )


@dataclass(frozen=True)
class FilingMetadata:
    accession_number: str
    form: str
    filing_date: str
    report_date: str | None
    primary_document: str
    source_url: str


@dataclass(frozen=True)
class PriceSnapshot:
    ticker: str
    snapshot_date: str
    open: float
    high: float
    low: float
    close: float
    adjusted_close: float
    volume: int
    source: str = "mock"


@dataclass(frozen=True)
class BenchmarkSnapshot:
    benchmark: str
    snapshot_date: str
    close: float
    total_return_index: float | None
    source: str = "mock"


class CompanyFactsProvider(Protocol):
    def company_facts(self, cik: str) -> ProviderResponse:
        ...


class FilingsProvider(Protocol):
    def submissions(self, cik: str) -> ProviderResponse:
        ...

    def filing_metadata(self, cik: str, *, limit: int = 20) -> ProviderResponse:
        ...


class PriceProvider(Protocol):
    def daily_prices(self, tickers: tuple[str, ...]) -> ProviderResponse:
        ...


class BenchmarkProvider(Protocol):
    def benchmark_snapshots(self, benchmarks: tuple[str, ...]) -> ProviderResponse:
        ...


class MacroProvider(Protocol):
    def series(self, series_id: str) -> ProviderResponse:
        ...
