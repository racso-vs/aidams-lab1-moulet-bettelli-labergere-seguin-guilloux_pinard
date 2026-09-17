# AIDAMS Lab 1 — Global Steel Plants Geospatial Analysis

Group: Adrien Labergere, Louis Bettelli, Oscar Moulet, Juliette Guilloux-Pinard, Apolline Seguin

## What's here

- `lab_1.ipynb` — the full analysis: EDA, Plotly maps, LitPop exposure matching, company-level aggregation
- `app.py` — Streamlit dashboard built from the notebook's outputs
- `requirements.txt` — dependencies for `app.py`
- `Plant-level_data_Global_Iron_and_Steel_Tracker_June_2026_V1.xlsx` — source plant data (Global Energy Monitor)
- `litpop/` — LitPop exposure samples (ETH Zurich), one `.hdf5` per country (China, India, Japan only)
- `plants_clean.csv`, `plants_litpop.csv`, `company_agg.csv` — processed data exported by the notebook, consumed by `app.py`

## Running the notebook

```bash
pip install pandas numpy plotly h5py tables scikit-learn nbformat
jupyter notebook lab_1.ipynb
```

Run the cells top to bottom — later cells (LitPop matching, company aggregation, data export) depend on
`df` and `df_enriched` built earlier in the notebook.

## Running the dashboard

```bash
pip install -r requirements.txt
streamlit run app.py
```

`app.py` reads the pre-exported `plants_clean.csv` (already in this repo), so it runs standalone without
needing the notebook or the raw data files.

## Note on data coverage

The LitPop exposure sample only covers **China, India, and Japan** — so exposure-related fields
(`litpop_asset_value`, `litpop_value_50km`) are only available for the 613 plants located in those
3 countries, out of 1293 worldwide.
