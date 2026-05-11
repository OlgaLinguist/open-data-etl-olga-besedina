# ============================================================
# ETL Mini-Project: Lisbon Weather Analysis
# Source: Open-Meteo API (https://open-meteo.com/)
# Author: Olga Besedina
# ============================================================
# PIPELINE:
# EXTRACT  → fetch daily weather data from Open-Meteo API
# TRANSFORM → clean columns, compute new metrics, aggregate
# LOAD     → save processed CSV to data/processed/output.csv
# ============================================================

import requests
import pandas as pd
import os
from datetime import date, timedelta

# ============================================================
# EXTRACT
# ============================================================

print("EXTRACT: Fetching weather data from Open-Meteo API...")

end_date = date.today()
start_date = end_date - timedelta(days=90)

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 38.72,
    "longitude": -9.14,
    "daily": [
        "temperature_2m_max",
        "temperature_2m_min",
        "precipitation_sum",
        "windspeed_10m_max"
    ],
    "start_date": str(start_date),
    "end_date": str(end_date),
    "timezone": "Europe/Lisbon"
}

response = requests.get(url, params=params)
response.raise_for_status()
data = response.json()

df_raw = pd.DataFrame(data["daily"])
print(f"Extracted {len(df_raw)} rows")
print(df_raw.head())

# ============================================================
# TRANSFORM
# ============================================================

print("\nTRANSFORM: Cleaning and processing data...")

# 1. Переименовываем колонки
df = df_raw.rename(columns={
    "time": "date",
    "temperature_2m_max": "temp_max_c",
    "temperature_2m_min": "temp_min_c",
    "precipitation_sum": "precipitation_mm",
    "windspeed_10m_max": "windspeed_max_kmh"
})

# 2. Преобразуем дату из текста в datetime
df["date"] = pd.to_datetime(df["date"])

# 3. Считаем среднюю температуру за день
df["temp_avg_c"] = (df["temp_max_c"] + df["temp_min_c"]) / 2

# 4. Добавляем колонку месяца
df["month"] = df["date"].dt.to_period("M").astype(str)

# 5. Убираем строки с пропусками
rows_before = len(df)
df = df.dropna()
print(f"Rows after cleaning: {len(df)} (removed {rows_before - len(df)})")

# 6. Агрегация по месяцам
monthly = df.groupby("month").agg(
    avg_temp_max=("temp_max_c", "mean"),
    avg_temp_min=("temp_min_c", "mean"),
    avg_temp=("temp_avg_c", "mean"),
    total_precipitation=("precipitation_mm", "sum"),
    avg_windspeed=("windspeed_max_kmh", "mean"),
    days=("date", "count")
).reset_index().round(2)

print("\nMonthly summary:")
print(monthly)

# ============================================================
# LOAD
# ============================================================

print("\nLOAD: Saving processed data...")

os.makedirs("data/processed", exist_ok=True)

df.to_csv("data/processed/output.csv", index=False)
print(f"Saved {len(df)} rows to data/processed/output.csv")

monthly.to_csv("data/processed/monthly_summary.csv", index=False)
print(f"Saved monthly summary to data/processed/monthly_summary.csv")

print("\nDone! ETL pipeline completed successfully.")
print("\nOutput preview:")
print(df.head())
