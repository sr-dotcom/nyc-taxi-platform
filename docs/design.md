# Design

## Purpose

This platform turns raw NYC taxi trip records into clean, trusted tables that answer questions about how people move around the city. It keeps the raw data unchanged, so every number in a cleaned table can be traced back to the file it came from.

## Sources

- **Taxi trips (now):** the monthly yellow taxi trip files in Parquet, from the NYC TLC Trip Record Data page.
- **Zone lookup (now):** `taxi_zone_lookup.csv`, which gives the borough and zone name for each zone ID.
- **311 service requests (later):** complaints and requests from NYC Open Data, to compare with trip patterns by zone.

See [sources.md](sources.md) for the files, download dates and sizes.

## Layers

- **Bronze:** the raw files exactly as downloaded, with no row or value changed.
- **Silver:** cleaned trips with correct types and zone names, where each row is flagged (not deleted) against the rules in [findings.md](findings.md).
- **Gold:** small summary tables built from silver, each one made to answer a user question.

## Users and their questions

The main users are city transport analysts and TLC policy staff. They would ask:

1. Which pickup zones have the most trips in each hour of the day?
2. How does the average fare per mile differ between boroughs?
3. What share of each vendor's trips fail a data quality rule?

## Out of scope for now

- Taxi types other than yellow, such as green taxis and for-hire vehicles.
- More than one month of trip data.
- 311 service requests, until the taxi layers work.
- Dashboards, scheduled runs and cloud storage.
- Fixing or deleting bad rows. Silver only flags them.
