# Airbnb in Istanbul: Comparing the Districts

**Team:** group-5 · **Theme:** T6 Cities We Live In: homes and bike-share

**Members:** Tuğçe Turgut (122203075) · Yaren Polat (123203024)

## The problem
Short-term rentals change how a city is lived in: they take homes off the long-term market and bring tourists into residential neighbourhoods. We want to compare Istanbul's districts: where Airbnb listings are concentrated, how nightly prices differ, how fast guest activity has grown, and who offers the listings. Knowing this shows which districts carry most of the tourism footprint.

## The data
| Dataset | Link | What is in it |
|---|---|---|
| Inside Airbnb – Istanbul listings (`listings.csv.gz`) | https://insideairbnb.com/get-the-data/ | One row per listing: district, coordinates, room type, capacity, nightly price, host, rating. Snapshot of 25 September 2026. |
| Inside Airbnb – Istanbul reviews (`reviews.csv`) | https://insideairbnb.com/get-the-data/ | One row per guest review (listing id, date), 2011–2026; joined to listings on the listing id. |
| Inside Airbnb – Istanbul districts (`neighbourhoods.geojson`) | https://insideairbnb.com/get-the-data/ | Boundaries of Istanbul's 39 districts (GeoJSON), joined to listings on the district name for the map. |

## Our questions
1. How do nightly prices differ across Istanbul's districts?
2. Which districts concentrate the listings, and how has guest activity in them grown over time?
3. How do districts differ in the kind of supply (entire homes vs. rooms, single vs. multi-listing hosts), and how is price related to listing size?
