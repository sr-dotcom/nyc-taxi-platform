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

## Find data quality issues

Run after the setup above:

    python scripts/find_issues.py data/raw/yellow_tripdata_2026-09.parquet

This prints the count of suspicious rows for each rule and one example row for each main finding. The results are described in [docs/findings.md](docs/findings.md).

## Reproduce the numbers in the docs

Run after the setup above:

    python scripts/investigate.py data/raw/yellow_tripdata_2026-09.parquet

This prints every supporting number quoted in [docs/findings.md](docs/findings.md) and in the Observations section of [docs/columns.md](docs/columns.md), each with a label. Running it twice gives the same output. The file `taxi_zone_lookup.csv` must be in the same folder as the Parquet file.
