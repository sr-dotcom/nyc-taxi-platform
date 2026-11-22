# Column dictionary

Source of meanings: [data_dictionary_trip_records_yellow.pdf](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) (dated March 18, 2025).
Types come from [profile.md](profile.md). The file is `yellow_tripdata_2026-09.parquet`.

## Columns

| Column                | Type           | Meaning                                                  | Unit                  |
|-----------------------|----------------|----------------------------------------------------------|-----------------------|
| VendorID              | int32          | The company that supplied the trip record (see codes)    | code                  |
| tpep_pickup_datetime  | datetime64[us] | When the meter started                                   | date and time         |
| tpep_dropoff_datetime | datetime64[us] | When the meter stopped                                   | date and time         |
| passenger_count       | float64        | Number of passengers in the car                          | passengers            |
| trip_distance         | float64        | Distance of the trip, measured by the taximeter          | miles                 |
| RatecodeID            | float64        | The rate that applied at the end of the trip (see codes) | code                  |
| store_and_fwd_flag    | str            | Whether the record was held in the car before sending    | Y or N                |
| PULocationID          | int32          | Taxi zone where the meter started                        | TLC taxi zone ID      |
| DOLocationID          | int32          | Taxi zone where the meter stopped                        | TLC taxi zone ID      |
| payment_type          | int64          | How the passenger paid (see codes)                       | code                  |
| fare_amount           | float64        | Fare calculated by the meter from time and distance      | US dollars            |
| extra                 | float64        | Miscellaneous extras and surcharges                      | US dollars            |
| mta_tax               | float64        | Tax triggered by the metered rate                        | US dollars            |
| tip_amount            | float64        | Tip. Filled in for credit card tips only. Cash tips are not included | US dollars |
| tolls_amount          | float64        | Total of all tolls paid on the trip                      | US dollars            |
| improvement_surcharge | float64        | Surcharge charged at the start of the trip (since 2015)  | US dollars            |
| total_amount          | float64        | Total charged to the passenger. Cash tips are not included | US dollars          |
| congestion_surcharge  | float64        | New York State congestion surcharge collected on the trip | US dollars           |
| Airport_fee           | float64        | Fee for pickups at LaGuardia and JFK airports only       | US dollars            |
| cbd_congestion_fee    | float64        | Charge for the MTA Congestion Relief Zone (since 5 Jan 2025) | US dollars        |
| request_source        | str            | Not in the data dictionary. Meaning unknown               | unknown               |

## Codes

### VendorID

| Code | Meaning                         |
|------|---------------------------------|
| 1    | Creative Mobile Technologies, LLC |
| 2    | Curb Mobility, LLC              |
| 6    | Myle Technologies Inc           |
| 7    | Helix                           |

### RatecodeID

| Code | Meaning                  |
|------|--------------------------|
| 1    | Standard rate            |
| 2    | JFK                      |
| 3    | Newark                   |
| 4    | Nassau or Westchester    |
| 5    | Negotiated fare          |
| 6    | Group ride               |
| 99   | Null or unknown          |

### store_and_fwd_flag

| Code | Meaning                              |
|------|--------------------------------------|
| Y    | Store and forward trip               |
| N    | Not a store and forward trip         |

### payment_type

| Code | Meaning       |
|------|---------------|
| 0    | Flex Fare trip |
| 1    | Credit card   |
| 2    | Cash          |
| 3    | No charge     |
| 4    | Dispute       |
| 5    | Unknown       |
| 6    | Voided trip   |

### request_source

Not in the data dictionary, so no code meanings are available. The values in this file are:
`HV0003`, `HV0005`, `A`, `EH0004`, `CC`, `EH0010`.

## Differences between the file and the dictionary

- **In the file, not in the dictionary:** `request_source`.
- **In the dictionary, not in the file:** none.
- **Name differs:** the file uses `Airport_fee`. The dictionary uses `airport_fee`.
