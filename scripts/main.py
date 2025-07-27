# main.py

from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy import (
    create_engine, Column, Date, String, Float, func
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List
from datetime import date

# === Database setup ===
DB_URL = "sqlite:///./covid.db"
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()

class CovidWeekly(Base):
    __tablename__ = "covid_weekly"
    date = Column(Date, primary_key=True)
    country = Column(String, primary_key=True)
    new_cases = Column(Float)

# Ensure table exists (in production, use migrations)
Base.metadata.create_all(bind=engine)

# === Pydantic schema ===
class CovidSummary(BaseModel):
    country: str
    total_cases: float

# === FastAPI app ===
app = FastAPI(
    title="COVID‑19 Weekly Analytics API",
    description="Serves aggregated weekly new‑cases per country",
    version="1.0",
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get(
    "/analytics/covid",
    response_model=List[CovidSummary],
    summary="Get total weekly cases for a country",
)
def get_covid_stats(
    country: str = Query(..., description="Country name as in the dataset"),
    start: date = Query(..., description="Start date (inclusive)"),
    end: date = Query(..., description="End date (inclusive)"),
    db: Session = Depends(get_db),
):
    """
    Returns the summed new_cases for the given country,
    grouped into weeks, filtered by [start, end].
    """
    # Validate date range
    if end < start:
        raise HTTPException(400, "`end` must be >= `start`")

    q = (
        db.query(
            CovidWeekly.country,
            func.sum(CovidWeekly.new_cases).label("total_cases")
        )
        .filter(CovidWeekly.country == country)
        .filter(CovidWeekly.date.between(start, end))
        .group_by(CovidWeekly.country)
    )
    result = q.one_or_none()
    if not result:
        return []
    return [CovidSummary(country=result.country, total_cases=result.total_cases)]
