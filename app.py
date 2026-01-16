import streamlit as st
import pandas as pd
import numpy as np

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Smart Restaurant Recommendation", layout="wide")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("places.csv")
    return df

df = load_data()

# ---------------- MOOD ASSIGNMENT (BASED ON RESTAURANT TYPE) ----------------
def assign_mood_by_type(rest_type, cost):
    rest_type = str(rest_type).lower()
    cost = float(cost)

    # Work → calm places
    if any(x in rest_type for x in ["cafe", "bakery"]):
        return "Work"

    # Budget Friendly → low cost
    elif cost <= 300:
        return "Budget Friendly"

    # Date → fine dining, romantic
    elif any(x in rest_type for x in ["fine dining", "lounge"]):
        return "Date"

    # Quick Bite → fast service
    elif any(x in rest_type for x in ["quick bites", "fast food"]):
        return "Quick Bite"

    # Party → pubs & bars
    elif any(x in rest_type for x in ["bar", "pub", "brewery"]):
        return "Party"

    # Happy → desserts, cafes
    elif any(x in rest_type for x in ["dessert", "ice cream", "cafe"]):
        return "Happy"

    # Family → default safe option
    else:
        return "Family"


# Create Mood column
df["Mood"] = df.apply(
    lambda x: assign_mood_by_type(
        x["restaurant type"], x["avg cost (two people)"]
    ),
    axis=1
)

# ---------------- UI ----------------
st.title("🍽 Smart Restaurant Recommendation System")
st.markdown("### 🎭 Choose your mood and find the perfect place to eat!")
st.write("Recommendations are generated based on restaurant type, budget, rating, and availability.")

# ---------------- SIDEBAR ----------------
st.sidebar.header("🎯 Filter your choices")

# Mood filter
moods = ["Work", "Budget Friendly", "Date", "Quick Bite", "Party", "Happy", "Family"]
selected_mood = st.sidebar.selectbox("Choose Your Mood", moods)

# Area filter
areas = sorted(df["area"].dropna().unique())
selected_area = st.sidebar.selectbox("Select Area", areas)

# Budget filter
max_budget = int(df["avg cost (two people)"].astype(float).max())
budget = st.sidebar.slider(
    "Maximum Budget for Two People", 100, max_budget, 500
)

# Rating filter
min_rating = st.sidebar.slider(
    "Minimum Rating", 0.0, 5.0, 3.5, 0.1
)

# Online order filter
online_order = st.sidebar.selectbox(
    "Online Order Available", ["All", "Yes", "No"]
)

# Table booking filter
table_booking = st.sidebar.selectbox(
    "Table Booking Available", ["All", "Yes", "No"]
)

# ---------------- FILTERING ----------------
filtered = df.copy()

filtered = filtered[filtered["Mood"] == selected_mood]
filtered = filtered[filtered["area"] == selected_area]
filtered = filtered[filtered["avg cost (two people)"].astype(float) <= budget]
filtered = filtered[filtered["rate (out of 5)"].astype(float) >= min_rating]

if online_order != "All":
    filtered = filtered[filtered["online_order"] == online_order]

if table_booking != "All":
    filtered = filtered[filtered["table booking"] == table_booking]

# ---------------- SCORING SYSTEM ----------------
filtered["rating_norm"] = filtered["rate (out of 5)"].astype(float) / 5
filtered["price_norm"] = 1 - (
    filtered["avg cost (two people)"].astype(float) / max_budget
)

filtered["score"] = (
    filtered["rating_norm"] * 0.6 +
    filtered["price_norm"] * 0.4
)

recommended = filtered.sort_values(by="score", ascending=False)

# ---------------- DISPLAY ----------------
st.subheader(f"🔝 Top {selected_mood} Restaurants For You")

if recommended.empty:
    st.warning("No restaurants found with the selected filters.")
else:
    st.dataframe(
        recommended[[
            "restaurant name",
            "restaurant type",
            "Mood",
            "rate (out of 5)",
            "num of ratings",
            "avg cost (two people)",
            "online_order",
            "table booking",
            "area",
            "local address",
            "score"
        ]].head(10),
        use_container_width=True
    )

# ---------------- DATASET VIEW ----------------
with st.expander("📂 View Full Dataset"):
    st.dataframe(df, use_container_width=True)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption(
    "Developed as a real-world smart restaurant recommendation system using Streamlit & Data Science"
)



