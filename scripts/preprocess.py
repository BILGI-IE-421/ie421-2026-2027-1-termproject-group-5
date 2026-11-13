"""Clean, join and reshape the raw files into data/processed/.

Inputs (from scripts/download_data.py, in data/raw/):
    listings.csv.gz, reviews.csv.gz, SNAPSHOT.txt
Outputs (in data/processed/):
    listings_clean.csv            one row per listing, analysis columns only
    district_summary.csv          one row per district (groupby)
    monthly_reviews_district.csv  one row per month, one column per busiest district (merge + pivot)

Run from the repository root:
    python scripts/preprocess.py
"""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
OUT_DIR = ROOT / "data" / "processed"

LISTING_COLUMNS = [
    "id", "host_id", "calculated_host_listings_count",
    "neighbourhood_cleansed", "latitude", "longitude",
    "room_type", "accommodates", "bedrooms", "price",
    "minimum_nights", "availability_365",
    "number_of_reviews", "review_scores_rating",
    "first_review", "last_review", "last_scraped",
]


def parse_dates(series):
    """The single date parser used everywhere.

    Inside Airbnb writes ISO dates (YYYY-MM-DD), so the
    format is fixed and dayfirst is False. Bad values become NaT.
    """
    return pd.to_datetime(series, format="%Y-%m-%d", dayfirst=False, errors="coerce")


def parse_price(series):
    """'$1,250.00' -> 1250.0. Zero or unparseable prices become missing."""
    cleaned = series.astype("string").str.replace(r"[^0-9.]", "", regex=True)
    price = pd.to_numeric(cleaned, errors="coerce").astype("float64")
    return price.where(price > 0)


def clean_listings():
    listings = pd.read_csv(RAW_DIR / "listings.csv.gz", usecols=LISTING_COLUMNS, low_memory=False)
    n_raw = len(listings)

    # The listing id is the identifier: keep one row per listing.
    listings = listings.drop_duplicates(subset="id")

    listings["price"] = parse_price(listings["price"])
    for col in ["first_review", "last_review", "last_scraped"]:
        listings[col] = parse_dates(listings[col])

    listings = listings.rename(columns={
        "neighbourhood_cleansed": "district",
        "calculated_host_listings_count": "host_listings",
    })
    # A host with more than one active listing is treated as a "multi-listing" host.
    listings["multi_listing_host"] = listings["host_listings"] > 1

    # Outliers are flagged, not dropped: the price distribution is heavy-tailed
    # and we report medians, which are robust to a few extreme values.
    upper = listings["price"].quantile(0.995)
    listings["price_outlier"] = listings["price"] > upper

    print(f"listings: {n_raw} raw rows -> {len(listings)} unique listings")
    print(f"  price missing: {listings['price'].isna().sum()}, flagged outliers: {listings['price_outlier'].sum()}")
    return listings


def district_summary(listings):
    priced = listings[listings["price"].notna() & ~listings["price_outlier"]]
    summary = listings.groupby("district").agg(
        listings=("id", "size"),
        share_entire_home=("room_type", lambda s: (s == "Entire home/apt").mean()),
        share_multi_listing_host=("multi_listing_host", "mean"),
        reviews_total=("number_of_reviews", "sum"),
    )
    summary["median_price"] = priced.groupby("district")["price"].median()
    summary["priced_listings"] = priced.groupby("district")["price"].size()
    return summary.reset_index().sort_values("listings", ascending=False)


def monthly_reviews_by_district(listings, snapshot_date, n_lines=3):
    """Monthly review counts per district, reshaped to one column per district (pivot).

    The three districts with most listings get their own column; all other
    districts are summed into "Other districts", so a line chart has at most four lines.
    """
    reviews = pd.read_csv(RAW_DIR / "reviews.csv.gz", usecols=["listing_id", "date"])
    reviews["date"] = parse_dates(reviews["date"])
    reviews = reviews.dropna(subset=["date"])

    # Attach each review to its listing's district (inner join on the listing id).
    reviews = reviews.merge(listings[["id", "district"]], left_on="listing_id", right_on="id", how="inner")

    top = listings["district"].value_counts().head(n_lines).index
    reviews["group"] = reviews["district"].where(reviews["district"].isin(top), "Other districts")
    reviews["month"] = reviews["date"].dt.to_period("M").dt.to_timestamp()

    monthly = reviews.pivot_table(index="month", columns="group", values="listing_id",
                                  aggfunc="size", fill_value=0)
    monthly = monthly[list(top) + ["Other districts"]]

    # The snapshot month is only partly observed, so it is removed.
    last_full_month = snapshot_date.to_period("M").to_timestamp() - pd.DateOffset(months=1)
    return monthly[monthly.index <= last_full_month].reset_index()


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    snapshot_date = parse_dates(pd.Series([(RAW_DIR / "SNAPSHOT.txt").read_text().strip()]))[0]

    listings = clean_listings()
    listings.to_csv(OUT_DIR / "listings_clean.csv", index=False)

    district_summary(listings).to_csv(OUT_DIR / "district_summary.csv", index=False)

    monthly = monthly_reviews_by_district(listings, snapshot_date)
    monthly.to_csv(OUT_DIR / "monthly_reviews_district.csv", index=False)

    print(f"wrote {len(listings)} listings, {monthly.shape[0]} months to {OUT_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
