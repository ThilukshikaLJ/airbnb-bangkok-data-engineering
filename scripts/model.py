import duckdb
import pandas as pd

# Connect to DuckDB (creates a file-based database)
con = duckdb.connect('reports/airbnb_bangkok.db')

print("DuckDB connected.")

# Load CSVs into DuckDB tables
con.execute("CREATE OR REPLACE TABLE dim_listings AS SELECT * FROM read_csv_auto('data/listings_enriched.csv')")
con.execute("CREATE OR REPLACE TABLE dim_neighbourhoods AS SELECT * FROM read_csv_auto('data/neighbourhoods.csv')")
con.execute("CREATE OR REPLACE TABLE fact_calendar AS SELECT * FROM read_csv_auto('data/calendar.csv.gz')")

print("Tables created.")

# Verify
print(con.execute("SELECT COUNT(*) FROM dim_listings").fetchall())
print(con.execute("SELECT COUNT(*) FROM fact_calendar").fetchall())

con.execute("""
    CREATE OR REPLACE TABLE dim_date AS
    SELECT DISTINCT
        date,
        EXTRACT(year FROM date) AS year,
        EXTRACT(month FROM date) AS month,
        EXTRACT(day FROM date) AS day,
        EXTRACT(dow FROM date) AS day_of_week,
        CASE WHEN EXTRACT(dow FROM date) IN (0, 6) THEN TRUE ELSE FALSE END AS is_weekend
    FROM fact_calendar
""")

print(con.execute("SELECT COUNT(*) FROM dim_date").fetchall())
print(con.execute("SELECT * FROM dim_date LIMIT 5").fetchall())

# ============================================
# ANALYTICAL SQL QUERIES
# ============================================

print("\n=== QUERY 1: Average price by room type ===")
result = con.execute("""
    SELECT room_type, ROUND(AVG(price_clean), 2) AS avg_price, COUNT(*) AS listing_count
    FROM dim_listings
    WHERE price_clean IS NOT NULL
    GROUP BY room_type
    ORDER BY avg_price DESC
""").fetchall()
for row in result:
    print(row)

print("\n=== QUERY 2: Top 5 neighbourhoods by occupancy rate ===")
result = con.execute("""
    SELECT neighbourhood_cleansed, 
           ROUND(AVG(occupancy_rate), 2) AS avg_occupancy,
           COUNT(*) AS listing_count
    FROM dim_listings
    WHERE occupancy_rate IS NOT NULL
    GROUP BY neighbourhood_cleansed
    HAVING COUNT(*) >= 10
    ORDER BY avg_occupancy DESC
    LIMIT 5
""").fetchall()
for row in result:
    print(row)

print("\n=== QUERY 3: Booking rate by day of week ===")
result = con.execute("""
    SELECT d.day_of_week,
           ROUND(SUM(CASE WHEN f.available = 'f' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS booking_rate
    FROM fact_calendar f
    JOIN dim_date d ON f.date = d.date
    GROUP BY d.day_of_week
    ORDER BY d.day_of_week
""").fetchall()
for row in result:
    print(row)