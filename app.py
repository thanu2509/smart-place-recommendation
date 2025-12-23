import streamlit as st
import pandas as pd

# Sample data
data = {
    "place_name": ["Cafe Aroma","WorkHub Cafe","Budget Bites",
                   "Romantic Rooftop","Quick Snacks","Luxury Dine"],
    "mood": ["work","work","budget","date","quick_bite","date"],
    "rating": [4.6,4.2,3.8,4.9,3.9,4.7],
    "distance_km": [0.5,1.2,2.0,1.5,0.8,2.5],
    "price_level": [2,1,1,3,1,4],
    "is_open": [1,1,1,1,0,1]
}

df = pd.DataFrame(data)

# Rule-based score (no ML to avoid errors)
df["score"] = (
    df["rating"] / 5
    + 1 / (df["distance_km"] + 0.1)
    + 1 / (df["price_level"] + 1)
    + df["is_open"]
)

# UI
st.title("📍 Smart Nearby Places Recommender")

user_mood = st.selectbox("Choose your mood", df["mood"].unique())
st.sidebar.header("🔍 Filters")

min_rating = st.sidebar.slider("Minimum Rating", 1.0, 5.0, 3.5)
max_distance = st.sidebar.slider("Maximum Distance (km)", 0.5, 5.0, 3.0)
max_price = st.sidebar.slider("Max Price Level", 1, 4, 3)


results = df[df["mood"] == user_mood].sort_values("score", ascending=False)

st.subheader("Top Recommendations")
st.dataframe(results[["place_name","rating","distance_km","price_level","score"]])
