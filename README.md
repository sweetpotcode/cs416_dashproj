# CS416 Dashboard Project: Mask Use vs COVID Spread

This Streamlit dashboard visualizes the relationship between mask usage and COVID-19 case rates across U.S. counties in July 2020.

## Features
- Interactive slider to filter by % mask usage
- Scatterplot showing cases per 100k, colored by population density
- Hover tooltips with county-level details


## installation

``` bash
python3 -m venv .cs416
source .cs416/bin/activate
```

## run

streamlit run app.py


## dataset:

2019 U.S. County Population Estimates CSV (Census)
https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/co-est2019-alldata.csv
