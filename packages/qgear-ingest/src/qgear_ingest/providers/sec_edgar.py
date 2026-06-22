from __future__ import annotations

import json
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from qgear_ingest.providers.base import (
    DataMode,
    FilingMetadata,
    ProviderName,
    ProviderResponse,
    ProviderStatus,
    utc_now_iso,
)


SEC_BASE = "https://data.sec.gov"


@dataclass
class SecEdgarProvider:
    user_agent: str
    cache_dir: Path
    max_requests_per_second: int = 10
    timeout_seconds: int = 20

    def __post_init__(self) -> None:
        if not self.user_agent or "contact" not in self.user_agent.lower() and "@" not in self.user_agent:
            raise ValueError("SEC access requires a custom User-Agent with contact information.")
        self.max_requests_per_second = min(max(1, self.max_requests_per_second), 10)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._last_request_at = 0.0

    def company_facts(self, cik: str) -> ProviderResponse:
        normalized = cik.zfill(10)
        url = f"{SEC_BASE}/api/xbrl/companyfacts/CIK{normalized}.json"
        return self._fetch_json(
            url,
            cache_name=f"sec_companyfacts_{normalized}.json",
            source_name="SEC EDGAR company facts",
        )

    def submissions(self, cik: str) -> ProviderResponse:
        normalized = cik.zfill(10)
        url = f"{SEC_BASE}/submissions/CIK{normalized}.json"
        return self._fetch_json(
            url,
            cache_name=f"sec_submissions_{normalized}.json",
            source_name="SEC EDGAR submissions",
        )

    def filing_metadata(self, cik: str, *, limit: int = 20) -> ProviderResponse:
        submissions = self.submissions(cik)
        if submissions.status != ProviderStatus.OK:
            return submissions

        filings = _extract_recent_filings(submissions.payload, limit=limit)
        normalized = cik.zfill(10)
        return ProviderResponse.ok(
            provider=ProviderName.SEC_EDGAR,
            payload={"cik": normalized, "filings": [filing.__dict__ for filing in filings]},
            source_url=submissions.source_url,
            source_name="SEC EDGAR filing metadata",
            cached=submissions.cached,
            source_date=filings[0].filing_date if filings else None,
            as_of_date=submissions.metadata.as_of_date,
            cache_written_at=submissions.metadata.cache_written_at,
            cache_key=f"sec_filing_metadata_{normalized}_{limit}",
            mode=DataMode.LIVE,
        )

    def _fetch_json(self, url: str, cache_name: str, source_name: str) -> ProviderResponse:
        cache_path = self.cache_dir / cache_name
        if cache_path.exists():
            return self._read_cache(cache_path, url=url, source_name=source_name)

        min_interval = 1 / self.max_requests_per_second
        elapsed = time.monotonic() - self._last_request_at
        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)

        request = Request(url, headers={"User-Agent": self.user_agent, "Accept": "application/json"})
        retries = 3
        for attempt in range(retries):
            try:
                with urlopen(request, timeout=self.timeout_seconds) as response:
                    payload = json.loads(response.read().decode("utf-8"))
                retrieved_at = utc_now_iso()
                self._last_request_at = time.monotonic()
                self._write_cache(cache_path, payload=payload, retrieved_at=retrieved_at, source_url=url, source_name=source_name)
                return ProviderResponse.ok(
                    provider=ProviderName.SEC_EDGAR,
                    payload=payload,
                    source_url=url,
                    source_name=source_name,
                    cached=False,
                    source_date=_infer_source_date(payload),
                    as_of_date=_infer_as_of_date(payload),
                    cache_written_at=retrieved_at,
                    cache_key=cache_name,
                    mode=DataMode.LIVE,
                    retrieved_at=retrieved_at,
                )
            except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
                if attempt == retries - 1:
                    return ProviderResponse.unavailable(
                        provider=ProviderName.SEC_EDGAR,
                        source_url=url,
                        source_name=source_name,
                        error=f"SEC request failed after {retries} attempts: {exc}",
                        status=ProviderStatus.UNAVAILABLE,
                        payload={},
                        mode=DataMode.LIVE,
                    )
                time.sleep(2**attempt)

        return ProviderResponse.unavailable(
            provider=ProviderName.SEC_EDGAR,
            source_url=url,
            source_name=source_name,
            error="SEC request failed unexpectedly.",
            status=ProviderStatus.ERROR,
            mode=DataMode.LIVE,
        )

    def _read_cache(self, cache_path: Path, *, url: str, source_name: str) -> ProviderResponse:
        try:
            cached = json.loads(cache_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            return ProviderResponse.unavailable(
                provider=ProviderName.SEC_EDGAR,
                source_url=url,
                source_name=source_name,
                error=f"SEC cache read failed: {exc}",
                status=ProviderStatus.ERROR,
                mode=DataMode.LIVE,
            )

        if isinstance(cached, dict) and "payload" in cached:
            payload = cached.get("payload") or {}
            cache_written_at = str(cached.get("cache_written_at") or _mtime_iso(cache_path))
            source_date = cached.get("source_date") or _infer_source_date(payload)
            as_of_date = cached.get("as_of_date") or _infer_as_of_date(payload)
        else:
            payload = cached
            cache_written_at = _mtime_iso(cache_path)
            source_date = _infer_source_date(payload)
            as_of_date = _infer_as_of_date(payload)

        return ProviderResponse.ok(
            provider=ProviderName.SEC_EDGAR,
            payload=payload if isinstance(payload, dict) else {"payload": payload},
            source_url=url,
            source_name=source_name,
            cached=True,
            source_date=source_date,
            as_of_date=as_of_date,
            cache_written_at=cache_written_at,
            cache_key=cache_path.name,
            mode=DataMode.LIVE,
        )

    def _write_cache(self, cache_path: Path, *, payload: dict, retrieved_at: str, source_url: str, source_name: str) -> None:
        cache_path.write_text(
            json.dumps(
                {
                    "payload": payload,
                    "source_url": source_url,
                    "source_name": source_name,
                    "source_date": _infer_source_date(payload),
                    "as_of_date": _infer_as_of_date(payload),
                    "cache_written_at": retrieved_at,
                }
            ),
            encoding="utf-8",
        )


def _extract_recent_filings(payload: dict[str, Any], *, limit: int) -> tuple[FilingMetadata, ...]:
    recent = payload.get("filings", {}).get("recent", {})
    accession_numbers = recent.get("accessionNumber", [])
    forms = recent.get("form", [])
    filing_dates = recent.get("filingDate", [])
    report_dates = recent.get("reportDate", [])
    primary_documents = recent.get("primaryDocument", [])
    cik = str(payload.get("cik", "")).zfill(10)

    filings: list[FilingMetadata] = []
    for index, accession in enumerate(accession_numbers[:limit]):
        accession_no_dash = str(accession).replace("-", "")
        primary_document = _safe_index(primary_documents, index) or ""
        source_url = f"https://www.sec.gov/Archives/edgar/data/{int(cik) if cik.isdigit() else cik}/{accession_no_dash}/{primary_document}"
        filings.append(
            FilingMetadata(
                accession_number=str(accession),
                form=str(_safe_index(forms, index) or ""),
                filing_date=str(_safe_index(filing_dates, index) or ""),
                report_date=_safe_index(report_dates, index),
                primary_document=primary_document,
                source_url=source_url,
            )
        )
    return tuple(filings)


def _safe_index(values: list[Any], index: int) -> Any | None:
    return values[index] if index < len(values) else None


def _infer_source_date(payload: dict[str, Any]) -> str | None:
    recent = payload.get("filings", {}).get("recent", {}) if isinstance(payload, dict) else {}
    filing_dates = recent.get("filingDate", []) if isinstance(recent, dict) else []
    if filing_dates:
        return str(filing_dates[0])
    return None


def _infer_as_of_date(payload: dict[str, Any]) -> str | None:
    if not isinstance(payload, dict):
        return None
    if "filed" in payload:
        return str(payload["filed"])
    if "end" in payload:
        return str(payload["end"])
    return _infer_source_date(payload)


def _mtime_iso(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime, tz=UTC).replace(microsecond=0).isoformat()
