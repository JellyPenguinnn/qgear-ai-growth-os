from __future__ import annotations

from dataclasses import dataclass

from qgear_ingest.providers.base import DataMode, ProviderName, ProviderResponse, ProviderStatus


@dataclass(frozen=True)
class FredProviderConfig:
    api_key: str | None


@dataclass(frozen=True)
class EiaProviderConfig:
    api_key: str | None


class FredProvider:
    def __init__(self, config: FredProviderConfig) -> None:
        self.config = config

    def series(self, series_id: str) -> ProviderResponse:
        if not self.config.api_key:
            return ProviderResponse.unavailable(
                provider=ProviderName.FRED,
                payload={"series_id": series_id, "status": "missing_api_key", "observations": []},
                source_url="https://api.stlouisfed.org/fred/series/observations",
                source_name="FRED API",
                error="FRED_API_KEY is not configured; returning metadata-only unavailable response.",
                status=ProviderStatus.MISSING_API_KEY,
                mode=DataMode.LIVE,
            )
        return ProviderResponse.unavailable(
            provider=ProviderName.FRED,
            payload={"series_id": series_id, "status": "not_implemented_in_v0.1", "observations": []},
            source_url="https://api.stlouisfed.org/fred/series/observations",
            source_name="FRED API",
            error="FRED live client is not implemented yet.",
            status=ProviderStatus.NOT_IMPLEMENTED,
            mode=DataMode.LIVE,
        )


class EiaProvider:
    def __init__(self, config: EiaProviderConfig) -> None:
        self.config = config

    def series(self, route: str) -> ProviderResponse:
        if not self.config.api_key:
            return ProviderResponse.unavailable(
                provider=ProviderName.EIA,
                payload={"route": route, "status": "missing_api_key", "observations": []},
                source_url="https://api.eia.gov/v2/",
                source_name="EIA API",
                error="EIA_API_KEY is not configured; returning metadata-only unavailable response.",
                status=ProviderStatus.MISSING_API_KEY,
                mode=DataMode.LIVE,
            )
        return ProviderResponse.unavailable(
            provider=ProviderName.EIA,
            payload={"route": route, "status": "not_implemented_in_v0.1", "observations": []},
            source_url="https://api.eia.gov/v2/",
            source_name="EIA API",
            error="EIA live client is not implemented yet.",
            status=ProviderStatus.NOT_IMPLEMENTED,
            mode=DataMode.LIVE,
        )
