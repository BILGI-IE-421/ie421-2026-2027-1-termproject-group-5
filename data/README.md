# Data card

> Draft prepared with AI assistance (see `AI_USAGE.md`); the numbers below come from running the scripts on the real files. The course requires the data card to be in our own words: **TO DO** — reread and rewrite each field ourselves before submission.

## Dataset 1: Inside Airbnb – Istanbul

- **Source and URL:** Inside Airbnb, https://insideairbnb.com/get-the-data/ (section "Istanbul, Marmara, Turkey"). Three files from the same snapshot:
  - `listings.csv.gz` – detailed listings
  - `reviews.csv` – summary reviews (listing id and date only; the detailed `reviews.csv.gz` has the same two columns plus review text, and `preprocess.py` reads either)
  - `neighbourhoods.geojson` – district boundaries
- **License:** Creative Commons Attribution 4.0 International (CC BY 4.0), as stated by Inside Airbnb. **TO CHECK** on the site.
- **Date accessed:** 2026-11-13. Snapshot dated 25 September 2026 on the site; listings were scraped on 28–29 September 2026 (`last_scraped`).
- **Time range and granularity:** Listings are a single snapshot, one row per listing. Reviews are one row per review, dated by day, from 2011-05-17 to 2026-09-28.
- **Size:** listings 27,232 rows × 90 columns; reviews 624,804 rows × 2 columns (17,571 listings); GeoJSON 39 districts.
- **Columns used:**
  - `id` (listing identifier), `host_id`, `calculated_host_listings_count` → `host_listings` (active listings of the host)
  - `neighbourhood_cleansed` → `district` (one of 39 Istanbul districts; join key to the GeoJSON `neighbourhood` property)
  - `latitude`, `longitude` (degrees, shifted slightly by Inside Airbnb for privacy)
  - `room_type`, `accommodates` (guests), `bedrooms`
  - `price` (nightly price as text, e.g. `$4,736.32`; the `$` sign is a display convention, the amounts are in Turkish lira — **TO CHECK** on a few listings on airbnb.com)
  - `minimum_nights`, `availability_365` (days available in the next year), `number_of_reviews`, `review_scores_rating` (0–5)
  - `first_review`, `last_review`, `last_scraped` (dates)
  - reviews: `listing_id`, `date`
- **Known issues:**
  - No duplicate listing ids. All 624,804 reviews match a listing in the listings file.
  - `price` is missing for 2,679 listings (9.8%). Prices are heavy-tailed: median 3,710, 99.5th percentile 55,730, maximum about 5 million (very likely an entry error).
  - 9,661 listings (35%) have no reviews, so `first_review`, `last_review` and `review_scores_rating` are missing for them. `bedrooms` is missing for 23 listings.
  - Reviews are a proxy for stays: not every guest writes a review.
  - Only listings that are still active in the snapshot are included, so reviews of listings that were removed earlier are missing. Growth over time is therefore overstated for early years.
  - The snapshot month (September 2026) is only partly observed.
- **Cleaning decisions and why:**
  - Keep one row per listing `id`, because `id` is the identifier.
  - Parse `price` into a number; empty or zero prices become missing, not zero, and are left out only of price analyses.
  - Dates are parsed by one function (`parse_dates` in `preprocess.py`) with the fixed ISO format `YYYY-MM-DD` (`dayfirst=False`); all dates are local calendar dates as published.
  - Prices above the 99.5th percentile (121 listings) are flagged (`price_outlier`), not deleted: district medians leave them out, the distribution figure keeps them on a log axis.
  - Reviews are joined to listings on `listing_id = id` (inner join), counted per month and reshaped to one column per district (pivot) for the three districts with most listings plus "Other districts". September 2026 is dropped as a partial month.
  - District summaries (`groupby`) give the number of listings, median price, share of entire homes and share of multi-listing hosts (hosts with more than one active listing).
- **How to regenerate:** `python scripts/download_data.py && python scripts/preprocess.py` (to reproduce exactly, use `--snapshot` with the snapshot date in the file URLs on the site).

