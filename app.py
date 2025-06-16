# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    import pandas as pd

    # Load NYT state-level COVID data (cases + deaths)
    covid = pd.read_csv("data/us-states.csv", parse_dates=["date"])
    covid = covid[["date", "state", "cases", "deaths"]]

    # Load Census population data and filter to state-level rows
    pop = pd.read_csv("data/co-est2019-alldata.csv", encoding='ISO-8859-1')
    pop = pop[pop["SUMLEV"] == 40].copy()
    pop = pop[["STNAME", "POPESTIMATE2019"]]
    pop.columns = ["state", "population"]

    # Merge population to COVID stats (by state name)
    covid = pd.merge(covid, pop, on="state", how="inner")

    # Derived metrics
    covid["cases_per_100k"] = covid["cases"] / covid["population"] * 100000
    covid["deaths_per_100k"] = covid["deaths"] / covid["population"] * 100000

    # Add state abbreviation for map plotting
    abbrev = pd.read_csv("data/state_abbrev.csv")
    covid = pd.merge(covid, abbrev, on="state", how="left")

    # Load and process vaccination data
    vac = pd.read_csv("data/COVID-19_Vaccinations_in_the_United_States_Jurisdiction_20250616.csv", parse_dates=["Date"])
    vac = vac[["Date", "Location", "Series_Complete_Pop_Pct"]]
    vac.columns = ["date", "state_code", "vaccination_rate"]

    # Merge vaccination data by date and state_code
    df = pd.merge(covid, vac, on=["date", "state_code"], how="left")

    return df

df = load_data()

st.title("COVID-19 Impact vs Vaccination Across U.S. States")

# Sidebar: Date selection
st.sidebar.header("Filters")

# Extract available years from date column
available_years = sorted(df["date"].dt.year.unique())
selected_year = st.sidebar.selectbox("Select a year", available_years, index=len(available_years) - 1)

# Filter by year
df_year = df[df["date"].dt.year == selected_year]

# Aggregate: take last (max date) entry per state
df_latest = df_year.sort_values("date").groupby("state", as_index=False).last()

# Drop rows with missing values
df_latest = df_latest.dropna(subset=["cases_per_100k", "deaths_per_100k", "vaccination_rate"])


st.subheader("COVID-19 Outcomes vs Vaccination Rate")

fig_scatter = px.scatter(
    df_latest,
    x="cases_per_100k",
    y="deaths_per_100k",
    color="vaccination_rate",
    hover_name="state",
    color_continuous_scale="Viridis",
    labels={
        "cases_per_100k": "Cases per 100k",
        "deaths_per_100k": "Deaths per 100k",
        "vaccination_rate": "Vaccination %"
    },
    title=f"Deaths vs Cases per 100k (Year: {selected_year})"
)
st.plotly_chart(fig_scatter, use_container_width=True)

st.subheader("Vaccination Rates by State")

df_sorted_vax = df_latest.sort_values("vaccination_rate", ascending=False)

fig_bar = px.bar(
    df_sorted_vax,
    x="state",
    y="vaccination_rate",
    color="vaccination_rate",
    color_continuous_scale="Blues",
    labels={"vaccination_rate": "Vaccination %"},
    title=f"State Vaccination Rates (Year: {selected_year})"
)
st.plotly_chart(fig_bar, use_container_width=True)
