# Trip file profile

- Rows: 3,876,044
- Columns: 21

## Columns

| Column                | Type           | Missing   |
|-----------------------|----------------|-----------|
| VendorID              | int32          | 0         |
| tpep_pickup_datetime  | datetime64[us] | 0         |
| tpep_dropoff_datetime | datetime64[us] | 0         |
| passenger_count       | float64        | 1,190,413 |
| trip_distance         | float64        | 0         |
| RatecodeID            | float64        | 1,190,413 |
| store_and_fwd_flag    | str            | 1,190,413 |
| PULocationID          | int32          | 0         |
| DOLocationID          | int32          | 0         |
| payment_type          | int64          | 0         |
| fare_amount           | float64        | 0         |
| extra                 | float64        | 0         |
| mta_tax               | float64        | 0         |
| tip_amount            | float64        | 0         |
| tolls_amount          | float64        | 0         |
| improvement_surcharge | float64        | 0         |
| total_amount          | float64        | 0         |
| congestion_surcharge  | float64        | 1,190,413 |
| Airport_fee           | float64        | 1,190,413 |
| cbd_congestion_fee    | float64        | 0         |
| request_source        | str            | 2,685,952 |

## Time ranges

| Column                | Earliest            | Latest              |
|-----------------------|---------------------|---------------------|
| tpep_pickup_datetime  | 2009-01-01 09:32:44 | 2026-10-07 07:40:40 |
| tpep_dropoff_datetime | 2009-01-01 10:22:44 | 2026-10-07 07:59:16 |

## Fare, distance and total

| Column        | Min     | Median | Max      |
|---------------|---------|--------|----------|
| fare_amount   | -1800.0 | 17.7   | 9999.7   |
| trip_distance | 0.0     | 1.96   | 232644.8 |
| total_amount  | -1801.0 | 25.26  | 10003.7  |
