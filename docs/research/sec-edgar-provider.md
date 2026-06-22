Title: EDGAR API and Fair Access Provider Note
Author/organisation: U.S. Securities and Exchange Commission
URL or citation: https://www.sec.gov/search-filings/edgar-application-programming-interfaces and https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data
Date accessed: 2026-06-22

Summary:
The SEC describes `data.sec.gov` as the host for JSON REST APIs for company submissions history and extracted XBRL company facts. The submissions endpoint uses 10-digit CIKs, including leading zeroes. SEC fair-access guidance lists a current maximum request rate of 10 requests per second and asks automated clients to declare a User-Agent with contact information.

How it affects Q-GEAR:
SEC EDGAR is the primary free source for filings metadata and company-facts provenance. Q-GEAR must treat SEC data as evidence input, not as an automatic action signal.

Implementation consequence:
The SEC provider must require a custom User-Agent, cap requests at 10 per second or less, use local cache files, preserve source URLs and retrieved/cache timestamps, expose submissions and company-facts endpoints behind provider interfaces, and degrade gracefully when unavailable.

Limitations:
SEC XBRL facts can require taxonomy normalization and filing-date availability handling. The current v0.2 implementation adds provider metadata and fixture-tested SEC submissions/company-facts foundations, but does not yet convert XBRL facts into scored financial metrics.
