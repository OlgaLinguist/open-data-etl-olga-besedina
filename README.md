# open-data-etl-olga-besedina
ETL pipeline for Lisbon weather data
# Lisbon Weather ETL Pipeline

## Data Source
Open-Meteo API — https://open-meteo.com/
Free, no API key required.
Daily weather data for Lisbon, Portugal (last 90 days).

## How to Run

1. Install dependencies:
pip install -r requirements.txt

2. Run the pipeline:
python -m src.main

3. Output will be saved to:
- data/processed/output.csv — daily weather data
- data/processed/monthly_summary.csv — aggregated by month

## Transformations Applied
1. Renamed columns for readability
2. Converted date column to datetime type
3. Computed new column: average daily temperature
4. Added month column for grouping
5. Removed rows with missing values
6. Aggregated data by month

## Output Columns
| Column | Description |
|--------|-------------|
| date | Date |
| temp_max_c | Max temperature (°C) |
| temp_min_c | Min temperature (°C) |
| temp_avg_c | Average temperature (°C) |
| precipitation_mm | Daily precipitation (mm) |
| windspeed_max_kmh | Max wind speed (km/h) |
| month | Month (YYYY-MM) |

## Author
Olga Besedina, 2026
