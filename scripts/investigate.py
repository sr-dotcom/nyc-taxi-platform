import sys
from pathlib import Path

import pandas as pd

CODES = {  # allowed values, from the data dictionary
    "VendorID": [1, 2, 6, 7],
    "RatecodeID": [1, 2, 3, 4, 5, 6, 99],
    "store_and_fwd_flag": ["Y", "N"],
    "payment_type": [0, 1, 2, 3, 4, 5, 6],
}
FIVE = ["passenger_count", "RatecodeID", "store_and_fwd_flag", "congestion_surcharge", "Airport_fee"]


def show(label, value):
    """Print one labelled number."""
    print(f"- {label}: {value:,}" if isinstance(value, (int, float)) else f"- {label}: {value}")


def count(mask):
    return int(mask.sum())


def pct(part, whole):
    return f"{part / whole:.1%}"


def main(path):
    df = pd.read_parquet(path)
    zones = pd.read_csv(Path(path).with_name("taxi_zone_lookup.csv"))  # lives next to the Parquet file
    pickup, dropoff = df.tpep_pickup_datetime, df.tpep_dropoff_datetime
    minutes = (dropoff - pickup).dt.total_seconds() / 60
    flex = df.payment_type == 0

    print("## File")
    show("Rows", len(df))

    print("\n## Finding 1: negative fare")
    neg = df.fare_amount < 0
    disputes = neg & (df.payment_type == 4)
    show("Rows with fare below 0", count(neg))
    show("Of these, payment_type 4 (Dispute)", count(disputes))
    show("Share that are disputes", pct(count(disputes), count(neg)))

    print("\n## Finding 2: pickup outside the month")
    month = pickup.dt.to_period("M").mode()[0]
    start, end = month.start_time, (month + 1).start_time
    day = pd.Timedelta(days=1)
    outside = (pickup < start) | (pickup >= end)
    show("Pickups outside the month", count(outside))
    show("Pickups more than 1 day before the month", count(pickup < start - day))
    show("Pickups in the last day before the month", count((pickup >= start - day) & (pickup < start)))
    show("Pickups after the month ends", count(pickup >= end))
    show("Earliest pickup after the month ends", pickup[pickup >= end].min())
    show("Latest pickup after the month ends", pickup[pickup >= end].max())

    print("\n## Finding 3: zero-length trip")
    zero = minutes == 0
    show("Zero-length trips", count(zero))
    for vendor, k in df[zero].VendorID.value_counts().items():
        show(f"Zero-length trips from VendorID {vendor}", int(k))
    show("Share from VendorID 7", pct(count(zero & (df.VendorID == 7)), count(zero)))
    show("Zero-length trips with fare above 0", count(zero & (df.fare_amount > 0)))

    print("\n## Finding 4: distance above 1,000 miles")
    far = df.trip_distance > 1000
    show("Rows above 1,000 miles", count(far))
    show("Largest distance (miles)", float(df.trip_distance.max()))
    show("Of these, Flex Fare (payment_type 0)", count(far & flex))
    show("Of these, VendorID 2", count(far & (df.VendorID == 2)))

    print("\n## Finding 5: zero fare on a trip with distance")
    zf = (df.fare_amount == 0) & (df.trip_distance > 0)
    show("Zero fare with distance above 0", count(zf))
    show("Of these, total_amount above 0", count(zf & (df.total_amount > 0)))
    show("Of these, Flex Fare", count(zf & flex))

    print("\n## Other checks")
    zd = df.trip_distance == 0
    show("Zero distance, pickup zone differs from drop-off zone", count(zd & (df.PULocationID != df.DOLocationID)))

    print("\n## Checks with no problems")
    show("Drop-off before pickup", count(dropoff < pickup))
    show("Exact duplicate rows", count(df.duplicated()))
    known = df.PULocationID.isin(zones.LocationID) & df.DOLocationID.isin(zones.LocationID)
    show("Rows with a zone ID missing from the lookup", count(~known))

    print("\n## Observations (docs/columns.md)")
    empty = df[FIVE].isna()
    for col in FIVE:
        show(f"Empty {col}", count(empty[col]))
    show("Rows where all five are empty", count(empty.all(axis=1)))
    show("Of these, Flex Fare", count(empty.all(axis=1) & flex))
    show("Flex Fare rows", count(flex))
    filled = df.request_source.notna()
    show("request_source filled", count(filled))
    show("Of these, Flex Fare", count(filled & flex))
    show("Flex Fare rows without request_source", count(flex & ~filled))
    for col, allowed in CODES.items():
        show(f"{col} values not in the dictionary (empty not counted)", count(df[col].notna() & ~df[col].isin(allowed)))
    show("RatecodeID 6 rows", count(df.RatecodeID == 6))
    show("payment_type 6 rows", count(df.payment_type == 6))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python scripts/investigate.py <path-to-parquet>")
    main(sys.argv[1])
