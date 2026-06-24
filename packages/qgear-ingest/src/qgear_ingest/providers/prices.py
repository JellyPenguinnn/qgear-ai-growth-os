from __future__ import annotations

from dataclasses import dataclass

from qgear_ingest.providers.base import DataMode, ProviderName, ProviderResponse, ProviderStatus


@dataclass(frozen=True)
class AlphaVantagePriceProviderConfig:
    api_key: str | None


class AlphaVantagePriceProvider:
    def __init__(self, config: AlphaVantagePriceProviderConfig) -> None:
        self.config = config

    def daily_prices(self, tickers: tuple[str, ...]) -> ProviderResponse:
        return self.daily_adjusted_history(tickers[0] if tickers else "")

    def daily_adjusted_history(self, ticker: str, *, output_size: str = "compact") -> ProviderResponse:
        normalized = ticker.upper()
        source_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED"
        if not self.config.api_key:
            return ProviderResponse.unavailable(
                provider=ProviderName.ALPHA_VANTAGE,
                payload={"ticker": normalized, "prices": [], "status": "missing_api_key"},
                source_url=source_url,
                source_name="Alpha Vantage daily adjusted prices",
                error="ALPHA_VANTAGE_API_KEY is not configured; price history falls back to demo/mock where configured.",
                status=ProviderStatus.MISSING_API_KEY,
                mode=DataMode.LIVE,
            )
        return ProviderResponse.unavailable(
            provider=ProviderName.ALPHA_VANTAGE,
            payload={"ticker": normalized, "prices": [], "status": "not_implemented"},
            source_url=source_url,
            source_name="Alpha Vantage daily adjusted prices",
            error="Alpha Vantage live price-history client is not implemented in this local foundation yet.",
            status=ProviderStatus.NOT_IMPLEMENTED,
            mode=DataMode.LIVE,
        )
