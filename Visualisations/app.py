"""
Streamlit app — Top-N Hotels by City

Purpose:
    - Load the enriched dataset (hotels + coordinates).
    - Let the user select a city, a minimum rating, and N hotels.
    - Show hotels on a Folium map with colored markers.

Inputs:
    - CSV path: default "data/hotels_weather_final_ter.csv"

Output:
    - Interactive map + UI (no file output)

Notes:
    - Dataset is cached with st.cache_data.
    - Marker color: 🟢 ≥ 9.0, 🟠 8.0–8.9, 🔴 < 8.0.
"""

import html

import folium
import pandas as pd
import streamlit as st
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium


CSV_PATH = "data/hotels_weather_final_ter.csv"


def color_by_rating(r: float) -> str:
    """Map a rating to a Folium marker color."""
    if pd.isna(r):
        return "gray"
    if r >= 9.0:
        return "green"
    if r >= 8.0:
        return "orange"
    return "red"


@st.cache_data(show_spinner=False)
def load_data(path: str) -> pd.DataFrame:
    """Load and lightly clean the hotels dataset."""
    df = pd.read_csv(path, encoding="utf-8-sig")

    # Keep only rows with rating and valid coordinates.
    df = df.dropna(
        subset=["hotel_rating", "hotel_latitude", "hotel_longitude"]
    )
    df["hotel_rating"] = pd.to_numeric(df["hotel_rating"], errors="coerce")
    df = df.dropna(subset=["hotel_rating"])
    return df


# Load data.
df = load_data(CSV_PATH)


# Sidebar filters.
with st.sidebar:
    st.markdown("### Filtres")
    cities = sorted(df["city_name"].dropna().unique())
    selected_city = st.selectbox("Choisir une ville", cities, index=0)
    min_rating = st.slider("Note minimale", 6.0, 10.0, 9.0, 0.1)
    top_n = st.slider("Nombre d'hôtels", 5, 25, 20, 5)

# Filter & sort
city_df = (
    df[df["city_name"] == selected_city]
    .sort_values(by="hotel_rating", ascending=False)
)
city_df = city_df[city_df["hotel_rating"] >= min_rating].head(top_n)

# Empty state
if city_df.empty:
    st.warning(f"Aucun hôtel ne correspond aux critères pour **{selected_city}**.")
    st.stop()

# City title.
nb_hotels = len(city_df)
st.markdown(
    f"""
    <h1 style='text-align:center; margin-bottom:30px;'>
        Top {nb_hotels} Hôtels à {html.escape(selected_city)}
    </h1>
    """,
    unsafe_allow_html=True,
)

# Build map (auto-center + auto-zoom).
hotel_map = folium.Map(tiles="OpenStreetMap")
bounds = city_df[["hotel_latitude", "hotel_longitude"]].values.tolist()
hotel_map.fit_bounds(bounds)

# Cluster markers only if many points.
cluster_parent = (
    MarkerCluster().add_to(hotel_map) if nb_hotels > 10 else hotel_map
)

for _, row in city_df.iterrows():
    name = row.get("hotel_name", "Unknown Hotel")
    rating = row.get("hotel_rating", None)
    url = row.get("hotel_url", "#")
    desc = row.get("hotel_description", "")

    safe_name = html.escape(str(name))
    safe_desc_raw = html.escape(str(desc))
    safe_desc = safe_desc_raw[:300] + (
        "..." if len(safe_desc_raw) > 300 else ""
    )
    rating_txt = f"{rating:.1f}" if pd.notna(rating) else "N/A"

    popup_html = f"""
    <div style="font-size:13px; line-height:1.3;">
      <strong>{safe_name}</strong><br>
      <em>Note:</em> {rating_txt}<br>
      <em>Description:</em> {safe_desc}<br>
      <a href="{html.escape(str(url))}" target="_blank"
         rel="noopener noreferrer">🔗 Voir sur Booking</a>
    </div>
    """

    folium.Marker(
        location=[row["hotel_latitude"], row["hotel_longitude"]],
        popup=folium.Popup(popup_html, max_width=320),
        icon=folium.Icon(
            color=color_by_rating(row["hotel_rating"]),
            icon="info-sign",
        ),
    ).add_to(cluster_parent)

# Render map.
st_folium(hotel_map, width=1000, height=600)

# Legend.
st.markdown("**Légende:** 🟢 ≥ 9.0 🟠 8.0–8.9 🔴 < 8.0")
