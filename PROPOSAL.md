# Airbnb in Istanbul: Comparing the Districts

**Team:** group-5 · **Theme:** T6 Cities We Live In: homes and bike-share

**Members:** Tuğçe Turgut (122203075) · Yaren Polat (123203024)

## The problem
Airbnb has become a popular accommodation option in Istanbul, especially in areas visited by tourists. We want to compare Istanbul's districts by looking at where Airbnb listings are located, how nightly prices differ, how guest activity has changed over time, and whether prices are related to guest ratings. This will help us understand how Airbnb activity differs across Istanbul.

## The data
| Dataset | Link | What is in it |
|---|---|---|
| Inside Airbnb – Istanbul listings (`listings.csv.gz`) | https://insideairbnb.com/get-the-data/ | One row per listing: district, coordinates, room type, capacity, nightly price, host, rating. Snapshot of 25 September 2026. |
| Inside Airbnb – Istanbul reviews (`reviews.csv`) | https://insideairbnb.com/get-the-data/ | One row per guest review (listing id, date), 2011–2026; joined to listings on the listing id. |
| Inside Airbnb – Istanbul districts (`neighbourhoods.geojson`) | https://insideairbnb.com/get-the-data/ | Boundaries of Istanbul's 39 districts (GeoJSON), joined to listings on the district name for the map. |

## Our questions
1. How do Airbnb prices vary between different districts in Istanbul?
2. Which districts in Istanbul have the most Airbnb listings, and how has guest activity changed over time in these districts?
3. Is there a relationship between Airbnb prices and guest ratings in Istanbul?
