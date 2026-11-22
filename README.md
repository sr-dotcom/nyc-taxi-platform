# nyc-taxi-platform

A data platform for analysing NYC taxi trip data.

## Data sources

Raw files come from the [NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) page. They are not stored in this repo. See [docs/sources.md](docs/sources.md) for the file list, download dates and sizes.

## Profile the trip file

Set up once (Windows PowerShell):

    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -r requirements.txt

Run:

    python scripts/profile_trips.py data/raw/yellow_tripdata_2026-09.parquet

Save the output to docs/profile.md (Windows PowerShell):

    python scripts/profile_trips.py data/raw/yellow_tripdata_2026-09.parquet | Out-File -Encoding utf8 docs/profile.md
