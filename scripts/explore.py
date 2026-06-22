import pandas as pd

# Load all files
listings = pd.read_csv('data/listings.csv.gz', compression='gzip')
reviews = pd.read_csv('data/reviews.csv')
calendar = pd.read_csv('data/calendar.csv.gz', compression='gzip')
neighbourhoods = pd.read_csv('data/neighbourhoods.csv')

# Listings
print("=== LISTINGS ===")
print("Shape:", listings.shape)
print("Columns:", listings.columns.tolist())

# Reviews
print("\n=== REVIEWS ===")
print("Shape:", reviews.shape)
print("Columns:", reviews.columns.tolist())

# Calendar
print("\n=== CALENDAR ===")
print("Shape:", calendar.shape)
print("Columns:", calendar.columns.tolist())

# Neighbourhoods
print("\n=== NEIGHBOURHOODS ===")
print("Shape:", neighbourhoods.shape)
print("Columns:", neighbourhoods.columns.tolist())

# Check if all listing_ids in reviews exist in listings
print("\n=== RELATIONSHIP CHECK ===")
print("Unique listings in listings file:", listings['id'].nunique())
print("Unique listings in reviews:", reviews['listing_id'].nunique())
print("Unique listings in calendar:", calendar['listing_id'].nunique())

# Detailed schema for each file
print("\n=== LISTINGS SCHEMA ===")
print(listings.dtypes)

print("\n=== REVIEWS SCHEMA ===")
print(reviews.dtypes)
print(reviews.head(3))

print("\n=== CALENDAR SCHEMA ===")
print(calendar.dtypes)
print(calendar.head(3))

print("\n=== NEIGHBOURHOODS SCHEMA ===")
print(neighbourhoods.dtypes)
print(neighbourhoods.head(3))

# Save schema to file
with open('reports/schema_documentation.txt', 'w', encoding='utf-8') as f:
    f.write("=== LISTINGS SCHEMA ===\n")
    f.write(str(listings.dtypes) + "\n\n")
    f.write("Missing Values:\n")
    f.write(str(listings.isnull().sum()[listings.isnull().sum() > 0]) + "\n\n")
    
    f.write("=== REVIEWS SCHEMA ===\n")
    f.write(str(reviews.dtypes) + "\n\n")
    
    f.write("=== CALENDAR SCHEMA ===\n")
    f.write(str(calendar.dtypes) + "\n\n")
    
    f.write("=== NEIGHBOURHOODS SCHEMA ===\n")
    f.write(str(neighbourhoods.dtypes) + "\n\n")

print("Schema saved to reports/schema_documentation.txt")

# Ranges and sample values for key columns
with open('reports/schema_documentation.txt', 'a',  encoding='utf-8') as f:
    f.write("=== LISTINGS SAMPLE VALUES ===\n")
    f.write(str(listings.describe()) + "\n\n")
    f.write(str(listings.head(3)) + "\n\n")

# File relationships
with open('reports/schema_documentation.txt', 'a', encoding='utf-8') as f:
    f.write("=== FILE RELATIONSHIPS ===\n")
    f.write("listings.id = Primary Key\n")
    f.write("reviews.listing_id = Foreign Key → listings.id\n")
    f.write("calendar.listing_id = Foreign Key → listings.id\n")
    f.write("listings.neighbourhood = connects to neighbourhoods.neighbourhood\n")
    f.write("Relationship type: One listing → Many reviews (one-to-many)\n")
    f.write("Relationship type: One listing → Many calendar entries (one-to-many)\n")

listings_simple = pd.read_csv('data/listings.csv')
print(listings_simple['price'].head(10))