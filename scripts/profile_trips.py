import sys

import pandas as pd


def table(headers, rows):
    """Print a Markdown table with padded, aligned columns."""
    widths = [max(len(str(x)) for x in col) for col in zip(headers, *rows)]

    def line(cells):
        return "| " + " | ".join(str(c).ljust(w) for c, w in zip(cells, widths)) + " |"

    print(line(headers))
    print("|" + "|".join("-" * (w + 2) for w in widths) + "|")
    for row in rows:
        print(line(row))


def main(path):
    df = pd.read_parquet(path)
    print("# Trip file profile\n")
    print(f"- Rows: {len(df):,}")
    print(f"- Columns: {len(df.columns)}\n")

    print("## Columns\n")
    table(
        ["Column", "Type", "Missing"],
        [(c, df[c].dtype, f"{df[c].isna().sum():,}") for c in df.columns],
    )

    print("\n## Time ranges\n")
    table(
        ["Column", "Earliest", "Latest"],
        [(c, df[c].min(), df[c].max()) for c in ["tpep_pickup_datetime", "tpep_dropoff_datetime"]],
    )

    print("\n## Fare, distance and total\n")
    table(
        ["Column", "Min", "Median", "Max"],
        [(c, df[c].min(), df[c].median(), df[c].max()) for c in ["fare_amount", "trip_distance", "total_amount"]],
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python scripts/profile_trips.py <path-to-parquet>")
    main(sys.argv[1])
