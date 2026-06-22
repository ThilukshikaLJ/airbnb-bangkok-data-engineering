import pandas as pd

listings = pd.read_csv('data/listings_clean.csv')
reviews = pd.read_csv('data/reviews_clean.csv')
calendar = pd.read_csv('data/calendar.csv.gz', compression='gzip')

print("Data loaded for enrichment.")
print(f"Listings: {listings.shape}")

def enrich_reviews(listings, reviews):
    review_counts = reviews.groupby('listing_id').size().reset_index(name='actual_review_count')
    listings = listings.merge(review_counts, left_on='id', right_on='listing_id', how='left')
    listings['actual_review_count'] = listings['actual_review_count'].fillna(0)
    print(f"Listings with at least 1 review: {(listings['actual_review_count'] > 0).sum()}")
    print(f"Listings with 0 reviews: {(listings['actual_review_count'] == 0).sum()}")
    return listings

def calculate_occupancy(listings, calendar):
    occupancy = calendar.groupby('listing_id')['available'].apply(
        lambda x: (x == 'f').sum() / len(x) * 100
    ).reset_index(name='occupancy_rate')
    
    listings = listings.merge(occupancy, left_on='id', right_on='listing_id', how='left')
    
    print(f"Average occupancy rate: {listings['occupancy_rate'].mean():.2f}%")
    print(f"Median occupancy rate: {listings['occupancy_rate'].median():.2f}%")
    
    return listings

def calculate_price_per_bedroom(listings):
    bedrooms_safe = listings['bedrooms'].replace(0, float('nan'))
    listings['price_per_bedroom'] = listings['price_clean'] / bedrooms_safe
    listings['price_per_bedroom'] = pd.to_numeric(listings['price_per_bedroom'], errors='coerce')
    print(f"Price per bedroom calculated. Valid values: {listings['price_per_bedroom'].notna().sum()}")
    print(listings['price_per_bedroom'].describe())
    return listings

def calculate_host_tenure(listings):
    listings['host_since'] = pd.to_datetime(listings['host_since'])
    today = pd.Timestamp.now()
    listings['host_tenure_years'] = (today - listings['host_since']).dt.days / 365.25
    
    print(f"Host tenure calculated. Valid: {listings['host_tenure_years'].notna().sum()}")
    print(listings['host_tenure_years'].describe())
    
    return listings

# Run all enrichment steps
listings = enrich_reviews(listings, reviews)
listings = calculate_occupancy(listings, calendar)
listings = calculate_price_per_bedroom(listings)
listings = calculate_host_tenure(listings)

# Save enriched data
listings.to_csv('data/listings_enriched.csv', index=False)
print("\nEnriched data saved.")