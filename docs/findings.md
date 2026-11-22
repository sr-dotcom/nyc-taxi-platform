# Data quality findings

Checked file: `yellow_tripdata_2026-09.parquet` (3,876,044 rows).
Reproduce the counts with the command in the [README](../README.md).
This document only reports. No row was changed or deleted.

## 1. Negative fare

- **Rule:** `fare_amount` is below 0.
- **Rows:** 14,190 (0.366% of the file).
- **Example:** VendorID 2, pickup 2026-09-01 00:06:56, distance 8.41 miles, `fare_amount` -35.2, `total_amount` -40.95, `payment_type` 2 (Cash). The fee columns are negative too.
- **Best guess at the cause:** these rows are refunds or reversed fares. 8,671 of the 14,190 rows (61.1%) have `payment_type` 4 (Dispute). The data does not confirm this.

## 2. Pickup outside the file's month

- **Rule:** the pickup time is not in September 2026.
- **Rows:** 22 (0.001% of the file). One row is from 2009. Two rows are from 31 August, just before midnight. Nineteen rows are from 1 to 7 October.
- **Example:** VendorID 2, pickup 2009-01-01 09:32:44, drop-off 2009-01-01 10:22:44, distance 17.32 miles, `fare_amount` 70.9, `total_amount` 99.73.
- **Best guess at the cause:** the 2009 and October rows have a wrong clock or were added late to this file. The two 31 August rows are normal trips that started a few minutes before midnight, so they may not be errors.

## 3. Zero-length trip

- **Rule:** the drop-off time equals the pickup time.
- **Rows:** 48,202 (1.244% of the file).
- **Example:** VendorID 7, pickup and drop-off both 2026-09-01 00:02:03, distance 17.39 miles, `fare_amount` 70.0, `total_amount` 92.63, `payment_type` 1 (Credit card).
- **Best guess at the cause:** 47,893 of the 48,202 rows (99.4%) come from VendorID 7 (Helix). Almost all have a fare above 0, so these are paid trips with a wrong drop-off time. Helix may copy the pickup time into the drop-off time. The data does not confirm this.

## 4. Distance above 1,000 miles

- **Rule:** `trip_distance` is above 1,000 miles.
- **Rows:** 46 (0.001% of the file). The largest value is 232,644.8 miles.
- **Example:** VendorID 2, pickup 2026-09-01 08:26:00, drop-off 09:02:00 (36 minutes), distance 53,718.71 miles, `fare_amount` 55.2, `total_amount` 59.95, `payment_type` 0 (Flex Fare), `request_source` HV0003.
- **Best guess at the cause:** the time and the fare are normal for the trip, so only the distance is wrong. 45 of the 46 rows are Flex Fare trips from VendorID 2. The distance in these records may not come from a taximeter, for example a GPS error or a wrong unit. The data does not confirm this.

## 5. Zero fare on a trip with distance

- **Rule:** `fare_amount` is 0 and `trip_distance` is above 0.
- **Rows:** 1,794 (0.046% of the file).
- **Example:** VendorID 6, pickup 2026-09-01 00:13:59, drop-off 00:49:43, distance 15.81 miles, `fare_amount` 0.0, `total_amount` 41.0, `payment_type` 0 (Flex Fare), `request_source` A.
- **Best guess at the cause:** these are mostly not free trips. 1,230 of the 1,794 rows have a `total_amount` above 0. 828 rows are Flex Fare trips, and for these the fare may be held in another column or not filled in. The data does not confirm this.

## Other checks (counts only)

These checks are not full findings. They have no example row.

| Check                                 | Rows    | Share  | Note                                                                 |
|---------------------------------------|---------|--------|----------------------------------------------------------------------|
| Zero distance                         | 147,158 | 3.797% | 118,311 of these rows have different pickup and drop-off zones.      |
| Airport fee outside JFK and LaGuardia | 7,271   | 0.188% | The data dictionary says this fee is for JFK and LaGuardia pickups only. |
| Unknown zone (ID 264)                 | 6,200   | 0.160% | Zone 264 is "Unknown" in `taxi_zone_lookup.csv`.                     |
| Zero passengers                       | 10,537  | 0.272% | The driver types this number. It may mean "not entered".             |
| Speed above 80 mph                    | 1,168   | 0.030% | Calculated from distance and trip time.                              |
| Trip longer than 24 hours             | 18      | <0.001% |                                                                      |

## Checks with no problems

- Drop-off time before pickup time: 0 rows.
- Exact duplicate rows: 0.
- Pickup or drop-off zone IDs missing from `taxi_zone_lookup.csv`: 0.
