""" assumptions.py

This file is NOT run on its own. It just holds small helper functions that every other script imports, so we don't repeat the same CSV-parsing code
seven times. The CSV has one row per assumption, and one column per year (Year 1..Year 5). This file turns rows into clean pandas Series/floats that are easy to work with, e.g:
    growth = get_yearly_row("Revenue Growth")   -> Series indexed Year 1..5
    opening_cash = get_single_value("Opening Cash")   -> a plain float """

import pandas as pd

INPUT_CSV = "project_2_assumptions_and_drivers.csv"
YEARS = [f"Year {i}" for i in range(1, 6)]

# Load the CSV once, when this file is imported.
driver_df = pd.read_csv(INPUT_CSV, encoding="latin1")


def get_yearly_row(assumption_name):
    """ Return one assumption's Year 1..Year 5 values as a pandas Series of floats. Strips out % signs, commas, and turns "-" (meaning "no value") into 0.
    Percentages are converted to decimals (e.g. "15.00%" -> 0.15). """
    row = driver_df.loc[driver_df["Assumption"] == assumption_name, YEARS].iloc[0]
    is_percent = row.astype(str).str.contains("%").any()

    row = row.astype(str).str.replace("[%,]", "", regex=True).str.strip()
    row = row.replace("-", "0")
    row = row.astype(float)

    if is_percent:
        row = row / 100.0
    return row


def get_single_value(assumption_name):
    """ Return a single opening/driver value (e.g. Opening Cash), read from the Year 1 column. Handles values like "?60,000" or "25%". """
    raw = str(driver_df.loc[driver_df["Assumption"].str.strip() == assumption_name, "Year 1"].iloc[0])
    raw = raw.replace("?", "").replace(",", "").replace("%", "").strip()
    value = float(raw.split()[0])

    if "%" in str(driver_df.loc[driver_df["Assumption"].str.strip() == assumption_name, "Year 1"].iloc[0]):
        value = value / 100.0
    return value


def revenue_series():
    """ Build the Revenue line for Year 1..Year 5 by growing Opening Revenue using the Revenue Growth assumption. Several other scripts need this,
    so it lives here rather than being repeated."""
    growth = get_yearly_row("Revenue Growth")
    opening_revenue = get_single_value("Opening Revenue")

    revenue = {}
    previous_year_revenue = opening_revenue
    for year in YEARS:
        previous_year_revenue = previous_year_revenue * (1 + growth[year])
        revenue[year] = previous_year_revenue
    return pd.Series(revenue)
