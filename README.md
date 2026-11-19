# IE 421 - Data Science for Engineers Term Project

## Airbnb in Istanbul: Comparing the Districts

Airbnb has become a popular accommodation option in Istanbul, especially in areas visited by tourists. Under the theme "Cities We Live In: homes and bike-share", our project focuses on comparing Airbnb activity across different districts of Istanbul. We want to understand how prices, listing numbers, and guest ratings vary across the city.

Our project aims to answer three main questions. First, how do Airbnb prices vary between different districts in Istanbul? Second, which districts have the most Airbnb listings, and how has guest activity changed over time in these areas? Third, is there a relationship between Airbnb prices and guest ratings?

To answer these questions, we use publicly available data from Inside Airbnb, including listing information, guest reviews, and district boundaries. The dataset provides details such as nightly prices, locations, review dates, and guest ratings. We will clean and organize the data before analyzing it and creating different visualizations, including charts and maps.

Through this project, we hope to identify patterns in Airbnb prices, listing distribution, and review activity. Our findings will help us better understand how Airbnb activity differs between Istanbul's districts.

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

`download_data.py` always downloads the same Inside Airbnb snapshot (2026-09-25), so the results do not change between runs.

## Key findings

Findings will be added after the analysis is complete (three sentences with numbers in context).

## Hosting

https://bilgi-ie-421.github.io/ie421-2026-2027-1-termproject-group-5/
