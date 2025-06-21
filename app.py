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

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

st.title("COVID-19 Impact vs Vaccination Across U.S. States")

#st.info("Select a year in the left sidebar. If the sidebar is hidden, click the ← arrow at the top left to expand it.")

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

#st.write("Vaccination Rate Summary Stats:")
#st.write(df_latest["vaccination_rate"].describe())

#st.write("Vaccination Rate Distribution Histogram:")
#st.bar_chart(df_latest["vaccination_rate"].value_counts(bins=10).sort_index())

# Categorize vaccination rate
def classify_vax(row):
    if row["vaccination_rate"] >= 78:
        return "Above 1 S.D. (78%+)"
    elif row["vaccination_rate"] >= 68:
        return "Above Mean (68%-78%)"
    else:
        return "Below Mean (<68%)"

df_latest["vax_group"] = df_latest.apply(classify_vax, axis=1)

# Define shape and color maps
shape_map = {
    "Above 1 S.D. (78%+)": "star",
    "Above Mean (68%-78%)": "triangle-up",
    "Below Mean (<68%)": "circle"
}
color_map = {
    "Above 1 S.D. (78%+)": "gold",
    "Above Mean (68%-78%)": "green",
    "Below Mean (<68%)": "red"
}
# End Categorize vaccination rate


# Create scatter plot using shape + color
fig_scatter = px.scatter(
    df_latest,
    x="cases_per_100k",
    y="deaths_per_100k",
    symbol="vax_group",
    symbol_map=shape_map,
    color="vax_group",
    color_discrete_map=color_map,
    hover_name="state",
    labels={
        "cases_per_100k": "Cases per 100k",
        "deaths_per_100k": "Deaths per 100k",
        "vax_group": "Vaccination Level"
    },
    title=f"Deaths vs Cases per 100k (Year: {selected_year})"
)
fig_scatter.update_traces(marker=dict(size=10)) 
#st.plotly_chart(fig_scatter, use_container_width=True)

#st.subheader("Chart 2: Average Deaths per 100k by Vaccination Group")

# Group and calculate mean deaths per 100k
grouped_df = (
    df_latest.groupby("vax_group", as_index=False)
    .agg(avg_deaths_per_100k=("deaths_per_100k", "mean"))
)

# Sort groups for better visual consistency
vax_group_order = ["Below Mean (<68%)", "Above Mean (68%-78%)", "Above 1 S.D. (78%+)"]
grouped_df["vax_group"] = pd.Categorical(grouped_df["vax_group"], categories=vax_group_order, ordered=True)
grouped_df = grouped_df.sort_values("vax_group")

# Bar chart
fig_summary = px.bar(
    grouped_df,
    x="vax_group",
    y="avg_deaths_per_100k",
    color="vax_group",
    color_discrete_map=color_map,
    labels={
        "vax_group": "Vaccination Level",
        "avg_deaths_per_100k": "Average Deaths per 100k"
    },
    title=f"Average Deaths per 100k by Vaccination Level (Year: {selected_year})"
)
#st.plotly_chart(fig_summary, use_container_width=True)


#st.subheader("COVID-19 Outcomes and Grouped Summary")
# Create 2 columns
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Chart 1: Outcomes vs Vaccination Rate")
    st.plotly_chart(fig_scatter, use_container_width=False, width=500, height=400)

with col2:
    st.markdown("### Chart 2: Avg Deaths per 100k by Vax Group")
    st.plotly_chart(fig_summary, use_container_width=False, width=500, height=400)

#st.markdown("---")
st.markdown("#### Datasets and code:")
st.markdown(
    "🔗 The full source code and all datasets used in this dashboard are available at: "
    "[GitHub Repository](https://github.com/sweetpotcode/cs416_dashproj)"
)
