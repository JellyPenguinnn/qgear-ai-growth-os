Title: EIA APIv2 Technical Documentation Provider Note
Author/organisation: U.S. Energy Information Administration
URL or citation: https://www.eia.gov/opendata/documentation.php
Date accessed: 2026-06-22

Summary:
EIA APIv2 is a REST-style public API for energy data. The documentation states that users must use an assigned API key and that the API key must appear in the URL. It also warns that high-volume recursive scraping can trigger temporary API-key suspension and that callers should throttle requests.

How it affects Q-GEAR:
EIA can support the data-center power, grid, electricity, and energy-cost side of AI infrastructure research. It should provide background evidence for power/cooling and utility exposure, not a standalone buy/add signal.

Implementation consequence:
The EIA provider should stay optional behind `EIA_API_KEY`, return clear missing-key metadata in demo/local use, preserve provider/source timestamps when live calls are implemented, and use throttling/backoff before any broad data pulls.

Limitations:
EIA data is macro/industry context rather than company-specific proof. v0.2 only documents and models provider readiness; live EIA ingestion remains deferred.
