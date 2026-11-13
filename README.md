# IE 421 - Data Science for Engineers Term Project

## Airbnb in Istanbul: Comparing the Districts

Short-term rentals shape how a city is lived in: they take homes away from long-term residents and bring visitors into residential streets. Under the theme "Cities We Live In: homes and bike-share", this project compares Istanbul's districts using the public Inside Airbnb snapshot of the city from 25 September 2026. We ask three questions. First, how do nightly prices differ across districts? Second, which districts concentrate the listings, and how has guest activity in them grown over time? Third, how do districts differ in the kind of supply they offer, entire homes or rooms, single hosts or hosts with many listings, and how is price related to listing size? To answer them we join three Inside Airbnb files: about 27,000 listings, more than 600,000 guest reviews and the boundaries of the 39 districts. Prices are parsed from text, dates are parsed with one explicit rule, duplicates and missing values are handled deliberately, and every decision is recorded in the data card. The results are shown as four static figures, an interactive district chart and a district price map on our GitHub Pages site. Reviews are only a proxy for stays, so the findings describe patterns, not causes.

## Student Names

- Tuğçe Turgut (122203075)
- Yaren Polat (123203024)

Site: https://bilgi-ie-421.github.io/ie421-2026-2027-1-termproject-group-5/

## Files (Explain each of them with a sentence)

- `data/`: The data card (`data/README.md`); raw downloads go to `data/raw/` (not committed) and cleaned, aggregated tables to `data/processed/`.
- `scripts/download_data.py`: Downloads the Inside Airbnb Istanbul files (listings, reviews, district boundaries) into `data/raw/`.
- `scripts/preprocess.py`: Cleans listings (prices, dates, duplicates, outliers), joins reviews to listings, reshapes monthly reviews to one column per district (pivot) and writes the tables in `data/processed/`.
- `scripts/eda.ipynb`: Exploratory analysis: first contact, one variable at a time, then relationships.
- `scripts/figures.py`: Produces every figure in `visuals/`.
- `visuals/`: Figures used on the site: price distribution, district price comparison, monthly reviews in the busiest districts, price vs. capacity, an interactive district chart (plotly) and a district price map (folium).
- `index.html` and `css/`: The project website served by GitHub Pages.
- `PROPOSAL.md`: Milestone 1 proposal: problem, datasets and research questions.
- `AI_USAGE.md`: Every use of AI tools, where it is used and how it was checked.
- `requirements.txt`: Python libraries the scripts import.
- `.github/`: The automatic repository check provided with the template.

## How to run (from the repository root)

```
pip install -r requirements.txt
python scripts/download_data.py
python scripts/preprocess.py
python scripts/figures.py
jupyter notebook scripts/eda.ipynb
```

`download_data.py` uses the newest Istanbul snapshot listed on Inside Airbnb; pass `--snapshot YYYY-MM-DD` to reproduce a specific one.

## Key findings

Findings will be added after the analysis is complete (three sentences with numbers in context).

## Hosting

https://bilgi-ie-421.github.io/ie421-2026-2027-1-termproject-group-5/
