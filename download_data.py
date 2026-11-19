"""Download the raw data into data/raw/.

Source
- Inside Airbnb, Istanbul, snapshot 2026-09-25 (fixed, so every run gets the same data):
  listings.csv.gz (detailed listings), reviews.csv (summary reviews: listing id and date),
  neighbourhoods.geojson (district boundaries)

Run from the repository root:
    python scripts/download_data.py

Inside Airbnb keeps roughly the last 12 months of snapshots online; if this snapshot has
been archived, request it from Inside Airbnb ("archived data request") and put the three
files in data/raw/ with the names above.
"""

from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"

AIRBNB_BASE = "https://data.insideairbnb.com/turkey/marmara/istanbul"
SNAPSHOT = "2026-09-25"  # fixed on purpose: never "latest", so the data do not change between runs
AIRBNB_FILES = {
    "listings.csv.gz": "data/listings.csv.gz",
    "reviews.csv": "visualisations/reviews.csv",
    "neighbourhoods.geojson": "visualisations/neighbourhoods.geojson",
}


def download(url, target):
    """Stream a file to disk so large files do not fill memory."""
    print(f"downloading {url}")
    with requests.get(url, stream=True, timeout=120) as response:
        response.raise_for_status()
        with open(target, "wb") as f:
            for chunk in response.iter_content(chunk_size=1 << 20):
                f.write(chunk)


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Inside Airbnb snapshot: {SNAPSHOT}")

    for name, path in AIRBNB_FILES.items():
        download(f"{AIRBNB_BASE}/{SNAPSHOT}/{path}", RAW_DIR / name)

    # Record the snapshot so preprocess.py and the data card use the same date.
    (RAW_DIR / "SNAPSHOT.txt").write_text(SNAPSHOT + "\n", encoding="utf-8")
    print("done")


if __name__ == "__main__":
    main()
