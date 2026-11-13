"""Produce every figure used on the site into visuals/.

Static (PNG):
    fig1_price_distribution.png   distribution
    fig2_district_prices.png      comparison across categories
    fig3_monthly_reviews.png      trend over time (busiest districts)
    fig4_price_vs_capacity.png    relationship
Interactive (HTML):
    interactive_districts.html    plotly scatter of districts
Advanced (HTML):
    map_district_prices.html      folium choropleth of median price by district

Run from the repository root, after scripts/preprocess.py:
    python scripts/figures.py
"""

import json
from pathlib import Path

import folium
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
RAW_DIR = ROOT / "data" / "raw"
VISUALS = ROOT / "visuals"

# Okabe-Ito colour-blind-safe palette.
BLUE, ORANGE, GREEN, GREY = "#0072B2", "#E69F00", "#009E73", "#999999"
SOURCE_AIRBNB = "Source: Inside Airbnb, Istanbul snapshot {snapshot}"
PRICE_LABEL = "Nightly price (local currency, as listed)"
TOP_DISTRICTS = 15

plt.rcParams.update({"figure.dpi": 150, "axes.spines.top": False, "axes.spines.right": False})


def add_source(fig, text):
    fig.text(0.01, 0.01, text, fontsize=8, color="#555555", ha="left", va="bottom")


def bootstrap_median_ci(values, n_boot=1000, seed=421):
    """95% bootstrap confidence interval for the median."""
    rng = np.random.default_rng(seed)
    values = np.asarray(values)
    medians = [np.median(rng.choice(values, size=len(values), replace=True)) for _ in range(n_boot)]
    return np.percentile(medians, [2.5, 97.5])


def fig_price_distribution(listings, source):
    prices = listings["price"].dropna()
    median = prices.median()
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bins = np.logspace(np.log10(prices.min()), np.log10(prices.max()), 60)
    ax.hist(prices, bins=bins, color=BLUE)
    ax.set_xscale("log")
    ax.axvline(median, color=ORANGE, linewidth=2)
    ax.annotate(f"median {median:,.0f}", xy=(median, ax.get_ylim()[1] * 0.9),
                xytext=(8, 0), textcoords="offset points", color=ORANGE)
    ax.set_xlabel(PRICE_LABEL + ", log scale")
    ax.set_ylabel("Number of listings")
    ax.set_title(f"Half of Istanbul's listings cost less than {median:,.0f} a night", loc="left")
    add_source(fig, source)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(VISUALS / "fig1_price_distribution.png")
    plt.close(fig)


def fig_district_prices(listings, source):
    priced = listings[listings["price"].notna() & ~listings["price_outlier"]]
    busiest = listings["district"].value_counts().head(TOP_DISTRICTS).index
    rows = []
    for district in busiest:
        values = priced.loc[priced["district"] == district, "price"]
        low, high = bootstrap_median_ci(values)
        rows.append({"district": district, "median": values.median(), "low": low, "high": high})
    table = pd.DataFrame(rows).sort_values("median")

    fig, ax = plt.subplots(figsize=(8, 6))
    colors = [ORANGE if i == len(table) - 1 else BLUE for i in range(len(table))]
    ax.barh(table["district"], table["median"], color=colors,
            xerr=[table["median"] - table["low"], table["high"] - table["median"]],
            error_kw={"ecolor": GREY, "capsize": 3})
    ax.set_xlim(left=0)
    ax.set_xlabel("Median " + PRICE_LABEL.lower() + " (bars: 95% bootstrap CI)")
    top = table.iloc[-1]
    ax.set_title(f"{top['district']} is the priciest of the {TOP_DISTRICTS} busiest districts", loc="left")
    add_source(fig, source)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(VISUALS / "fig2_district_prices.png")
    plt.close(fig)


def fig_monthly_reviews(monthly, source):
    """Monthly reviews for the three busiest districts and all others: at most four lines."""
    monthly = monthly.set_index("month")
    yearly = monthly.groupby(monthly.index.year).sum()
    first, last = 2019, yearly.index.max() - 1  # last complete year
    lead = monthly.columns[0]
    growth = yearly.loc[last, lead] / yearly.loc[first, lead]

    fig, ax = plt.subplots(figsize=(9, 5))
    for column, color in zip(monthly.columns, [ORANGE, BLUE, GREEN, GREY]):
        smooth = monthly[column].rolling(3, center=True).mean()
        ax.plot(monthly.index, smooth, color=color, linewidth=2)
        ax.annotate(column, xy=(monthly.index[-2], smooth.iloc[-2]), xytext=(6, 0),
                    textcoords="offset points", color=color, va="center")
    ax.set_ylim(bottom=0)
    ax.set_ylabel("Reviews per month (3-month average)")
    ax.margins(x=0.12)
    ax.set_title(f"{lead} received {growth:.0f}× more reviews in {last} than in {first}", loc="left")
    add_source(fig, source)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(VISUALS / "fig3_monthly_reviews.png")
    plt.close(fig)


