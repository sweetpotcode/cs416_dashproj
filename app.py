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

st.dataframe(df.head(20))