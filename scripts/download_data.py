"""Download the raw data into data/raw/.

Sources
- Inside Airbnb, Istanbul: listings.csv.gz, reviews.csv.gz, neighbourhoods.geojson

Run from the repository root:
    python scripts/download_data.py
    python scripts/download_data.py --snapshot 2025-06-29   # pick a snapshot date by hand
"""

import argparse
import re
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"

AIRBNB_PAGE = "https://insideairbnb.com/get-the-data/"
AIRBNB_BASE = "https://data.insideairbnb.com/turkey/marmara/istanbul"
AIRBNB_FILES = {
    "listings.csv.gz": "data/listings.csv.gz",
    "reviews.csv.gz": "data/reviews.csv.gz",
    "neighbourhoods.geojson": "visualisations/neighbourhoods.geojson",
}


def latest_snapshot():
    """Find the newest Istanbul snapshot date listed on the Inside Airbnb page."""
    html = requests.get(AIRBNB_PAGE, timeout=60).text
    dates = re.findall(r"turkey/marmara/istanbul/(\d{4}-\d{2}-\d{2})/", html)
    if not dates:
        raise RuntimeError("No Istanbul snapshot found; pass --snapshot YYYY-MM-DD")
    return max(dates)


def download(url, target):
    """Stream a file to disk so large files do not fill memory."""
    print(f"downloading {url}")
    with requests.get(url, stream=True, timeout=120) as response:
        response.raise_for_status()
        with open(target, "wb") as f:
            for chunk in response.iter_content(chunk_size=1 << 20):
                f.write(chunk)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot", help="Inside Airbnb snapshot date, YYYY-MM-DD")
    args = parser.parse_args()

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    snapshot = args.snapshot or latest_snapshot()
    print(f"Inside Airbnb snapshot: {snapshot}")

    for name, path in AIRBNB_FILES.items():
        download(f"{AIRBNB_BASE}/{snapshot}/{path}", RAW_DIR / name)

    # Remember which snapshot was used so the data card can cite it.
    (RAW_DIR / "SNAPSHOT.txt").write_text(snapshot + "\n", encoding="utf-8")
    print("done")


if __name__ == "__main__":
    main()
