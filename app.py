import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    import pandas as pd

    # Load and filter NYT state-level COVID data
    covid = pd.read_csv("data/us-states.csv", parse_dates=["date"])
    covid_july = covid[covid["date"] == "2020-07-31"].copy()
    covid_july = covid_july[["state", "cases", "deaths"]]

    # Load Census population data and filter to state-level rows only
    pop = pd.read_csv("data/co-est2019-alldata.csv", encoding='ISO-8859-1')
    pop = pop[pop["SUMLEV"] == 40].copy()
    pop = pop[["STNAME", "POPESTIMATE2019"]]
    pop.columns = ["state", "population"]

    # Merge on state name
    df = pd.merge(covid_july, pop, on="state", how="inner")

    # Calculate derived metric
    df["cases_per_100k"] = df["cases"] / df["population"] * 100000

    return df

df = load_data()

#st.dataframe(df.head(20))

st.title("COVID-19 Impact by State: Case Rate Rankings as of July 2020")
#st.caption("This dashboard ranks U.S. states by their COVID-19 case rates per 100,000 residents, providing a snapshot of relative impact as of July 31, 2020.")

# Sort for visualization
df_sorted = df.sort_values("cases_per_100k", ascending=False)

# Plot with Plotly
fig = px.bar(
    df_sorted,
    x="cases_per_100k",
    y="state",
    orientation="h",
    title="COVID-19 Case Rate per 100,000 Residents (by State)",
    labels={"cases_per_100k": "Cases per 100k", "state": "State"},
    color="cases_per_100k",
    color_continuous_scale="Reds"
)

st.plotly_chart(fig, use_container_width=True)
