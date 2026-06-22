ASSUMPTIONS & DECISIONS LOG
Bangkok, Thailand - Airbnb Dataset
====================================

DECISIONS:
1. license column — ignored, 100% missing, not relevant for Bangkok
2. neighbourhood_group_cleansed — ignored, 100% empty for Bangkok
3. bedrooms/beds — filled with median value (19% missing)
4. review_scores — kept as null, flagged as unreviewed listings
5. price — available in Thai Baht, cleaning required (remove $ symbol)

DATA DICTIONARY NOTES:
- price: $ symbol is artifact, must be removed before analysis
- reviews_per_month: calculated field, can be misleading for new listings
- calculated_host_listings_count: use this (city-specific)
  not host_listings_count (global)
- listings.price = advertised base nightly price (Thai Baht)
- calendar.price = actual daily price (100% empty for Bangkok)

DATASET LIMITATIONS:
1. 35% listings (10,090) have no reviews - new/inactive listings
2. license column 100% empty - no regulatory analysis possible
3. neighbourhood_group_cleansed 100% empty for Bangkok
4. calendar price 100% empty - cannot do daily price analysis
5. Data is static snapshot - not real-time
6. Reviews file only has date, no review text - no sentiment analysis
7. Price outliers: min 4 THB (error), max 1,000,000 THB (extreme)
8. 12,295 duplicate reviews removed (scraping artifact)

BUSINESS DOMAIN CONTEXT:
- Listing: Property available for rent. Contains property details,
  host information, pricing, and availability.
- Host: Person who owns/manages listings. One host can have multiple listings.
- Review: Guest feedback after stay. Proxy for booking demand and quality.
- Calendar: Daily availability per listing over 365 days.
- Neighbourhood: Geographic grouping influencing price and demand.

KEY INSIGHTS FROM EXPLORATION:
1. Bangkok is a large active market - 28,806 listings
2. Average price: 2,528 THB/night (~$70 USD)
3. Median price: 1,379 THB/night (~$38 USD)
4. Average availability: 250 days/year
5. 12,295 duplicate reviews removed (scraping artifact)
6. 35% listings never reviewed - significant inactive segment


CLEANING ACTIONS PERFORMED:
1. Price cleaned - 23,273 valid, 5,533 missing retained as null
2. Price outliers flagged (17 listings) - price < 100 or > 100,000 THB
3. Bedrooms filled with median = 1.0
4. Beds filled with median = 1.0
5. Dates converted to datetime format
6. 12,295 duplicate reviews removed
7. Clean data saved to listings_clean.csv and reviews_clean.csv

DOMAIN VALIDATION RESULTS:
1. No negative prices found - price data is valid
2. No invalid latitude/longitude values
3. No invalid minimum_nights values
4. All listings confirmed within Bangkok geographic region
5. Data passes domain validation checks

IQR OUTLIER ANALYSIS:
- IQR bounds: -1003 to 4133 THB
- 2,154 listings (9%) flagged as price outliers (mostly high-end)
- These likely represent luxury/premium segment, not data errors
- Decision: Keep these listings but flag for separate analysis
  rather than removing them

OCCUPANCY ENRICHMENT:
- Average occupancy rate: 31.47%
- Median occupancy rate: 20.55%
- Skewed distribution - few listings drive most bookings
- Calculated from calendar 'available' field (f = booked)

PRICE PER BEDROOM:
- Median price per bedroom: 1,200 THB
- Mean: 1,793 THB (skewed by luxury outliers)
- Valid calculations: 22,396 listings (bedrooms=0 excluded)

HOST TENURE & ENRICHMENT SUMMARY:
- Average host tenure: 7.05 years
- Median host tenure: 7.59 years
- Range: 0.73 to 17.01 years
- Indicates Bangkok is a mature, established Airbnb market
- Enriched master dataset saved as listings_enriched.csv
  (includes: review counts, occupancy rate, price per bedroom, 
  host tenure)

SQL ANALYTICAL QUERIES.

Top performing neighbourhoods by occupancy:
- Nong Khaem leads at 59.48% (but only 11 listings — small sample)
- Bang Khae: 46.43% (92 listings — more reliable)
- Yan na wa: 42.58% (309 listings — most reliable sample size)

MODELING TRADE-OFF DECISION:

Chose: Star Schema (single fact table - fact_calendar)
Rejected: Galaxy Schema (multiple fact tables - calendar + reviews)

Reasoning:
- Star schema is simpler to query and maintain
- Single fact table reduces join complexity for analysts
- Matches assignment's explicit request for "star schema"

Trade-off accepted:
- Review-based facts (review counts, dates) are not in a 
  separate fact table - they were pre-aggregated into 
  dim_listings during Section 3.3 enrichment instead
- This means review trends over time are less flexible to 
  query directly from the model, but listing-level analysis 
  is simpler and faster
- For a larger production system with reviews growing daily, 
  a galaxy schema would be more scalable


# EDA FINDINGS - Bangkok Airbnb

## 4.1 Price Distribution

Finding: Right-skewed distribution. Most listings priced 900-1500 THB, 
with a long tail toward premium/luxury pricing (up to 1,000,000 THB outlier).

Business Interpretation:
The majority of Bangkok Airbnb listings are priced between 900-1,500 THB 
per night, representing the dominant budget-to-midrange market segment. 
A new host entering this market should price competitively within this 
range to maximize visibility and bookings. The long right tail indicates 
a smaller but viable luxury market exists, but likely requires stronger 
branding or superhost status to compete for high-spending guests.

[Price Distribution](price_distribution.png)

SECTION 3.5 — SKIPPED (Pipeline Automation)

Skills required for this section:
- Python logging module (structured log levels: INFO, ERROR, WARNING)
- try/except exception handling patterns
- Retry decorators or retry libraries (e.g., tenacity)
- Incremental data processing strategies (timestamp-based 
  change detection, watermarking)
- Metadata/audit table design for pipeline observability

Current skill level:
As a beginner in Python, I have hands-on experience with basic 
scripting, pandas data manipulation, and functions - but I have 
not yet learned exception handling, logging frameworks, or 
production pipeline patterns like retry logic and incremental 
processing.

Decision rationale:
Rather than implementing these features superficially (e.g., copying 
boilerplate code I don't understand), I chose to invest my remaining 
time deepening Sections 02, 03.1-03.4, and 04 (EDA) - areas where I 
could genuinely demonstrate understanding and produce quality work.

This decision follows the assignment's own guidance that exceptional 
depth in fewer areas outperforms superficial attempts across all areas.

What I would need to learn first:
- Python's built-in `logging` module documentation
- Basic try/except/finally syntax and exception types
- Concepts of idempotency and incremental ETL design