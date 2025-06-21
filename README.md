# CS416 Dashboard Project: COVID-19 Impact vs Vaccination Across U.S. States

This dashboard explores the relationship between COVID-19 outcomes and vaccination rates across U.S. states. Users can interactively select a year to compare both individual and group-level trends in COVID-19 death rates relative to vaccination coverage.

## Features

- **Year selector** in the sidebar for temporal comparison
- **Scatterplot** of states showing COVID-19 deaths vs. cases per 100k, with marker shape and color indicating vaccination level
- **Grouped bar chart** summarizing average deaths per 100k by vaccination tier
- **Consistent color and shape encodings** for vaccination groups across both charts
- **Interactive tooltips** providing details on demand

## publish on
Streamlit Community Cloud: [https://cs416-su2025-dashproj-st-fung2.streamlit.app/](https://cs416-su2025-dashproj-st-fung2.streamlit.app/)

## Installation in local

```bash
python3 -m venv .cs416
source .cs416/bin/activate

pip install -r requirements.txt
```

## Run the app

```bash
streamlit run app.py
```

## Datasets Used

* **U.S. State-Level COVID-19 Cases and Deaths**
  New York Times COVID-19 Data: [https://github.com/nytimes/covid-19-data](https://github.com/nytimes/covid-19-data)

* **2019 U.S. State Population Estimates**
  U.S. Census Bureau: [https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/co-est2019-alldata.csv](https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/co-est2019-alldata.csv)

* **CDC Vaccination Data by Jurisdiction**
  COVID-19 Vaccination Data (archived snapshot as of 2025-06-16)[https://data.cdc.gov/Vaccinations/COVID-19-Vaccinations-in-the-United-States-Jurisdi/unsk-b7fc?utm_source=chatgpt.com](https://data.cdc.gov/Vaccinations/COVID-19-Vaccinations-in-the-United-States-Jurisdi/unsk-b7fc?utm_source=chatgpt.com)
