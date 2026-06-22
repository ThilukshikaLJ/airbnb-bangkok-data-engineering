import pandas as pd

def load_data():
    listings = pd.read_csv('data/listings.csv.gz', compression='gzip')
    listings_simple = pd.read_csv('data/listings.csv')
    reviews = pd.read_csv('data/reviews.csv')
    calendar = pd.read_csv('data/calendar.csv.gz', compression='gzip')
    listings_simple['price_clean'] = listings_simple['price'].replace(r'[\$,]', '', regex=True).astype(float)
    listings = listings.merge(listings_simple[['id', 'price_clean']], on='id', how='left')
    return listings, reviews, calendar

def clean_price(listings):
    print(f"Price - Valid: {listings['price_clean'].notna().sum()}, Missing: {listings['price_clean'].isna().sum()}")
    listings['price_outlier'] = (listings['price_clean'] < 100) | (listings['price_clean'] > 100000)
    print(f"Price outliers flagged: {listings['price_outlier'].sum()}")
    return listings

def detect_iqr_outliers(listings):
    print("\n=== IQR OUTLIER DETECTION ===")
    
    Q1 = listings['price_clean'].quantile(0.25)
    Q3 = listings['price_clean'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    print(f"Q1: {Q1}, Q3: {Q3}, IQR: {IQR}")
    print(f"Lower bound: {lower_bound}, Upper bound: {upper_bound}")
    
    outliers = ((listings['price_clean'] < lower_bound) | (listings['price_clean'] > upper_bound)).sum()
    print(f"IQR-based price outliers: {outliers}")
    
    listings['price_iqr_outlier'] = (listings['price_clean'] < lower_bound) | (listings['price_clean'] > upper_bound)
    
    return listings

def clean_bedrooms(listings):
    median_bedrooms = listings['bedrooms'].median()
    median_beds = listings['beds'].median()
    listings['bedrooms'] = listings['bedrooms'].fillna(median_bedrooms)
    listings['beds'] = listings['beds'].fillna(median_beds)
    print(f"Bedrooms filled with median: {median_bedrooms}")
    print(f"Beds filled with median: {median_beds}")
    return listings

def clean_dates(listings, reviews):
    listings['last_scraped'] = pd.to_datetime(listings['last_scraped'])
    listings['first_review'] = pd.to_datetime(listings['first_review'])
    listings['last_review'] = pd.to_datetime(listings['last_review'])
    reviews['date'] = pd.to_datetime(reviews['date'])
    print("Dates standardized.")
    return listings, reviews

def remove_duplicates(reviews):
    before = len(reviews)
    reviews = reviews.drop_duplicates()
    print(f"Removed {before - len(reviews)} duplicate reviews")
    return reviews

def validate_data(listings):
    print("\n=== DOMAIN VALIDATION ===")
    
    negative_price = (listings['price_clean'] < 0).sum()
    print(f"Negative prices found: {negative_price}")
    
    invalid_lat = ((listings['latitude'] < -90) | (listings['latitude'] > 90)).sum()
    print(f"Invalid latitude values: {invalid_lat}")
    
    invalid_long = ((listings['longitude'] < -180) | (listings['longitude'] > 180)).sum()
    print(f"Invalid longitude values: {invalid_long}")
    
    invalid_min_nights = (listings['minimum_nights'] <= 0).sum()
    print(f"Invalid minimum_nights (<=0): {invalid_min_nights}")
    
    outside_bangkok = ((listings['latitude'] < 13.0) | (listings['latitude'] > 14.5) |
                        (listings['longitude'] < 100.0) | (listings['longitude'] > 101.0)).sum()
    print(f"Listings outside expected Bangkok region: {outside_bangkok}")
    
    return listings

def save_clean_data(listings, reviews):
    listings.to_csv('data/listings_clean.csv', index=False)
    reviews.to_csv('data/reviews_clean.csv', index=False)
    print("Clean data saved.")

# Run
listings, reviews, calendar = load_data()
listings = clean_price(listings)
listings = detect_iqr_outliers(listings)
listings = clean_bedrooms(listings)
listings, reviews = clean_dates(listings, reviews)
reviews = remove_duplicates(reviews)
listings = validate_data(listings)
save_clean_data(listings, reviews)
print("Cleaning complete.")