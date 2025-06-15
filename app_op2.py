import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    # Load base datasets
    covid = pd.read_csv("data/us-counties-2020.csv", parse_dates=["date"])
    masks = pd.read_csv("data/mask-use-by-county.csv")
    pop = pd.read_csv("data/co-est2019-alldata.csv", encoding='ISO-8859-1')

    # Filter COVID data to July 31, 2020
    covid_july = covid[covid["date"] == "2020-07-31"].copy()
    covid_july = covid_july[["fips", "county", "state", "cases"]]
    covid_july["fips"] = covid_july["fips"].astype("Int64").astype(str).str.zfill(5)

    # Convert COUNTYFP to string in mask data
    masks["fips"] = masks["COUNTYFP"].astype(str).str.zfill(5)

    # Merge COVID and mask data on FIPS
    merged = pd.merge(masks, covid_july, on="fips", how="inner")

    # Prep population data (only county-level rows)
    pop = pop[pop["SUMLEV"] == 50].copy()
    pop["fips"] = pop["STATE"].apply(lambda x: f"{x:02d}") + pop["COUNTY"].apply(lambda x: f"{x:03d}")
    pop = pop[["fips", "POPESTIMATE2019", "STNAME", "CTYNAME"]]
    pop.columns = ["fips", "population", "state_name", "county_name"]

    # Merge population into merged set
    merged = pd.merge(merged, pop, on="fips", how="inner")

    # Rename and calculate derived fields
    merged.rename(columns={"ALWAYS": "always"}, inplace=True)
    merged["cases_per_100k"] = merged["cases"] / merged["population"] * 100000
    #merged["population_density"] = merged["population"] / (merged["land_area"] / 2.59e6)  # sq. miles

    return merged

df = load_data()

#st.dataframe(df.head(20))

st.title("Mask Usage vs. COVID-19 Case Rate (per 100k)")
st.markdown("""
This chart explores the relationship between how often people reported wearing masks (July 2020) and the COVID-19 case rate (cases per 100,000 people) across U.S. counties.
""")

# Filter range using a sidebar slider
st.sidebar.header("Filters")
mask_range = st.sidebar.slider(
    "Always Wear Mask (%)",
    0.0, 1.0,
    (0.5, 0.9),  # default range
    step=0.01
)

filtered_df = df[(df["always"] >= mask_range[0]) & (df["always"] <= mask_range[1])]

# Scatterplot
fig = px.scatter(
    filtered_df,
    x="always",
    y="cases_per_100k",
    hover_data=["county", "state", "cases", "population"],
    labels={
        "always": "Always Wear Mask (%)",
        "cases_per_100k": "Cases per 100k"
    },
    title="Mask Usage vs COVID-19 Cases per 100k"
)

st.plotly_chart(fig, use_container_width=True)
