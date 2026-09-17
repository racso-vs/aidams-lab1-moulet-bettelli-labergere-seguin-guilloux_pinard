# Import streamlit and other necessary libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Global Steel Plants Dashboard", layout="wide")

# Title and description
st.title("Global Steel Plants Dashboard")
st.markdown(
    "Explore steel plant locations, capacity, and (for China/India/Japan) "
    "nearby LitPop asset exposure. Data: Global Energy Monitor Iron & Steel "
    "Tracker + ETH Zurich LitPop."
)

# Load the data exported in the notebook (Part 6, Exercise "Prepare Data for Dashboard")
plants = pd.read_csv("plants_clean.csv")

# Sidebar for filters
st.sidebar.header("Filters")

# Company selector: empty selection = no filter (all companies), avoids a
# 1069-item dropdown forcing the user to pick one before seeing anything
companies = st.sidebar.multiselect("Company (Owner)", sorted(plants["Owner"].unique()))

# Region/country filter
regions = st.sidebar.multiselect("Region", sorted(plants["Region"].unique()))
countries = st.sidebar.multiselect("Country/area", sorted(plants["Country/area"].unique()))

# Capacity range slider (based on plants that actually have a known capacity)
cap_min = int(plants["Capacity (ttpa)"].min(skipna=True))
cap_max = int(plants["Capacity (ttpa)"].max(skipna=True))
cap_range = st.sidebar.slider("Capacity range (ttpa)", cap_min, cap_max, (cap_min, cap_max))

# Apply filters (empty multiselect = don't filter on that field)
filtered = plants.copy()
if companies:
    filtered = filtered[filtered["Owner"].isin(companies)]
if regions:
    filtered = filtered[filtered["Region"].isin(regions)]
if countries:
    filtered = filtered[filtered["Country/area"].isin(countries)]
# capacity comparison drops rows with NaN capacity automatically (NaN comparisons are False)
filtered = filtered[
    (filtered["Capacity (ttpa)"] >= cap_range[0]) & (filtered["Capacity (ttpa)"] <= cap_range[1])
]

# Main content area
# KPI metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Plants shown", f"{len(filtered):,}")
col2.metric("Total capacity (ttpa)", f"{filtered['Capacity (ttpa)'].sum():,.0f}")
col3.metric("Companies", f"{filtered['Owner'].nunique():,}")
col4.metric("Countries", f"{filtered['Country/area'].nunique():,}")

# Interactive map
st.subheader("Plant locations")
if filtered.empty:
    st.warning("No plants match the current filters.")
else:
    map_df = filtered.dropna(subset=["Capacity (ttpa)"])
    map_df = map_df[map_df["Capacity (ttpa)"] > 0]  # size can't handle NaN/0
    fig = px.scatter_map(
        map_df,
        lat="Latitude", lon="Longitude",
        size="Capacity (ttpa)", color="Region",
        hover_name="Plant name (English)",
        hover_data=["Owner", "Country/area", "Capacity (ttpa)"],
        color_discrete_sequence=px.colors.qualitative.Bold,
        size_max=25, zoom=1, height=550,
    )
    fig.update_traces(marker=dict(opacity=0.8))
    fig.update_layout(map_style="carto-positron", margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig, use_container_width=True)

# Data table
st.subheader("Plant data")
st.dataframe(filtered, use_container_width=True)

# Footer with data sources and notes
st.markdown("---")
st.caption(
    "Sources: Global Energy Monitor Global Iron and Steel Tracker (June 2026) "
    "and ETH Zurich LitPop (sample limited to China, India, Japan). "
    "\"Capacity\" = summed nominal crude steel capacity of currently operating "
    "production units per plant."
)
