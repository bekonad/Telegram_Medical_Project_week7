# pipeline.py

import pandas as pd
from dagster import op, graph, ScheduleDefinition, Definitions
from sqlalchemy import create_engine

# SQLite URL for demo
DB_URL = "sqlite:///./covid.db"

@op
def extract_covid() -> pd.DataFrame:
    """Download the raw CSV of daily new cases per country."""
    url = (
        "https://raw.githubusercontent.com/owid/"
        "covid-19-data/master/public/data/jhu/new_cases.csv"
    )
    df = pd.read_csv(url)
    # Ensure date column is datetime
    df["date"] = pd.to_datetime(df["date"])
    return df

@op
def transform_covid(df: pd.DataFrame) -> pd.DataFrame:
    """Melt and compute weekly new‐cases sums per country."""
    # Convert wide → long
    melted = df.melt(
        id_vars=["date"], var_name="country", value_name="new_cases"
    ).dropna(subset=["new_cases"])
    # Resample to weekly sums
    weekly = (
        melted.set_index("date")
              .groupby("country")["new_cases"]
              .resample("W-MON")  # weeks ending Monday
              .sum()
              .reset_index()
    )
    return weekly

@op
def load_covid_weekly(weekly: pd.DataFrame):
    """Write the weekly totals into a SQLite table."""
    engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
    # Table schema: date (date), country (str), new_cases (float)
    weekly.to_sql(
        "covid_weekly", engine,
        if_exists="replace",
        index=False,
        dtype={
            "date": "DATE",
            "country": "TEXT",
            "new_cases": "REAL",
        },
    )

@graph
def covid_etl():
    """Full ETL: extract → transform → load."""
    load_covid_weekly(transform_covid(extract_covid()))

# Create a job from the graph
covid_etl_job = covid_etl.to_job()

# Schedule it to run every day at 1 AM
daily_schedule = ScheduleDefinition(
    job=covid_etl_job,
    cron_schedule="0 1 * * *",
)

# IMPORTANT: Register your jobs and schedules with Definitions
defs = Definitions(
    jobs=[covid_etl_job],
    schedules=[daily_schedule],
)