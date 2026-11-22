import sys

import pandas as pd

from profile_trips import table

MAIN = [  # the five findings that also print an example row
    "Negative fare",
    "Pickup outside the file's month",
    "Zero-length trip",
    "Distance above 1,000 miles",
    "Zero fare on a trip with distance",
]


def find_rules(df):
    """Return {rule name: True/False for each row}. True means the row looks wrong."""
    pickup = df.tpep_pickup_datetime
    minutes = (df.tpep_dropoff_datetime - pickup).dt.total_seconds() / 60
    month = pickup.dt.to_period("M").mode()[0]  # the month most pickups are in
    return {
        # the five main findings
        "Negative fare": df.fare_amount < 0,
        "Pickup outside the file's month": pickup.dt.to_period("M") != month,
        "Zero-length trip": minutes == 0,
        "Distance above 1,000 miles": df.trip_distance > 1000,
        "Zero fare on a trip with distance": (df.fare_amount == 0) & (df.trip_distance > 0),
        # extra checks: counts only
        "Zero passengers": df.passenger_count == 0,
        "Trip longer than 24 hours": minutes > 24 * 60,
        "Speed above 80 mph": (minutes > 0) & (df.trip_distance / (minutes / 60) > 80),
        "Zero distance": df.trip_distance == 0,
        "Airport fee outside JFK and LaGuardia": (df.Airport_fee > 0) & ~df.PULocationID.isin([132, 138]),
        "Unknown zone (ID 264)": (df.PULocationID == 264) | (df.DOLocationID == 264),
    }


def main(path):
    df = pd.read_parquet(path)
    results = find_rules(df)
    print(f"Rows checked: {len(df):,}\n")
    table(
        ["Rule", "Rows", "Share"],
        [(name, f"{bad.sum():,}", f"{bad.mean():.3%}") for name, bad in results.items()],
    )
    for name in MAIN:
        print(f"\nExample row: {name}\n")
        table(["Column", "Value"], list(df[results[name]].sort_values("tpep_pickup_datetime").iloc[0].items()))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python scripts/find_issues.py <path-to-parquet>")
    main(sys.argv[1])