def fig_price_vs_capacity(listings, source):
    data = listings[listings["price"].notna() & listings["accommodates"].between(1, 16)].copy()
    data["guests"] = data["accommodates"].clip(upper=8).astype(int).astype(str).replace("8", "8+")
    order = [str(i) for i in range(1, 8)] + ["8+"]
    groups = [data.loc[data["guests"] == g, "price"] for g in order]
    ratio = groups[5].median() / groups[1].median() if len(groups[1]) and len(groups[5]) else float("nan")

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.boxplot(groups, tick_labels=order, showfliers=False,
               medianprops={"color": ORANGE, "linewidth": 2}, boxprops={"color": BLUE})
    ax.set_yscale("log")
    ax.set_xlabel("Guests the listing accommodates")
    ax.set_ylabel(PRICE_LABEL + ", log scale")
    ax.set_title(f"A 6-guest listing costs {ratio:.1f}× a 2-guest listing at the median", loc="left")
    add_source(fig, source)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(VISUALS / "fig4_price_vs_capacity.png")
    plt.close(fig)


def interactive_districts(districts, snapshot):
    fig = px.scatter(
        districts.dropna(subset=["median_price"]),
        x="listings", y="median_price", size="reviews_total", color="share_entire_home",
        hover_name="district", hover_data={"share_multi_listing_host": ":.0%", "share_entire_home": ":.0%"},
        log_x=True, color_continuous_scale="Cividis",
        labels={
            "listings": "Number of listings (log scale)",
            "median_price": "Median nightly price",
            "share_entire_home": "Share entire home",
            "reviews_total": "Total reviews",
            "share_multi_listing_host": "Share multi-listing hosts",
        },
        title="Districts with more listings: are they also more expensive? Hover a bubble for details",
    )
    fig.update_yaxes(rangemode="tozero")
    fig.add_annotation(text=f"Source: Inside Airbnb, Istanbul snapshot {snapshot}",
                                              xref="paper", yref="paper", x=0, y=-0.28, showarrow=False, font={"size": 10})
    fig.update_layout(margin={"b": 110})
    fig.write_html(VISUALS / "interactive_districts.html", include_plotlyjs="cdn")


def map_district_prices(districts, snapshot):
    with open(RAW_DIR / "neighbourhoods.geojson", encoding="utf-8") as f:
        geo = json.load(f)
    lookup = districts.set_index("district")
    for feature in geo["features"]:
        name = feature["properties"].get("neighbourhood")
        row = lookup.loc[name] if name in lookup.index else None
        feature["properties"]["listings"] = int(row["listings"]) if row is not None else 0
        price = row["median_price"] if row is not None else None
        feature["properties"]["median_price"] = f"{price:,.0f}" if price is not None and pd.notna(price) else "n/a"

    m = folium.Map(location=[41.04, 29.0], zoom_start=10, tiles="OpenStreetMap")
    folium.Choropleth(
        geo_data=geo, data=districts, columns=["district", "median_price"],
        key_on="feature.properties.neighbourhood", fill_color="YlGnBu",
        nan_fill_color="white", fill_opacity=0.75, line_opacity=0.4,
        legend_name="Median nightly price (local currency)",
    ).add_to(m)
    folium.GeoJson(
        geo, style_function=lambda _: {"fillOpacity": 0, "weight": 0},
        tooltip=folium.GeoJsonTooltip(
            fields=["neighbourhood", "listings", "median_price"],
            aliases=["District", "Listings", "Median price"]),
    ).add_to(m)
    m.get_root().html.add_child(folium.Element(
        f'<div style="position:fixed;bottom:8px;left:8px;font-size:11px;background:white;padding:2px 4px">'
        f'Source: Inside Airbnb, Istanbul snapshot {snapshot}</div>'))
    m.save(VISUALS / "map_district_prices.html")


def main():
    VISUALS.mkdir(exist_ok=True)
    snapshot = (RAW_DIR / "SNAPSHOT.txt").read_text().strip()
    listings = pd.read_csv(PROCESSED / "listings_clean.csv")
    districts = pd.read_csv(PROCESSED / "district_summary.csv")
    monthly = pd.read_csv(PROCESSED / "monthly_reviews_district.csv", parse_dates=["month"])

    fig_price_distribution(listings, SOURCE_AIRBNB.format(snapshot=snapshot))
    fig_district_prices(listings, SOURCE_AIRBNB.format(snapshot=snapshot))
    fig_monthly_reviews(monthly, SOURCE_AIRBNB.format(snapshot=snapshot))
    fig_price_vs_capacity(listings, SOURCE_AIRBNB.format(snapshot=snapshot))
    interactive_districts(districts, snapshot)
    map_district_prices(districts, snapshot)
    print(f"figures written to {VISUALS.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
